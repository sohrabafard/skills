# Workspace, Commits, and Integration

## The completion lifecycle

| State | Proven when |
|---|---|
| `IMPLEMENTED` | the focused-tier proof passed and the change sits in a durable local commit |
| `MERGE_CANDIDATE` | every affected integration gate and the required independent review passed |
| `RELEASE_CANDIDATE` | the user asked for a release and the repository's prerequisites passed |

A blocker in a later state never unproves an earlier one, and a release is requested, never
inferred.
