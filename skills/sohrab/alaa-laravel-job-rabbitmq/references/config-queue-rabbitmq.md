# Writing or reviewing the `rabbitmq` connection in `config/queue.php`

Read this when adding, editing or reviewing the `rabbitmq` entry in `config/queue.php`, or an `RABBITMQ_*`
variable in `.env`, a Helm `envConfig`, or a Compose file. Which keys the driver reads and which are
silently ignored is in `references/driver-facts.md`; check there before adding a key not listed below. The
package's own minimal example is at
`references/upstream/vyuldashev/9b8df5d.../config/rabbitmq.php`.

## Two corrections to make on sight

**1. `queue_max_priority` without `prioritize_delayed` is inert.** The driver emits `x-max-priority` only
when `prioritize_delayed` is true and `quorum` is false, so a config setting `queue_max_priority` while
`prioritize_delayed` is false reaches the broker with no priority argument at all and a reader believes
priority is configured when it is not. Set both or set neither. When you do set them, note what priority
means here: `createMessage()` sets the AMQP `priority` property to the message's **attempt count**, so
retried messages jump ahead of first attempts — it is not "important jobs first". A `priority` property on
the command object overrides it. Omitting `queue_max_priority` applies a maximum of `2` per the upstream
README, not `10`.

**2. `connection` is a class name, not a connection kind.** Upstream README: "When you specify a
`connection` key in the config, with your own class name, every connection will use your own class" — a
subclass of `PhpAmqpLib\Connection\AMQPStreamConnection` or `AMQPSSLConnection`. A variable named
`RABBITMQ_CONNECTION_TYPE` invites an `amqp` or `amqps` value that the driver will try to resolve as a
class. TLS is selected by `secure`, never here. So name the variable `RABBITMQ_CONNECTION_CLASS`, leave it
unset unless the repository ships such a subclass, and give it no default beyond the package's `'default'`.

## The connection block

```php
'rabbitmq' => [
    'driver' => 'rabbitmq',
    'queue' => env('RABBITMQ_QUEUE', 'default'),

    // Only set when this repository ships an AMQPStreamConnection/AMQPSSLConnection subclass.
    'connection' => env('RABBITMQ_CONNECTION_CLASS', 'default'),

    // Inert on this driver (references/driver-facts.md). Kept so a later switch of
    // QUEUE_CONNECTION to database or redis is not silently unbounded.
    'retry_after' => (int) env('RABBITMQ_RETRY_AFTER', 90),

    'hosts' => [
        [
            'host' => env('RABBITMQ_HOST', '127.0.0.1'),
            'port' => (int) env('RABBITMQ_PORT', 5672),
            'user' => env('RABBITMQ_USER', 'guest'),
            'password' => env('RABBITMQ_PASSWORD', 'guest'),
            'vhost' => env('RABBITMQ_VHOST', '/'),
        ],
    ],

    'worker' => 'default',   // Horizon is forbidden for these workers; see SKILL.md.
    'after_commit' => (bool) env('QUEUE_AFTER_COMMIT', true),

    'lazy' => (bool) env('RABBITMQ_LAZY', true),
    'secure' => (bool) env('RABBITMQ_SECURE', false),
    'network_protocol' => env('RABBITMQ_NETWORK_PROTOCOL', 'tcp'),

    'options' => [
        'heartbeat' => (int) env('RABBITMQ_HEARTBEAT', 10),
        'connection_timeout' => (float) env('RABBITMQ_CONNECTION_TIMEOUT', 3.0),
        'read_timeout' => (float) env('RABBITMQ_READ_TIMEOUT', 3.0),
        'write_timeout' => (float) env('RABBITMQ_WRITE_TIMEOUT', 3.0),
        'channel_rpc_timeout' => (float) env('RABBITMQ_CHANNEL_RPC_TIMEOUT', 0.0),

        // Files mounted from a Secret. Read only when secure is true.
        'ssl_options' => [
            'cafile' => env('RABBITMQ_SSL_CAFILE'),
            'local_cert' => env('RABBITMQ_SSL_LOCALCERT'),
            'local_key' => env('RABBITMQ_SSL_LOCALKEY'),
            'verify_peer' => (bool) env('RABBITMQ_SSL_VERIFY_PEER', true),
            'passphrase' => env('RABBITMQ_SSL_PASSPHRASE'),
        ],

        'queue' => [
            // Set both or neither (correction 1).
            'prioritize_delayed' => (bool) env('RABBITMQ_PRIORITIZE_DELAYED', false),
            // 'queue_max_priority' => (int) env('RABBITMQ_QUEUE_MAX_PRIORITY', 2),

            'exchange' => env('RABBITMQ_EXCHANGE'),
            'exchange_type' => env('RABBITMQ_EXCHANGE_TYPE', 'direct'),
            'exchange_routing_key' => env('RABBITMQ_EXCHANGE_ROUTING_KEY', ''),

            // Adds x-dead-letter-* to queues this driver declares itself. Leave false when the
            // DLX comes from a broker policy, which is the rule in SKILL.md.
            'reroute_failed' => (bool) env('RABBITMQ_REROUTE_FAILED', false),
            'failed_exchange' => env('RABBITMQ_FAILED_EXCHANGE', 'amq.direct'),
            'failed_routing_key' => env('RABBITMQ_FAILED_ROUTING_KEY', '%s.failed'),

            'quorum' => (bool) env('RABBITMQ_QUEUE_QUORUM', true),

            // Only when an external producer publishes a payload Laravel did not build.
            // 'job' => \App\Queue\Jobs\RabbitMQJob::class,
        ],
    ],
],
```

## Boundary validation

These values are read once at boot and never re-validated, so a wrong one surfaces as a runtime AMQP error
at first publish rather than a startup failure. Therefore:

- Cast every numeric and boolean `env()` at the point of read, as above. A Helm `envConfig` delivers `"0"`
  as a string, which is truthy in a bare comparison; the `(bool)` cast is what makes it `false`.
- Queue, exchange and vhost names are contract surfaces, not local choices. Take them from
  `alaa-services-contract references/23-queue-and-exchange-registry.md`, which also decides event versus
  command before the topology follows.
- `RABBITMQ_PASSWORD` and every `RABBITMQ_SSL_*` path are the secret-bearing keys on this connection; the
  rule that governs them is `SKILL.md` constraint 12.
- **One canonical env name per setting.** This file uses `RABBITMQ_USER` and `RABBITMQ_PASSWORD`, matching
  the package's published config. Do not write `env('RABBITMQ_USER', env('RABBITMQ_USERNAME', ...))`
  fallback chains: two names for one value means changing one of them silently does nothing and the reader
  cannot tell which is live. Where a repository already ships an alias, delete the alias in the same change
  that renames the variable in every manifest.

## `after_commit`

Keep `after_commit => true`. A job dispatched inside a transaction and consumed before that transaction
commits reads rows that do not exist yet, and on this driver that failure looks like a spurious
"model not found" that disappears on retry. Per-dispatch `->afterCommit()` and `->beforeCommit()` still
override it where one dispatch needs the other behaviour.
