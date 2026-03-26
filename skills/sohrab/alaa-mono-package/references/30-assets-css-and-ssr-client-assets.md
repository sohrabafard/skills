# Assets, CSS, and Final Client Assets

Use this file when the task touches package CSS, images, fonts, or emitted assets.

## Asset rule

Package runtime CSS and assets must stay in the bundling graph so the final browser build emits them into the client asset output.

## Good defaults

- import package CSS from the package entry
- keep assets referenced through the normal bundling graph
- use deterministic asset paths

## Risk areas

- package CSS never imported by the root app
- package assets copied to side paths that the final build does not ship
- runtime URLs that point outside the deployed asset root

## Verification

- build the final app
- inspect the final client asset folder
- confirm the package assets really landed there
