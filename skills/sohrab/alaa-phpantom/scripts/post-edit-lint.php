<?php
/**
 * Claude PostToolUse adapter: read event JSON, run php -l on a single edited
 * PHP source file, return exit 2 + stderr on syntax error. Never modify files.
 * No PHPantom CLI/JSON-RPC server is started by this hook.
 */

if (PHP_SAPI !== 'cli' || getenv('ALAA_PHPANTOM_LINT') === '0') {
    exit(0);
}

$payload = stream_get_contents(STDIN, 1048577);
if ($payload === false || strlen($payload) > 1048576) {
    exit(0);
}
$event = json_decode($payload, true);
if (!is_array($event)) {
    exit(0);
}
$tool = $event['tool_name'] ?? null;
if ($tool !== null && !in_array($tool, ['Write', 'Edit'], true)) {
    exit(0);
}
$file = $event['tool_input']['file_path'] ?? null;
if (!is_string($file) || $file === '' || str_contains($file, "\0")) {
    exit(0);
}

// Ignore Blade and unrelated extensions. PHP code in Blade is a template.
if (str_ends_with(strtolower($file), '.blade.php') || !str_ends_with(strtolower($file), '.php')) {
    exit(0);
}

if (!str_starts_with($file, '/')) {
    $file = getcwd() . DIRECTORY_SEPARATOR . $file;
}
$resolved = realpath($file);
if ($resolved === false || !is_file($resolved)) {
    exit(0);
}

// Keep the hook scoped to the current repository; never lint arbitrary files.
$project = getenv('CLAUDE_PROJECT_DIR');
if ($project !== false && $project !== '') {
    $projectReal = realpath($project);
    if ($projectReal !== false && $resolved !== $projectReal &&
        !str_starts_with($resolved, $projectReal . DIRECTORY_SEPARATOR)) {
        exit(0);
    }
}

// Passing an argv array avoids spawning a shell and safely handles odd paths.
$descriptors = [
    0 => ['pipe', 'r'],
    1 => ['pipe', 'w'],
    2 => ['pipe', 'w'],
];
$process = @proc_open([PHP_BINARY, '-l', $resolved], $descriptors, $pipes);
if (!is_resource($process)) {
    fwrite(STDERR, "[alaa-phpantom] Unable to run php -l on: $resolved\n");
    exit(2);
}
fclose($pipes[0]);
$out = stream_get_contents($pipes[1]);
$err = stream_get_contents($pipes[2]);
fclose($pipes[1]);
fclose($pipes[2]);
$status = proc_close($process);
if ($status !== 0) {
    fwrite(STDERR, "[alaa-phpantom] PHP syntax error: $resolved\n" . trim((string) $out . "\n" . (string) $err) . "\n");
    exit(2);
}
exit(0);
