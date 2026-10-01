# Path rewrites and deep-link fallback

## Path rewrites

| Directive | What it changes |
|---|---|
| `http-request set-path <expr>` | replaces the path, leaving the query string |
| `http-request replace-path <match> <replace>` | regex-rewrites the path, leaving the query string |
| `http-request set-pathq` / `replace-pathq` | the same, including the query string |
| `http-request replace-uri <match> <replace>` | rewrites the whole URI including any absolute form |

**The default is no rewrite.** A rewrite that was not required is exactly how an asset prefix gets
stripped, and a stripped prefix produces 404 for every hashed asset while the HTML document loads
normally — which reads as a broken deploy rather than as a rewrite bug. Add a rewrite only when
the origin has been **observed** to serve the asset at a different path from the public one, and
put it behind a named condition so the reason survives in the file.

The reciprocal failure is duplication: a rewrite whose replacement re-adds a prefix the match did
not consume produces `/assets/assets/app.abc12345.js`, which 404s in the same way and looks like
the first failure.

## Deep-link fallback

A single-page or server-rendered application needs a request for `/orders/42` to resolve to the
application entry document, so that a hard refresh returns the same document as a client-side
navigation:

```
acl is_document path_reg '^[^?]*/[^./?]*$'
http-request set-path /index.html if is_document
```

**The guard is that the fallback must not catch asset requests.** The condition above matches only
a path whose last segment has no file extension. Without that guard a missing asset returns the
application document with status 200, and the browser parses HTML as JavaScript — an error whose
message names a syntax error in a file that is not JavaScript, which is among the most expensive
false trails in frontend debugging.
