"""Structure-aware walk over an Ansible YAML document.

Both check_fqcn.py and check_task_safety.py need the same thing: the action key
of every task, told apart from the parameters of that action and from play
keywords. A line-oriented match cannot do that. The pre-repair check_fqcn.sh
reported the `group: root` parameter of a template task and the
`gather_facts: true` play keyword as modules, and `user:`, `command:`, `file:`,
`service:`, `find:`, `meta:` and `mount:` are all common parameter names that
would have fired the same way.

The walk is over the composed node graph rather than the loaded value, because
the node graph keeps the line number of every key and a finding without a line
number is not actionable.

Pure Python, no shell, no temporary files, no Path(__file__).parents[N].
"""

from __future__ import annotations

from typing import Iterator, Tuple

import yaml

# Keys that appear beside an action inside a task and are never the action.
TASK_KEYWORDS = frozenset(
    """
    action any_errors_fatal args async become become_exe become_flags
    become_method become_user changed_when check_mode collections connection
    debugger delay delegate_facts delegate_to diff environment failed_when
    ignore_errors ignore_unreachable listen local_action loop loop_control
    module_defaults name no_log notify poll port register remote_user retries
    run_once tags throttle timeout until vars when with_dict with_fileglob
    with_first_found with_flattened with_indexed_items with_inventory_hostnames
    with_items with_lines with_list with_nested with_random_choice
    with_sequence with_subelements with_together
    """.split()
)

# Keys whose value is a list of tasks.
TASK_LIST_KEYS = ("pre_tasks", "tasks", "post_tasks", "handlers")
NESTED_TASK_KEYS = ("block", "rescue", "always")

# A mapping carrying this key is a play, not a task.
PLAY_MARKER = "hosts"


def _keys(node: yaml.MappingNode) -> set:
    return {k.value for k, _ in node.value if isinstance(k.value, str)}


def _child(node: yaml.MappingNode, name: str):
    for key_node, value_node in node.value:
        if key_node.value == name:
            return value_node
    return None


def iter_tasks(root) -> Iterator[Tuple[yaml.MappingNode, yaml.ScalarNode, object]]:
    """Yield (task_node, action_key_node, action_value_node) for every task.

    A task with no action key -- a bare `block:` wrapper, for instance -- yields
    nothing itself; its nested task lists are walked.
    """
    if root is None:
        return
    if isinstance(root, yaml.SequenceNode):
        items = [i for i in root.value if isinstance(i, yaml.MappingNode)]
        if any(PLAY_MARKER in _keys(i) for i in items):
            for play in items:
                yield from _iter_play(play)
        else:
            yield from _iter_task_list(root)
    elif isinstance(root, yaml.MappingNode):
        if PLAY_MARKER in _keys(root):
            yield from _iter_play(root)
        else:
            # A vars, defaults or meta file. It holds no tasks.
            return


def _iter_play(play: yaml.MappingNode) -> Iterator[Tuple]:
    for key in TASK_LIST_KEYS:
        child = _child(play, key)
        if isinstance(child, yaml.SequenceNode):
            yield from _iter_task_list(child)


def _iter_task_list(seq: yaml.SequenceNode) -> Iterator[Tuple]:
    for item in seq.value:
        if isinstance(item, yaml.MappingNode):
            yield from _iter_task(item)


def _iter_task(task: yaml.MappingNode) -> Iterator[Tuple]:
    for key_node, value_node in task.value:
        key = key_node.value if isinstance(key_node.value, str) else None
        if key is None:
            continue
        if key in NESTED_TASK_KEYS:
            if isinstance(value_node, yaml.SequenceNode):
                yield from _iter_task_list(value_node)
            continue
        if key in TASK_KEYWORDS or key.startswith("_"):
            continue
        yield task, key_node, value_node


def iter_scalars(root, key_name: str) -> Iterator[yaml.ScalarNode]:
    """Yield every scalar node bound to `key_name` anywhere in the document.

    Used for keys such as `mode`, which are parameters rather than actions and
    are equally wrong in a task, a defaults file and a variables file.
    """
    if isinstance(root, yaml.MappingNode):
        for key_node, value_node in root.value:
            if key_node.value == key_name and isinstance(value_node, yaml.ScalarNode):
                yield value_node
            yield from iter_scalars(value_node, key_name)
    elif isinstance(root, yaml.SequenceNode):
        for item in root.value:
            yield from iter_scalars(item, key_name)


def line_of(node) -> int:
    try:
        return node.start_mark.line + 1
    except AttributeError:
        return 0
