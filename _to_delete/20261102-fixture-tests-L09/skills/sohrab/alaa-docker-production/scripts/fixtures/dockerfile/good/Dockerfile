# syntax=docker/dockerfile:1
# Fixture: a compliant Octane/Swoole runtime image, reduced to the lines the checker inspects.
# The full worked artifact, with the reasoning for every line, is in
# alaa-docker-production references/10-dockerfile-authorship.md.

ARG OCTANE_BASE_IMAGE=registry.example.invalid/docker/octane-base:v1.3.1
ARG COMPOSER_VERSION=2.9.5

FROM composer:2.9.5 AS composer-bin

FROM registry.example.invalid/docker/octane-base:v1.3.1 AS vendor
WORKDIR /app
COPY --from=composer-bin /usr/bin/composer /usr/bin/composer
# Manifest and lockfile first: this layer is invalidated only when a dependency changes.
COPY composer.json composer.lock ./
RUN --mount=type=cache,target=/tmp/composer,uid=1000,gid=1000 \
    COMPOSER_HOME=/tmp/composer composer install \
      --no-dev --no-scripts --no-interaction --prefer-dist --optimize-autoloader
# Application source arrives after the install, so a source edit does not re-resolve dependencies.
COPY . .
RUN COMPOSER_HOME=/tmp/composer composer dump-autoload --classmap-authoritative --no-dev

FROM registry.example.invalid/docker/octane-base:v1.3.1 AS runtime
ARG VCS_REF=unknown
LABEL org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.title="comment-service" \
      org.opencontainers.image.base.name="registry.example.invalid/docker/octane-base:v1.3.1"
WORKDIR /var/www/html
COPY --from=vendor --chown=1000:1000 /app /var/www/html
COPY --chown=1000:1000 --chmod=0555 docker/octane/ /usr/local/bin/octane/
ENV OCTANE_SERVER=swoole OCTANE_PORT=8000
EXPOSE 8000
STOPSIGNAL SIGTERM
HEALTHCHECK --interval=10s --timeout=2s --start-period=45s --start-interval=2s --retries=3 \
  CMD ["/usr/local/bin/octane/healthcheck.sh"]
USER 1000:1000
ENTRYPOINT ["/usr/local/bin/octane/entrypoint.sh"]
CMD ["/usr/local/bin/octane/start-octane.sh"]
