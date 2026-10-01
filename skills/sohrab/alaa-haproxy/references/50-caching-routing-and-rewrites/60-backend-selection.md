# Backend selection

## Selecting a backend

`use_backend <name> if <condition>` with an ACL, or a map when the table is large or is edited by
someone who is not editing the config. Map mechanics, and when a map beats an ACL chain, are in
`20-core-config-and-timeouts.md`. Which paths route where is a routing policy and, when it follows
from the build's output layout, it is decided by `/alaa-frontend-devops`; when it follows from a release step it is decided by
`/alaa-controlled-ops`. `13-canary-map-routing.cfg` is the worked file.
