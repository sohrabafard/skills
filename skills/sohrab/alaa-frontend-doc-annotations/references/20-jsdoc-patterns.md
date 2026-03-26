# JSDoc Patterns

Use this file when you need the default annotation shapes for this skill.

## File-level header

Use a short file header when a file has non-obvious responsibility, lifecycle constraints, or SSR behavior.

Typical content:

- what the file owns
- why it exists
- how it interacts with nearby files
- one or two `@see` references when useful

## Function-level JSDoc

Use JSDoc for functions, actions, helpers, or composables when it adds real value.

Focus on:

- parameters
- return values
- side effects
- SSR or hydration notes when relevant
- store or auth notes when relevant

## Inline comments

Use inline comments only at reasoning hotspots.

Preferred prefixes:

- `SSR NOTE:`
- `HYDRATION NOTE:`
- `STORE NOTE:`
- `AUTH NOTE:`

## Anti-patterns

- explaining obvious syntax
- repeating type information that is already clear from JSDoc tags
- leaving long paragraphs inside function bodies
- using comments to apologize for confusing code instead of clarifying the actual boundary
