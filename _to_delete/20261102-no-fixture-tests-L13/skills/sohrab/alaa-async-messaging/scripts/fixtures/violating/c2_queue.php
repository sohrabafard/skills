<?php
// Violates C2: a queue declaration with no dead-letter target in the file.
// Prefetch is set, so C1 does not fire here.
$channel->basic_qos(0, 16, false);
$channel->queue_declare('content.jobs.outbox', true, true, false, false);
