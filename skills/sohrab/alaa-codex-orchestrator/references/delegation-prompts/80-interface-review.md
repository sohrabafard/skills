# Interface review templates

## Accessibility reviewer

```xml
<task>Review accessibility for: <changed interface>.</task>
<trigger>New or changed user-visible interface — components, forms, dialogs, navigation, tables, and any flow a user completes with a keyboard or a screen reader.</trigger>
<surface><components, templates, styles, and routes in scope, and the flows they compose></surface>
<rendered_evidence><snapshots, accessibility tree output, automated scan results, or explicitly none></rendered_evidence>
<design_system><design tokens, focus-style resets, and motion conventions in force></design_system>
<locales><shipped locales, and whether an RTL locale is among them></locales>
<action_safety>Read-only. Never fix markup, styles, or components, and never pass a check that requires rendered evidence you were not given.</action_safety>
<output>First line exactly VERDICT: ACCESSIBLE | VERDICT: ACCESSIBLE-WITH-GAPS | VERDICT: BLOCK; then FINDINGS with file:line, severity, the barrier, who it blocks, concrete fix; RTL AND LOCALE NOTES; NOT ASSESSED; EVIDENCE INSPECTED.</output>
```

## Browser QA

```xml
<task>Execute browser QA for: <user-visible behavior>.</task>
<environment><URL, existing server, auth/test data, viewport></environment>
<scenarios><exact steps and expected results></scenarios>
<browser_constraint>Preserve --browser chromium and configured profile. Do not start duplicate services.</browser_constraint>
<artifacts><absolute permitted artifact directory></artifacts>
```
