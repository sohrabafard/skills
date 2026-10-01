# HAProxy response cache

## HAProxy's own cache

A small-object, in-process cache. It is not a CDN and it is not a replacement for one.

```
cache static_cache
  total-max-size 256        # megabytes; the documented maximum is 4095
  max-object-size 262144    # bytes; at most half of total-max-size
  max-age 60                # seconds
  process-vary on
```

```
frontend ...
  http-request cache-use static_cache if <condition>
backend ...
  http-response cache-store static_cache
```

What it does not do, each of which is a production surprise:

- **An object larger than `max-object-size` is passed through uncached, silently.** A bundle that
  grows past the ceiling stops being cached with no error and no signal other than origin load.
- **The cache does not survive a reload or a restart.** Every config change empties it, so a
  frequent-deploy estate never reaches steady state.
- **It is per process and per node.** On N nodes the first request per node per key still reaches
  the origin, so the origin must be sized for N times the miss rate, not once.
- **A response the origin marks `Cache-Control: no-store` is not stored**, which is the correct
  behaviour and also the reason a cache that appears to do nothing is usually being told not to.
- `process-vary on` stores one entry per `Vary` key instead of refusing to store varying responses
  at all. Without it, any response carrying `Vary` is uncacheable.

`show cache` on the Runtime API reports what is actually stored. Use it before concluding the
cache is working.
