# Command and Path Discipline in WSL

## Shell and executable identity

Use the active Linux shell and the tool's working-directory field. Resolve the needed executable with `command -v`; inspect its target or file type when provenance is unclear. A mounted-drive file is not necessarily a Windows executable.

For a missing Linux executable, use `SKILL.md` capability inquiry; report the gap if no authorized compatible tool exists. Do not install tools or switch to a Windows binary automatically.

## Bash quoting and paths

- **Symptom.** Bash syntax/quoting errors, a Windows drive path, backslash-separated arguments, `bad interpreter`, `^M`, or an executable selected from the wrong environment.
- **Diagnosis.** Check the actual shell, current worktree, executable and exact failing path. A missing interpreter, CRLF line ending, execute bit or mount restriction is different from a sandbox denial; do not assume the tool and path are valid.
- **Retry.** Correct only the invocation when that is the cause: use Bash syntax, quote path arguments and use the verified WSL path. Prefer a quoted heredoc for multiline Python or other code over nested `-c` escaping. Use `bash <script>` only when the repository declares Bash and invocation semantics remain valid.
- **Fallback.** Report repository-owned script defects to their owner. Do not rewrite line endings, permissions or scripts as a harness workaround. Route service runtime environment generation to /service-runtime-kit-governance.

Use the verified current checkout. Do not infer a second checkout by mechanically translating a drive letter or clone/move the repository as recovery. For an actual mounted-drive path, use its observed POSIX mount path. WSL path handling needs no MSYS path-conversion flags.

## Command length

- **Symptom.** `Argument list too long` or `E2BIG` before the tool starts.
- **Diagnosis.** Check expanded arguments and relevant environment size without dumping secret values; a smaller successful invocation supports the command-size diagnosis.
- **Retry.** Split independent targets deterministically when batching preserves the operation. Prefer `rg --files` plus focused reads. Do not split a gate whose semantics require the complete input set.
- **Fallback.** Use a tool-supported response file or an allowed useful task artifact for long lists. Do not change repository source to shorten a command.

## Filesystem and process permissions

- **Symptom.** `EACCES`, `EPERM`, `EROFS` or `spawn EPERM` while opening files, launching workers or cleaning build output.
- **Diagnosis.** Identify the failing operation and whether validation started. Inspect the relevant Linux user/group, path ownership/mode and mount when necessary; check effective sandbox writable roots. For mounted-drive files, preserve the distinction between Linux and host filesystem permissions.
- **Retry.** Use `references/10-wsl-sandbox-recovery.md` only when evidence supports a sandbox denial. Preserve the exact gate; affected independent package commands may run serially within the remaining budget.
- **Fallback.** Report actual ownership, mount, executable or project-script problems. Do not apply recursive `chmod`/`chown`, change group membership, disable protection or delete generated output as a speculative fix.

## Docker access

- **Symptom.** Permission denied connecting to a Unix socket, missing socket, or failure to connect to the Docker daemon.
- **Diagnosis.** Resolve the Linux Docker client and intended context/endpoint, including task-provided overrides. Inspect only needed context fields and socket metadata. Distinguish sandbox denial from an unavailable daemon, ordinary socket permissions, wrong context or missing WSL integration. Do not assume the endpoint is `/var/run/docker.sock` or that Docker Desktop is the backend.
- **Retry.** When live Docker evidence is necessary and sandbox denial is supported, use `references/10-wsl-sandbox-recovery.md` for the exact authorized command.
- **Fallback.** Inspect source/config and mark Docker validation blocked. If the verified backend is Docker Desktop, report missing integration for the active distribution. Do not switch contexts, install another engine, restart services or loosen socket permissions automatically. An endpoint access failure proves no container or application defect.

## Port binding

- **Symptom.** `Address already in use`, `EADDRINUSE`, `Permission denied`, `EACCES` or `ports are not available` while binding a local port.
- **Diagnosis.** Use available Linux listener evidence such as `ss -ltnp` for TCP; check address, protocol, port and the environment performing the bind. No visible WSL listener does not prove a Docker backend or host port is free. Privileged-port restrictions and sandbox restrictions differ from an occupied port.
- **Retry.** If the task permits a host-binding change, select a verified available host port without changing the container/application port. For evidenced sandbox denial, follow `references/10-wsl-sandbox-recovery.md` instead.
- **Fallback.** Report an unresolved backend/host restriction. Do not kill listeners, change kernel/network policy or run Windows administration commands as recovery.
