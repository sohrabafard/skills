# Lane N focused evidence

- Owner /root/normalization, dispatched alaa-implementer; configured Sol/high from parent-inspected TOML, observed runtime model/effort unknown.
- Cwd repository root; BelowNormal; content identity captured at 2026-09-25T15:58:26Z by lane and subsequently held by parent manifest.
- Changed references/10-normalization-contract.md, references/30-backend-middleware-binding.md; added scripts/test_laravel_middleware_example.php, all under skills/sohrab/alaa-input-normalization.
- Intentional corrections: distinguish 1:1 digit fold from NFC; text length equals NFC(input); typed length does not exceed text. Complete imports/namespace and exact full-path typed selection; explicit contact.phone and contacts.0.phone examples. No wildcard or implicit leaf selection.
- Focused command: python -B skills/sohrab/alaa-input-normalization/assets/input-normalization/normalize_reference.py --self-test; exit 0, 145 corpus cases in both modes. Existing decomposed-accent case demonstrated 2 code points becoming 1 after NFC.
- Focused command: php -l skills/sohrab/alaa-input-normalization/scripts/test_laravel_middleware_example.php; exit 0. Extracted complete Markdown PHP block also syntax checked by lane, exit 0; independent runtime command executes that same block directly.
- Focused command: php skills/sohrab/alaa-input-normalization/scripts/test_laravel_middleware_example.php ../auth/vendor/autoload.php; exit 0 on PHP 8.5.8 / Laravel 13.23.0. Real framework, no stub. Query/form/JSON, nested exact typed/text selection, unlisted indices and leaves, key preservation, NFC, booleans/numbers/nulls checked.
- Canonical implementations and corpus are unchanged; four-runtime harness unrun, no new parity claim.
- Consumer deployment/global middleware registration before validation not executed; the selected proof is real-framework example execution in-process, not a deployed service integration.
- Compression pass preserved load-bearing conditions; numeric wildcard draft was rejected and removed before final snapshot.
- Official source refreshed by lead at https://raw.githubusercontent.com/laravel/framework/v13.23.0/src/Illuminate/Foundation/Http/Middleware/TransformsRequest.php .

## Lane clarification

Individual command timestamps were not captured and are unavailable; do not treat the subsequent content snapshot time as their execution timestamp. Follow-up performed no tests or writes. Exact composition check loaded normalize_reference.py with runpy, selected the existing corpus input e plus U+0301, and asserted output equals text_expected equals U+00E9, input length 2, and output length equals NFC(input) length 1. Snippet lint extracted the first php fenced block from the backend reference using Python regex and piped it to php -l (exit 0). The real-framework command used the existing adjacent auth/vendor/autoload.php. Parent-independent verifier reruns that runtime example on the held snapshot; focused reference/corpus results are retained with this timestamp limitation.

## Fix cycle 1

Correctness findings resolved by original lane in the same three files. Literal-dot keys are explicitly outside the example assumptions; Laravel flat/nested collision is documented and characterized in the real-framework test. Consumers supporting those keys require a separate selection design before adopting the snippet. No new rejection policy or traversal was introduced. Dependency autoload Throwable maps to exit 2. Digit-fold no-insertion/deletion wording excludes NFC.

Focused reruns (repository root, BelowNormal): script php -l 0; extracted Markdown snippet php -l 0; real-Laravel example 0; example invoked with assets/input-normalization/InputNormalization.php as unusable autoload gave expected 2; scoped git diff --check 0. Individual timestamps unavailable. No new fixture file. Canonical assets/corpus untouched; their checks not repeated.

New held source/tool-input digest: 93adc14f11bf9daf79881014dc5803437f21ca88c9d3dbd3c17cc38b6e56a5b9. Original digest preserved in held-snapshot-v1.json. Independent affected verification and both review lenses reopened for the changed normalization inputs; Arvan focused evidence remains applicable.
