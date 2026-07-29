# Jinja, filters and lookups

Read this only when writing a Jinja template, a filter chain or a lookup. It is
authoring knowledge and has no counterpart in `ansible-validator`
(`/ansible-validator`, `$ansible-validator`); that skill routes here on a
`jinja[...]` finding.

Three rules that apply to everything below:

1. **A lookup runs on the control node, at template time.** `lookup('file', ...)`
   reads a file on *your* machine, not on the target. To read a file on the
   target, use `ansible.builtin.slurp` and decode the result.
2. **A value that reaches a shell needs `| quote`.** Every example here that
   feeds a `command` or `shell` shows it. `ansible-validator
   references/security_checklist.md` section S6 states the rule and
   `check_task_safety.py` reports a violation.
3. **`mandatory`, not `required`.** There is no `required` filter;
   `{{ x | required('...') }}` fails at run time with `No filter named
   'required'`. Both skills taught the non-existent one until 2026-07-29.

### Common Filters

#### Data Format Conversion

```yaml
- name: Convert to JSON
  ansible.builtin.copy:
    content: "{{ my_dict | to_json }}"
    dest: /tmp/config.json

- name: Convert to YAML
  ansible.builtin.copy:
    content: "{{ my_dict | to_yaml }}"
    dest: /tmp/config.yml

- name: Convert to pretty JSON
  ansible.builtin.copy:
    content: "{{ my_dict | to_nice_json }}"
    dest: /tmp/config.json

# Parse JSON/YAML strings
- name: Parse JSON string
  ansible.builtin.set_fact:
    parsed_data: "{{ json_string | from_json }}"

- name: Parse YAML string
  ansible.builtin.set_fact:
    parsed_data: "{{ yaml_string | from_yaml }}"
```

#### String Manipulation

```yaml
# Regex operations
- name: Replace text
  ansible.builtin.set_fact:
    new_string: "{{ original | regex_replace('^old', 'new') }}"

- name: Extract with regex
  ansible.builtin.set_fact:
    extracted: "{{ text | regex_search('version: (\\d+\\.\\d+)', '\\1') }}"

# Case conversion
- name: Convert case
  ansible.builtin.set_fact:
    upper: "{{ text | upper }}"
    lower: "{{ text | lower }}"
    title: "{{ text | title }}"

# String operations
- name: String operations
  ansible.builtin.set_fact:
    trimmed: "{{ '  text  ' | trim }}"
    replaced: "{{ text | replace('old', 'new') }}"
    split_list: "{{ 'a,b,c' | split(',') }}"
    joined: "{{ ['a', 'b', 'c'] | join('-') }}"
```

#### Hashing and Encoding

```yaml
# Hash values
- name: Generate hashes
  ansible.builtin.set_fact:
    md5_hash: "{{ 'mystring' | hash('md5') }}"
    sha256_hash: "{{ 'mystring' | hash('sha256') }}"

# Password hashing
- name: Hash password
  ansible.builtin.user:
    name: myuser
    password: "{{ user_password | password_hash('sha512', vault_password_salt) }}"
  no_log: true

# Encoding
- name: Encode/decode
  ansible.builtin.set_fact:
    base64_encoded: "{{ 'text' | b64encode }}"
    base64_decoded: "{{ encoded_value | b64decode }}"
    url_encoded: "{{ url_string | urlencode }}"
```

#### List and Dict Operations

```yaml
# List operations
- name: List operations
  ansible.builtin.set_fact:
    unique_items: "{{ my_list | unique }}"
    sorted_items: "{{ my_list | sort }}"
    first_item: "{{ my_list | first }}"
    last_item: "{{ my_list | last }}"
    list_length: "{{ my_list | length }}"
    flattened: "{{ nested_list | flatten }}"

# Dict operations
- name: Dict operations
  ansible.builtin.set_fact:
    dict_keys: "{{ my_dict | dict2items }}"
    dict_values: "{{ my_dict | list }}"
    combined: "{{ dict1 | combine(dict2) }}"

# Extract values
- name: Extract from list of dicts
  ansible.builtin.set_fact:
    names: "{{ users | map(attribute='name') | list }}"
    ids: "{{ items | map(attribute='id') | list }}"
```

#### Network Filters

The `ipaddr` family lives in `ansible.utils`, not in core. Declare
`ansible.utils` in `requirements.yml` and install the `netaddr` Python package
on the control node.

```yaml
# IP address operations (ansible.utils collection plus the netaddr package)
- name: IP operations
  ansible.builtin.set_fact:
    is_valid: "{{ ip_address | ipaddr }}"
    network: "{{ ip_address | ipaddr('network') }}"
    netmask: "{{ ip_address | ipaddr('netmask') }}"
    broadcast: "{{ ip_address | ipaddr('broadcast') }}"
    host_ip: "{{ ip_address | ipaddr('address') }}"

# CIDR operations
- name: CIDR operations
  ansible.builtin.set_fact:
    hosts_in_network: "{{ '192.168.1.0/24' | ipaddr('size') }}"
    first_host: "{{ '192.168.1.0/24' | ipaddr('1') | ipaddr('address') }}"
```

#### File and Math Filters

```yaml
# File size formatting
- name: Format file size
  ansible.builtin.debug:
    msg: "File size: {{ file_stat.stat.size | filesizeformat }}"

# Math operations
- name: Math operations
  ansible.builtin.set_fact:
    sum: "{{ [1, 2, 3] | sum }}"
    min: "{{ [5, 2, 8] | min }}"
    max: "{{ [5, 2, 8] | max }}"
    rounded: "{{ 3.14159 | round(2) }}"
    absolute: "{{ -42 | abs }}"
```

#### Default and Mandatory Values

```yaml
# Provide defaults
- name: Use default values
  ansible.builtin.set_fact:
    port: "{{ custom_port | default(8080) }}"
    config: "{{ app_config | default({}) }}"

# Nested defaults (Ansible 2.8+)
- name: Nested default
  ansible.builtin.set_fact:
    value: "{{ foo.bar.baz | default('fallback') }}"

# Mandatory values
- name: Require variable
  ansible.builtin.set_fact:
    required_value: "{{ must_be_defined | mandatory }}"
```

### Lookup Plugins

#### File and Environment Lookups

```yaml
# Read file content
- name: Read an SSH public key from the control node
  ansible.posix.authorized_key:
    user: deploy
    key: "{{ lookup('file', 'files/deploy_key.pub') }}"

# Environment variables
- name: Get environment variable
  ansible.builtin.set_fact:
    home_dir: "{{ lookup('env', 'HOME') }}"
    path: "{{ lookup('env', 'PATH') }}"

# Pipe command output
# lookup('pipe', ...) runs a shell on the CONTROL NODE. Never interpolate a
# variable into it without | quote: the value runs on your machine.
- name: Get command output from the control node
  ansible.builtin.set_fact:
    current_date: "{{ lookup('pipe', 'date +%Y-%m-%d') }}"
    git_commit: "{{ lookup('pipe', 'git rev-parse HEAD') }}"
```

#### Template and URL Lookups

```yaml
# Template lookup
- name: Inline template
  ansible.builtin.set_fact:
    greeting: "{{ lookup('template', 'greeting.j2') }}"

# URL content
- name: Fetch URL content
  ansible.builtin.set_fact:
    remote_content: "{{ lookup('url', 'https://api.example.com/config') }}"
```

#### Password and Random Lookups

```yaml
# Generate random password
- name: Generate password
  ansible.builtin.set_fact:
    random_password: "{{ lookup('password', '/dev/null length=32 chars=ascii_letters,digits') }}"

# Random choice
- name: Pick random item
  ansible.builtin.set_fact:
    random_server: "{{ lookup('random_choice', ['server1', 'server2', 'server3']) }}"
```

#### Query vs Lookup

```yaml
# lookup returns comma-separated string
- name: Using lookup
  ansible.builtin.debug:
    msg: "{{ lookup('file', 'file1.txt', 'file2.txt') }}"
  # Returns: "content1,content2"

# query always returns list
- name: Using query
  ansible.builtin.debug:
    msg: "{{ query('file', 'file1.txt', 'file2.txt') }}"
  # Returns: ["content1", "content2"]

# Prefer query for loops
- name: Loop with query
  ansible.builtin.debug:
    msg: "{{ item }}"
  loop: "{{ query('inventory_hostnames', 'all') }}"
```

### Template Control Structures

#### Loops in Templates

```jinja2
{# templates/config.j2 #}
# User list
{% for user in users %}
user {{ user.name }}:
  uid: {{ user.uid }}
  groups: {{ user.groups | join(',') }}
{% endfor %}

# Conditional in loop
{% for item in items if item.enabled %}
  - {{ item.name }}: {{ item.value }}
{% endfor %}

# Loop with index
{% for server in servers %}
server_{{ loop.index }}: {{ server.hostname }}
{% endfor %}
```

#### Conditionals in Templates

```jinja2
{# templates/app_config.j2 #}
{% if environment == 'production' %}
log_level: warning
max_connections: 1000
{% elif environment == 'staging' %}
log_level: info
max_connections: 500
{% else %}
log_level: debug
max_connections: 100
{% endif %}

# Complex conditions
{% if ansible_os_family == 'Debian' and ansible_distribution_major_version|int >= 20 %}
use_modern_config: true
{% endif %}

# Check if defined
{% if custom_setting is defined %}
custom_setting: {{ custom_setting }}
{% endif %}

# Check if none
{% if database_host is none %}
database_host: localhost
{% else %}
database_host: {{ database_host }}
{% endif %}
```

#### Whitespace Control

```jinja2
{# Remove whitespace before #}
{%- if condition %}
content
{% endif %}

{# Remove whitespace after #}
{% if condition -%}
content
{% endif %}

{# Remove both #}
{%- if condition -%}
content
{%- endif -%}
```

#### Macros and Includes

```jinja2
{# Define macro #}
{% macro render_user(name, uid) -%}
user: {{ name }}
uid: {{ uid }}
{%- endmacro %}

{# Use macro #}
{{ render_user('alice', 1000) }}
{{ render_user('bob', 1001) }}

{# Include other template #}
{% include 'header.j2' %}

{# Import macros from other template #}
{% from 'macros.j2' import render_user %}
```

### Advanced Template Patterns

#### Multi-line Strings

```jinja2
server {
    listen 80;
    server_name {{ server_name }};

    {% if ssl_enabled %}
    listen 443 ssl;
    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};
    {% endif %}

    location / {
        proxy_pass http://{{ backend_host }}:{{ backend_port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Complex Data Structures

```jinja2
{# Nested loops for complex config #}
{% for service in services %}
[{{ service.name }}]
{% for key, value in service.config.items() %}
{{ key }} = {{ value }}
{% endfor %}

{% endfor %}

{# Generate from dict #}
{% for key, value in app_settings.items() %}
export {{ key | upper }}="{{ value }}"
{% endfor %}
```
