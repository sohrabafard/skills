# Official Reference Map

Use these references when the exact shell version, utility flag, or portability rule matters. Re-check them when the task is version-sensitive.

## Freshness triggers

Re-check official or primary sources when the user asks for latest/current behavior, shell-version differences, POSIX portability, BusyBox/dash/macOS compatibility, ShellCheck or shfmt rule behavior, security-sensitive shell code, or GNU/BSD utility flags.

## Core shell references

- GNU Bash Reference Manual  
  Purpose: definitive Bash behavior, builtins, variables, and Bash-only features  
  URL: https://www.gnu.org/software/bash/manual/

- POSIX.1-2024 Shell and Utilities  
  Purpose: the portability baseline for `/bin/sh` and standard utilities  
  URL: https://pubs.opengroup.org/onlinepubs/9799919799/

- Google Shell Style Guide  
  Purpose: naming, structure, and maintainability guidance for shell code  
  URL: https://google.github.io/styleguide/shellguide.html

## Validation and formatting

- ShellCheck  
  Purpose: shell linting, warnings, and directive behavior  
  URL: https://www.shellcheck.net/

- ShellCheck Wiki  
  Purpose: detailed rule explanations and directive patterns  
  URL: https://www.shellcheck.net/wiki/

- shfmt  
  Purpose: formatting and EditorConfig-aware shell formatting behavior  
  URL: https://github.com/mvdan/sh/tree/master/cmd/shfmt

- checkbashisms  
  Purpose: detect likely Bashisms in `/bin/sh` scripts  
  URL: https://manpages.debian.org/testing/devscripts/checkbashisms.1.en.html

- Bats-core  
  Purpose: Bash-focused CLI and behavior tests  
  URL: https://github.com/bats-core/bats-core

## Platform and distro references

- Alpine Linux BusyBox page  
  Purpose: default shell and BusyBox-centric userland behavior  
  URL: https://wiki.alpinelinux.org/wiki/BusyBox

- Debian Shell wiki  
  Purpose: `/bin/sh` and `dash` expectations on Debian systems  
  URL: https://wiki.debian.org/Shell

- Apple Terminal shell guide  
  Purpose: macOS default interactive shell behavior  
  URL: https://support.apple.com/guide/terminal/change-the-default-shell-trml113/mac

## High-performance external tools

- ripgrep  
  Purpose: fast recursive code and text search  
  URL: https://github.com/BurntSushi/ripgrep

- fd  
  Purpose: fast file discovery for developer workflows  
  URL: https://github.com/sharkdp/fd

- jq  
  Purpose: JSON processing  
  URL: https://jqlang.org/manual/

- yq  
  Purpose: YAML and mixed structured config processing  
  URL: https://mikefarah.gitbook.io/yq

- GNU Parallel  
  Purpose: documented advanced parallel command execution  
  URL: https://www.gnu.org/software/parallel/

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for concrete troubleshooting after manuals, tool docs, lint output, and local reproduction are checked. Do not use them as normative portability, security, or style policy.
