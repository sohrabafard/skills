# Backend selection

## Selecting a backend

Write `use_backend <name> if <condition>` with an ACL. Use a map instead of the ACL when the table is large,
or when someone who does not edit the config edits the table. Map mechanics, and when a map beats an ACL chain, are in
`20-core-config-and-timeouts.md`. Which paths route where is a routing policy and, when it follows
from the build's output layout, it is decided by `/alaa-frontend-devops`; when it follows from a release step it is decided by
`/alaa-controlled-ops`. `13-canary-map-routing.cfg` is the worked file.
