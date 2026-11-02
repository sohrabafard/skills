<?php

declare(strict_types=1);

// Run from any directory: php test_laravel_middleware_example.php /path/to/vendor/autoload.php
// Exit 0: the documented example passed on real Laravel; 1: behavior failed; 2: unavailable input.
$autoload = $argv[1] ?? null;

if (! is_string($autoload) || ! is_file($autoload)) {
    fwrite(STDERR, "Pass an existing Laravel vendor/autoload.php path.\n");
    exit(2);
}

try {
    require $autoload;
    $runtimeReady = class_exists(\Illuminate\Foundation\Http\Middleware\TransformsRequest::class)
        && class_exists(\Normalizer::class)
        && extension_loaded('mbstring');
} catch (\Throwable $error) {
    fwrite(STDERR, 'Could not load Laravel autoload.php ('.get_class($error).").\n");
    exit(2);
}

if (! $runtimeReady) {
    fwrite(STDERR, "Laravel TransformsRequest, Normalizer, and mbstring are required.\n");
    exit(2);
}

require __DIR__.'/../assets/input-normalization/InputNormalization.php';

$reference = file_get_contents(__DIR__.'/../references/30-backend-middleware-binding.md');

if (! is_string($reference) || preg_match('/```php\R(.*?)\R```/s', $reference, $matches) !== 1) {
    fwrite(STDERR, "The Laravel example was not found.\n");
    exit(1);
}

try {
    eval(substr($matches[1], strlen('<?php')));
} catch (\Throwable $error) {
    fwrite(STDERR, $error->getMessage()."\n");
    exit(1);
}

$middleware = new \App\Http\Middleware\NormalizeRequestInput;

$same = static function (mixed $expected, mixed $actual, string $case): void {
    if ($expected !== $actual) {
        throw new \RuntimeException($case.': expected '.var_export($expected, true).', got '.var_export($actual, true));
    }
};

try {
    $form = \Illuminate\Http\Request::create(
        '/?mobile='.rawurlencode('۱ ۲').'&note='.rawurlencode("Cafe\u{0301} ۱۲"),
        'POST',
        [
            'mobile' => '۰۹۱۲ ۳۸۳ ۰۰۰۰',
            'code' => '۱۲ ۳',
            'national_code' => '۱۲۳ ۴',
            'contact' => ['phone' => '۰۹۱۲ ۳۸۳', 'note' => "Cafe\u{0301} ۱۲"],
            'contacts' => [
                ['phone' => '۱-۲', 'note' => '۱ ۲', 'enabled' => true, 'number' => 12, 'empty' => null],
                ['phone' => '۱ ۲'],
                'named' => ['phone' => '۱ ۲'],
            ],
            'other' => ['phone' => '۱ ۲'],
            'field۱' => '۱',
        ],
    );

    $middleware->handle($form, static fn ($request) => $request);
    $same('12', $form->query->get('mobile'), 'query typed field');
    $same('Café 12', $form->query->get('note'), 'query NFC and digit fold');
    $same('09123830000', $form->request->get('mobile'), 'form top-level typed field');
    $same('123', $form->request->get('code'), 'form code typed field');
    $same('1234', $form->request->get('national_code'), 'form national code typed field');
    $formData = $form->request->all();
    $same('0912383', $formData['contact']['phone'], 'nested typed path');
    $same('Café 12', $formData['contact']['note'], 'nested text NFC');
    $same('12', $formData['contacts'][0]['phone'], 'numeric-index typed path');
    $same('1 2', $formData['contacts'][0]['note'], 'nested default text');
    $same(true, $formData['contacts'][0]['enabled'], 'boolean preserved');
    $same(12, $formData['contacts'][0]['number'], 'number preserved');
    $same(null, $formData['contacts'][0]['empty'], 'null preserved');
    $same('1 2', $formData['contacts'][1]['phone'], 'undeclared numeric index remains text');
    $same('1 2', $formData['contacts']['named']['phone'], 'undeclared named index remains text');
    $same('1 2', $formData['other']['phone'], 'unlisted leaf remains text');
    $same('1', $formData['field۱'], 'value folded without changing key');
    $same(false, array_key_exists('field1', $formData), 'key not folded');

    $json = \Illuminate\Http\Request::create(
        '/',
        'POST',
        [],
        [],
        [],
        ['CONTENT_TYPE' => 'application/json'],
        json_encode([
            'contact' => ['phone' => '۱ ۲'],
            'contact.phone' => '۱ ۲', // Unsupported literal-dot key: Laravel supplies the same transform path.
            'other' => ['phone' => '۱ ۲'],
            'note' => "Cafe\u{0301} ۱۲",
        ], JSON_THROW_ON_ERROR),
    );

    $middleware->handle($json, static fn ($request) => $request);
    $jsonData = $json->json()->all();
    $same('12', $jsonData['contact']['phone'], 'JSON typed path');
    $same('12', $jsonData['contact.phone'], 'unsupported flat-dot collision characterized');
    $same('1 2', $jsonData['other']['phone'], 'JSON unlisted path');
    $same('Café 12', $jsonData['note'], 'JSON text NFC');
} catch (\Throwable $error) {
    fwrite(STDERR, $error->getMessage()."\n");
    exit(1);
}

echo 'PASS Laravel '.\Illuminate\Foundation\Application::VERSION." TransformsRequest example: query, form, JSON, nested typed/text, NFC, and non-strings.\n";
