# References and attribution

This locally authored integration follows the packaging conventions of PHPantom's upstream MIT-licensed Claude plugin (`PHPantom-dev/phpantom_claude`). The source plugin's design (native .lsp.json, launcher, root plugin manifest, global PostToolUse hook and PHP analysis skill) is used as an architectural reference. Code in the bundled launcher and hook is independently written for the specified already-installed WSL environment; it is not a copy of upstream source. All feature claims are subject to the user's installed PHPantom and Claude Code versions.

- https://github.com/PHPantom-dev/phpantom_claude/blob/main/LICENSE
- https://github.com/PHPantom-dev/phpantom_claude
- https://github.com/PHPantom-dev/phpantom_lsp
