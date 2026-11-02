<?php
// Conforming: prefetch set explicitly, dead-letter arguments declared with the queue.
$channel->basic_qos(0, 32, false);
$channel->queue_declare('auth.jobs.sms', true, true, false, false, false, [
    'x-dead-letter-exchange' => ['S', 'auth.commands.dlx'],
    'x-delivery-limit' => ['I', 5],
]);
$channel->basic_consume('auth.jobs.sms', '', false, false, false, false, $handler);
