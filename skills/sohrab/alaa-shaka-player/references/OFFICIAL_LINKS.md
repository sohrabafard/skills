# Official links

Use these sources whenever you need to verify or refresh the skill:

## Shaka Player

- [Releases](https://github.com/shaka-project/shaka-player/releases)
- [GitHub releases API](https://api.github.com/repos/shaka-project/shaka-player/releases)
- [Pull requests](https://github.com/shaka-project/shaka-player/pulls)
- [Upgrade Guide](https://shaka-player-demo.appspot.com/docs/api/tutorial-upgrade.html)
- [Basic Usage](https://shaka-player-demo.appspot.com/docs/api/tutorial-basic-usage.html)
- [Configuration](https://shaka-player-demo.appspot.com/docs/api/tutorial-config.html)
- [License Server Authentication](https://shaka-player-demo.appspot.com/docs/api/tutorial-license-server-auth.html)
- [FairPlay support](https://shaka-player-demo.appspot.com/docs/api/tutorial-fairplay.html)
- [Monetization with Ads](https://shaka-player-demo.appspot.com/docs/api/tutorial-ad_monetization.html)
- [Debugging](https://shaka-player-demo.appspot.com/docs/api/tutorial-debugging.html)
- [Frequently Asked Questions](https://shaka-player-demo.appspot.com/docs/api/tutorial-faq.html)
- [API reference](https://shaka-player-demo.appspot.com/docs/api/)

## Codex and skill maintenance

- [Agent Skills docs](https://developers.openai.com/codex/skills)
- [Create a skill](https://developers.openai.com/codex/skills#create-a-skill)
- [Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- [Harness engineering](https://openai.com/index/harness-engineering/)

## Refresh order

1. Check the Shaka releases page.
2. Check the Shaka upgrade guide for documented public API, config, and
   deprecation changes.
3. Check the relevant Shaka tutorial or generated API page for current
   supported patterns.
4. Check the Shaka pull request list only for unresolved regressions or
   near-term watch items.
5. Only then reuse an old workaround from this skill.

## Freshness triggers

Re-check official sources when the task mentions latest/current behavior, security,
DRM, browser support, HLS/DASH parsing, ABR, ads, iOS/Safari, TV platforms,
license filters, networking retries, or a workaround copied from an issue.

Treat community wrappers, StackOverflow answers, and issue comments as
troubleshooting-only. They can point to symptoms, but the final recommendation
should come from Shaka docs, releases, source code, or a local reproduction.
