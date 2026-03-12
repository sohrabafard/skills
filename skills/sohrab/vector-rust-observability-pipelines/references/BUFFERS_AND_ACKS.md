
# Buffers and acknowledgements

## Buffers
### memory
- faster
- less durable
- data can be lost on crash/restart

### disk
- more durable
- slower
- requires `data_dir`, writable disk, and monitoring

## when_full
### block
- backpressure propagates upstream
- data preserved more often
- latency and source pressure can rise

### drop_newest
- preserves liveness
- intentionally loses events
- appropriate only when loss is acceptable

## Acknowledgements
Use end-to-end acknowledgements when:
- the source and sink path support them
- the durability contract is worth the latency / throughput cost
- you understand fanout implications

Do not assume acknowledgements are free; they can materially affect throughput and failure semantics.
