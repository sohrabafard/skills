
# Troubleshooting

## Sink healthy but no data arrives
- validate the config
- inspect internal logs
- inspect sink auth/TLS errors
- confirm routing conditions and VRL outputs
- verify buffer / ack settings and backpressure behavior

## Pipeline stalls
- inspect `buffer.when_full`
- inspect disk buffer capacity and `data_dir`
- inspect whether a slow sink in fanout is blocking the path

## Data loss / duplication
- revisit acknowledgement settings
- inspect retry and timeout behavior
- confirm whether the source actually participates in end-to-end acknowledgements

## OOM or high CPU
- inspect source burstiness
- inspect batching and buffering
- inspect VRL cost
- inspect version-specific regressions or sink-specific hot paths
