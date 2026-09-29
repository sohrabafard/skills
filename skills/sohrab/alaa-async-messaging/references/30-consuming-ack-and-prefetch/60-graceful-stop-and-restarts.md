# Graceful stop and rolling restarts

## Graceful stop and rolling restarts

**A worker's graceful-stop budget must exceed the longest handler's own deadline.** When the stop budget is
shorter, a rolling restart kills handlers mid-flight, and every one of those messages is redelivered — so a
routine deploy converts in-flight work into a redelivery burst, at the exact moment fewer consumers are
running to absorb it.

Two consequences: **give the handler an explicit deadline**, since a handler with no deadline makes the
correct stop budget unknowable; and **stop accepting new deliveries first, then finish in-flight work**, so
the drain is bounded by one handler's deadline rather than by the queue's depth.

The Go kit expresses shutdown in ordered phases against a fixed budget, and Laravel workers express it
through the worker command and its process supervisor. Neither expression is this file's ground: the rule is
the ordering between the two budgets. Laravel specifics are `/alaa-laravel-job-rabbitmq`; container and Deployment expression are `/alaa-docker-production` and `/alaa-k8s-helm`.
