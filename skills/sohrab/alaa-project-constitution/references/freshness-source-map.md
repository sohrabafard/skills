# Freshness and Source Map

Read this reference whenever a rule depends on a current external value. It owns the research
source priority, where to look for each class of obligation value, and the freshness rule that
governs writing any of them into policy.

Repository truth remains authoritative for the project's current behaviour. External sources are
authoritative for what a standard currently requires and for a vendor's current documented
semantics — never for what this project does.

## Model, effort, and runtime questions are owned elsewhere

`/alaa-prompting-guide` — `$alaa-prompting-guide` in Codex — is the sole authority for model
selection, effort and thinking budgets, prompting technique, agent definitions, and runtime
capability questions. Route every such question there and cite it rather than restating a pin.
This file deliberately contains no model names, tiers, or effort ladders: a pin copied into a
second file goes stale silently and then gets copied forward because it looks authoritative.

## Research source priority

For any obligation value, prefer in this order:

1. current standards, specifications, and guidance from a standards body, regulator, or security
   body;
2. official framework, database, browser, platform, protocol, and vendor documentation for the
   version the project pins;
3. maintained upstream repositories, reference implementations, and primary research;
4. reputable engineering articles, and only where a primary source does not answer the question.

Use narrow queries that name the surface and the failure mode, not the topic. Verify every
version-sensitive claim live when tools are available. Record source URL, verification date,
applicability, and limitation for each value.

## Where each obligation's numbers live

Named authorities, not values. Fetch the current document; if a URL no longer resolves, search
for the named document from the named publisher rather than substituting a remembered number.

| Obligation class | Authority to fetch |
|---|---|
| Core Web Vitals metric set and thresholds | The Web Vitals documentation published by the Chrome team on `web.dev` |
| Lighthouse categories, weighting, and scoring | The Lighthouse scoring documentation for the version the project runs |
| Field performance data | The Chrome UX Report documentation, plus the project's own RUM provider docs |
| Accessibility conformance level and version | W3C WAI, for the standard the project targets, at its current version |
| Structured data types and validation | `schema.org` for the vocabulary, plus the consuming search provider's own structured-data documentation |
| Robots, crawl, and AI-crawler directives | Each search or AI provider's own crawler documentation, because directive support differs per provider |
| Service worker and browser storage semantics | MDN plus the relevant W3C/WHATWG specification, checked against the target browser versions |
| Broker delivery, acknowledgement, and quorum semantics | The broker's own documentation for the pinned version |
| Scheduler missed-run and concurrency behaviour | The scheduler's or orchestrator's documentation for the pinned version |
| Warehouse transactional and late-arrival semantics | The warehouse vendor's documentation for the version in use |
| Auth, token, and transport standards | The relevant RFC or specification at its current status, plus the implementing library's docs |
| Regulatory retention and personal-data duties | The regulator's own published guidance for the project's jurisdiction |
| Platform background execution and push limits | The mobile platform vendor's current developer documentation for the target OS versions |


## The freshness rule for generated constitutions

Never write a volatile value into binding policy from memory — no metric threshold, category score,
framework version, browser support level, security-standard version, retention period, price, or
token limit. Fetch the current official page when the value materially affects a rule, then record
the value with its source URL and verification date.

When live verification is unavailable, write the rule with the metric or standard named and the
value carried as a non-blocking factual TODO. State the obligation and defer only the number: a
named metric with a pending value governs behaviour, while a dropped rule governs nothing. Do not
present an unverified value as current.
