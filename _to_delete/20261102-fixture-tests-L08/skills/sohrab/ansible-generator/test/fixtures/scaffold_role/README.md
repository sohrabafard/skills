# demo_nginx

Installs nginx and renders one configuration file. It does not manage virtual hosts or TLS material.

## Requirements

- ansible-core 2.19 or newer on the control node. ansible-core 2.20 and newer
  need control-node Python 3.12 or newer.
- Target hosts run Python 3.9 or newer.
- Platforms this role is tested on:
  - Ubuntu 22.04, 24.04
  - Debian 12, 13
  - RHEL, Rocky and Alma 9, 10
- Collections: none, declared in the project's
  `requirements.yml` with a version floor.

A platform not in the list above is a platform nobody tested.

## Role variables

Every variable is declared in `meta/argument_specs.yml` with its type and
whether it is required, so a missing or mistyped value is refused before the
first task runs rather than failing part-way through.

### Required

| Variable | Type | Description |
|---|---|---|
| `demo_nginx_version` | str | Version to install. No default: an unpinned version makes the run non-reproducible. |

### Optional

| Variable | Type | Default | Description |
|---|---|---|---|
| `demo_nginx_package_name` | str | `nginx` | Package to install |
| `demo_nginx_service_name` | str | `nginx` | systemd unit name |
| `demo_nginx_port` | int | `8080` | TCP port the service listens on |
| `demo_nginx_bind_address` | str | `127.0.0.1` | Interface to bind. Loopback by default; a wider bind is the caller's explicit decision. |
| `demo_nginx_config_dir` | path | `/etc/nginx` | Configuration directory |
| `demo_nginx_config_mode` | str | `"0644"` | Mode of the rendered configuration file |
| `demo_nginx_secret_mode` | str | `"0600"` | Mode of any file holding a credential |
| `demo_nginx_enable_ssl` | bool | `false` | Configure TLS |
| `demo_nginx_max_connections` | int | `100` | Connection limit written into the configuration |

## Dependencies

None.

## Example

```yaml
- name: Configure nginx
  hosts: webservers
  become: true
  roles:
    - role: demo_nginx
      vars:
        demo_nginx_version: "1.26.2"
        demo_nginx_port: 9090
        demo_nginx_enable_ssl: true
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
bash <ansible-validator>/scripts/validate_role.sh roles/demo_nginx
bash <ansible-validator>/scripts/scan_secrets.sh roles/demo_nginx
python3 <ansible-validator>/scripts/check_task_safety.py roles/demo_nginx
```

Exit 0 is clean, 1 is findings, 2 is could-not-run and is never a pass.

## Licence

MIT

## Author

ansible-generator fixtures
