# Ansible ruleset: 2. Naming

## 2. Naming

**2.1 Every task has a `name`.** The name is what an operator reads in the
output of a failing run at 03:00.
*Reported by:* `ansible-lint` rule `name[missing]`, which `assets/.ansible-lint`
enables. `scripts/check_assets.sh` asserts that it fires.

**2.2 A task name starts with a capital letter and a verb in the imperative:**
"Install nginx", "Ensure the configuration directory exists", "Reload the web
server". A name that describes a noun ("Nginx configuration") does not say what
the task did when it appears beside `changed`.
*Reported by:* `ansible-lint` rule `name[casing]` for the capital;
nothing reports the verb.

**2.3 Variables are `snake_case`,** and a role's variables carry the role name
as a prefix: `nginx_worker_processes`, not `workers`. An unprefixed variable in
a role collides with the same name in another role at play scope, and the
collision is silent.
*Reported by:* `ansible-lint` rule `var-naming`, with the pattern in
`assets/.ansible-lint`.

**2.4 Files and directories are lowercase with underscores.**
*Reported by:* nothing. This is a review finding.
