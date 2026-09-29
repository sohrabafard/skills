# Inputs and components

Open this guide when designing typed inputs or reusable components. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Inputs and components

Declare a type on every input, and constrain it where the set of valid values is
known:

```yaml
spec:
  inputs:
    stage:
      type: string
      default: test
    php-version:
      type: string
      default: "8.5"
      options: ["8.3", "8.4", "8.5"]
    job-prefix:
      type: string
      default: app
      regex: '^[a-z][a-z0-9-]{0,30}$'
    coverage:
      type: boolean
      default: false
    test-command:
      type: array
      default: ["php artisan test"]
```

`type:` takes `string`, `number`, `boolean` or `array`. `options:` restricts a
value to a list. `regex:` restricts a string. All three are checked when the
pipeline is created, which is the entire reason to prefer an input over a
variable for a compile-time value.

Interpolation is `$[[ inputs.name ]]`, and it happens before YAML is parsed.
Never interpolate a free-text input into a quoted shell command
(`sh -lc '$[[ inputs.cmd ]]'`): a quote in the input breaks out of the string.
Type the input as an array and let each element be one command instead.

The split to hold to: **input** for structure — target stage, base image, job
prefix, a bounded option. **Variable** for a runtime value — a registry password,
a cloud role, a deploy URL.

Reference a published component by commit SHA or tag. Resolution precedence is
commit SHA, then tag, then branch, with `~latest` and partial semantic versions
resolving against the catalog. A branch reference makes the component's content
change under the consumer without a change on the consumer's side.
