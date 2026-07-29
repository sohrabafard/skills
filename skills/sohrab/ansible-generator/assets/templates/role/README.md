# ROLE_NAME

CHANGE_ME_one_paragraph_describing_what_this_role_does_and_what_it_deliberately_does_not_do

## Requirements

- ansible-core 2.19 or newer on the control node. ansible-core 2.20 and newer
  need control-node Python 3.12 or newer.
- Target hosts run Python 3.9 or newer.
- Platforms this role is tested on:
  - Ubuntu 22.04, 24.04
  - Debian 12, 13
  - RHEL, Rocky and Alma 9, 10
- Collections: CHANGE_ME_collections_or_none, declared in the project's
  `requirements.yml` with a version floor.

A platform not in the list above is a platform nobody tested.

## Role variables

Every variable is declared in `meta/argument_specs.yml` with its type and
whether it is required, so a missing or mistyped value is refused before the
first task runs rather than failing part-way through.

### Required

| Variable | Type | Description |
|---|---|---|
| `ROLE_NAME_version` | str | Version to install. No default: an unpinned version makes the run non-reproducible. |

### Optional

| Variable | Type | Default | Description |
|---|---|---|---|
| `ROLE_NAME_package_name` | str | `CHANGE_ME_package` | Package to install |
| `ROLE_NAME_service_name` | str | `CHANGE_ME_service` | systemd unit name |
| `ROLE_NAME_port` | int | `8080` | TCP port the service listens on |
| `ROLE_NAME_bind_address` | str | `127.0.0.1` | Interface to bind. Loopback by default; a wider bind is the caller's explicit decision. |
| `ROLE_NAME_config_dir` | path | `/etc/CHANGE_ME_service` | Configuration directory |
| `ROLE_NAME_config_mode` | str | `"0644"` | Mode of the rendered configuration file |
| `ROLE_NAME_secret_mode` | str | `"0600"` | Mode of any file holding a credential |
| `ROLE_NAME_enable_ssl` | bool | `false` | Configure TLS |
| `ROLE_NAME_max_connections` | int | `100` | Connection limit written into the configuration |

## Dependencies

None.

## Example

```yaml
- name: Configure CHANGE_ME_service
  hosts: CHANGE_ME_group
  become: true
  roles:
    - role: ROLE_NAME
      vars:
        ROLE_NAME_version: "CHANGE_ME_version"
        ROLE_NAME_port: 9090
        ROLE_NAME_enable_ssl: true
```

## Tags

| Tag | Runs |
|---|---|
| `install` | package installation |
| `configure` | directories and the configuration file |
| `service` | unit state |

## Validating this role

The validator is ansible-validator (/ansible-validator, $ansible-validator).

```bash
bash <ansible-validator>/scripts/validate_role.sh roles/ROLE_NAME
bash <ansible-validator>/scripts/scan_secrets.sh roles/ROLE_NAME
python3 <ansible-validator>/scripts/check_task_safety.py roles/ROLE_NAME
```

Exit 0 is clean, 1 is findings, 2 is could-not-run and is never a pass.

## Licence

MIT

## Author

CHANGE_ME_author
