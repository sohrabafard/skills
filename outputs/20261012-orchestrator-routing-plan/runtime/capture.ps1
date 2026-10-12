param(
  [Parameter(Mandatory=$true)][ValidateSet('codex','claude-code')][string]$Runtime,
  [Parameter(Mandatory=$true)][ValidateSet(1,2)][int]$Repetition
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$task = Join-Path $root 'outputs\20261012-orchestrator-routing-plan'
$checker = Join-Path $task 'checker-lane'
$out = $PSScriptRoot
$id = if ($Runtime -eq 'codex') { 'codex' } else { 'claude-code' }
$requestRel = if ($Runtime -eq 'codex') { 'checker-lane/codex-allocation-request.txt' } else { 'checker-lane/claude-code-allocation-request.txt' }
$inputRel = if ($Runtime -eq 'codex') { 'checker-lane/codex-probe-input.json' } else { 'checker-lane/claude-code-probe-input.json' }
$manifestRel = "checker-lane/$id-probe-manifest.json"
$manifest = Get-Content -LiteralPath (Join-Path $task $manifestRel) -Raw | ConvertFrom-Json
$pin = Get-Content -LiteralPath (Join-Path $task 'verification\review-fix\source-pin-refreshed.json') -Raw | ConvertFrom-Json
$pinMismatches = @()
foreach ($entry in $pin) {
  $path = Join-Path $root $entry.path
  if (!(Test-Path -LiteralPath $path)) { $pinMismatches += $entry.path; continue }
  $item = Get-Item -LiteralPath $path
  $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($item.Length -ne $entry.bytes -or $hash -ne $entry.sha256) { $pinMismatches += $entry.path }
}
if ($pinMismatches.Count) { throw "SOURCE_PIN_MOVED: $($pinMismatches -join ', ')" }
$request = Join-Path $task $requestRel.Replace('/', '\')
$input = Join-Path $task $inputRel.Replace('/', '\')
$requestHash = (Get-FileHash -LiteralPath $request -Algorithm SHA256).Hash.ToLowerInvariant()
$inputHash = (Get-FileHash -LiteralPath $input -Algorithm SHA256).Hash.ToLowerInvariant()
$loaded = @()
foreach ($contract in $manifest.loaded_contracts) {
  $path = Join-Path $root $contract.path
  $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
  $loaded += [pscustomobject]@{path=$contract.path;expected_sha256=$contract.sha256;actual_sha256=$hash;matches=($hash -eq $contract.sha256)}
}
if ($requestHash -ne $manifest.request_sha256 -or $inputHash -ne $manifest.input_sha256 -or @($loaded | Where-Object { !$_.matches }).Count) {
  throw 'REQUEST_OR_SOURCE_HASH_MISMATCH'
}
$rep = "r$Repetition"
$stdoutPath = Join-Path $out "$id-$rep-stdout.jsonl"
$stderrPath = Join-Path $out "$id-$rep-stderr.txt"
$finalPath = Join-Path $out "$id-$rep-final.txt"
$metadataPath = Join-Path $out "$id-$rep-metadata.json"
$eventsPath = Join-Path $out "$id-$rep-events-usage.json"
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.UseShellExecute = $false
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.WorkingDirectory = $root
$psi.CreateNoWindow = $true
$dispatchArgv = @()
if ($Runtime -eq 'codex') {
  $node = (Get-Command node -ErrorAction Stop).Source
  $codexShim = (Get-Command codex -ErrorAction Stop).Source
  $shimDir = Split-Path -Parent $codexShim
  $js = Join-Path $shimDir 'node_modules\@openai\codex\bin\codex.js'
  if (!(Test-Path -LiteralPath $js)) { throw 'CODEX_JS_LAUNCHER_MISSING' }
  $psi.FileName = $node
  $psi.ArgumentList.Add($js)
  $dispatchArgv = @('exec','--ignore-user-config','--ephemeral','--sandbox','read-only','--model','gpt-6.1-sol','--config','model_reasoning_effort="high"','--json','--output-last-message',$finalPath,'-')
  foreach ($arg in $dispatchArgv) { $psi.ArgumentList.Add($arg) }
  $launcher = '<RESOLVED_NODE> <RESOLVED_CODEX_CLI_JS>'
  $allocator = 'gpt-6.1-sol'
} else {
  $claude = (Get-Command claude -ErrorAction Stop).Source
  $psi.FileName = $claude
  $dispatchArgv = @('--safe-mode','--tools','','--no-session-persistence','--permission-mode','plan','--model','claude-sonnet-5-5','--effort','high','--output-format','json','-p')
  foreach ($arg in $dispatchArgv) { $psi.ArgumentList.Add($arg) }
  $launcher = '<RESOLVED_CLAUDE_EXE>'
  $allocator = 'claude-sonnet-5-5'
}
$preflight = [pscustomobject]@{
  runtime=$Runtime;repetition=$Repetition;command='dispatch exact argv';cwd='.';request=$requestRel;request_sha256=$requestHash
  probe_input=$inputRel;probe_input_sha256=$inputHash;loaded_sources=$loaded;source_pin_files=$pin.Count
  source_pin='outputs/20261012-orchestrator-routing-plan/verification/review-fix/source-pin-refreshed.json'
  launcher=$launcher;argv=@($dispatchArgv | ForEach-Object { if ($_ -eq $finalPath) { "<REPO_ROOT>/outputs/20261012-orchestrator-routing-plan/runtime/$id-$rep-final.txt" } else { $_ } });requested_model=$allocator;requested_effort='high'
  process_priority='ordinary OS default';affinity='default';timeout_seconds=600;stdin='raw request bytes'
}
$preflight | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $out "$id-$rep-preflight.json") -Encoding utf8
$proc = [System.Diagnostics.Process]::new()
$proc.StartInfo = $psi
$clock = [System.Diagnostics.Stopwatch]::StartNew()
$started = [DateTimeOffset]::Now
if (!$proc.Start()) { throw 'PROCESS_START_RETURNED_FALSE' }
$stdoutFile = [System.IO.File]::Create($stdoutPath)
$stderrFile = [System.IO.File]::Create($stderrPath)
$stdoutCopy = $proc.StandardOutput.BaseStream.CopyToAsync($stdoutFile)
$stderrCopy = $proc.StandardError.BaseStream.CopyToAsync($stderrFile)
$inputBytes = [System.IO.File]::ReadAllBytes($request)
$stdinError = $null
try { $proc.StandardInput.BaseStream.Write($inputBytes,0,$inputBytes.Length); $proc.StandardInput.BaseStream.Flush() } catch { $stdinError = $_.Exception.Message } finally { $proc.StandardInput.Close() }
$finished = $proc.WaitForExit(600000)
if (!$finished) { try { $proc.Kill() } catch {}; $proc.WaitForExit() }
$clock.Stop()
[System.Threading.Tasks.Task]::WaitAll(@($stdoutCopy,$stderrCopy))
$stdoutFile.Dispose(); $stderrFile.Dispose()
$ended = [DateTimeOffset]::Now
$exitCode = if ($finished) { $proc.ExitCode } else { 124 }
$stdoutText = [System.Text.UTF8Encoding]::new($false).GetString([System.IO.File]::ReadAllBytes($stdoutPath))
$finalText = $null
$usage = @()
$eventTypes = @()
$toolEvents = @()
$extractError = $null
if ($Runtime -eq 'codex') {
  if (Test-Path -LiteralPath $finalPath) { $finalText = [System.IO.File]::ReadAllText($finalPath,[System.Text.UTF8Encoding]::new($false)) }
  foreach ($line in ($stdoutText -split "`r?`n")) {
    if (!$line.Trim()) { continue }
    try {
      $evt = $line | ConvertFrom-Json
      if ($evt.type) { $eventTypes += [string]$evt.type }
      if ($evt.type -match 'item\.(started|completed|failed)' -and $evt.item) {
        $toolEvents += [pscustomobject]@{event=$evt.type;item_type=$evt.item.type;item_id=$evt.item.id;name=$evt.item.name}
      }
      foreach ($prop in @('usage','token_usage')) { if ($evt.PSObject.Properties.Name -contains $prop) { $usage += $evt.$prop } }
    } catch { $extractError = 'One or more JSONL stdout lines could not be parsed' }
  }
} else {
  try {
    $wrapper = $stdoutText | ConvertFrom-Json
    if ($wrapper.PSObject.Properties.Name -contains 'result' -and $wrapper.result -is [string]) {
      $finalText = $wrapper.result
      [System.IO.File]::WriteAllText($finalPath,$finalText,[System.Text.UTF8Encoding]::new($false))
    } else { $extractError = 'Claude JSON wrapper has no string result field' }
    if ($wrapper.PSObject.Properties.Name -contains 'usage') { $usage += $wrapper.usage }
    if ($wrapper.PSObject.Properties.Name -contains 'session_id') { $extractError = 'Claude wrapper contains a session identifier; omitted from metadata' }
  } catch { $extractError = 'Claude stdout could not be parsed as JSON' }
}
$strict = [pscustomobject]@{valid_json=$false;root_shape_ok=$false;response_count=$null;unique_key_count=$null;all_30_keys_present=$false;error=$null}
if ($null -ne $finalText) {
  try {
    $doc = [System.Text.Json.JsonDocument]::Parse($finalText)
    $rootElement = $doc.RootElement
    $names = @(); $items = @()
    if ($rootElement.ValueKind -eq [System.Text.Json.JsonValueKind]::Object) {
      foreach ($prop in $rootElement.EnumerateObject()) { $names += $prop.Name; if ($prop.Name -eq 'responses' -and $prop.Value.ValueKind -eq [System.Text.Json.JsonValueKind]::Array) { foreach ($v in $prop.Value.EnumerateArray()) { $items += $v } } }
      $strict.valid_json=$true
      $strict.root_shape_ok=(@($names).Count -eq 1 -and $names[0] -eq 'responses')
      $strict.response_count=$items.Count
      $keys=@(); foreach($item in $items){ if($item.ValueKind -eq [System.Text.Json.JsonValueKind]::Object){$case=$item.GetProperty('case').GetString();$variant=$item.GetProperty('variant').GetString();$keys+="$case/$variant"} }
      $strict.unique_key_count=@($keys|Sort-Object -Unique).Count
      $strict.all_30_keys_present=($strict.root_shape_ok -and $items.Count -eq 30 -and $strict.unique_key_count -eq 30)
    }
    $doc.Dispose()
  } catch { $strict.error='Final response failed strict JSON/wrapper inspection' }
}
$eventInfo=[pscustomobject]@{event_types=$eventTypes;tool_events=$toolEvents;reported_usage=$usage;extract_note=$extractError}
$eventInfo|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $eventsPath -Encoding utf8
$finalPathRelative = $null
$finalHash = $null
if (Test-Path -LiteralPath $finalPath) {
  $finalPathRelative = Split-Path $finalPath -Leaf
  $finalHash = (Get-FileHash -LiteralPath $finalPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
$runtimeAccepted = $false
if ($Runtime -eq 'codex') {
  $runtimeAccepted = ($exitCode -eq 0 -and ($eventTypes -contains 'turn.started' -or $eventTypes -contains 'turn.completed') -and $null -ne $finalText)
} else {
  $runtimeAccepted = ($exitCode -eq 0 -and $null -ne $finalText)
}
$effectiveControlState = if ($runtimeAccepted) { 'runtime accepted the requested invocation controls; serving identity remains unknown' } else { 'unknown; runtime acceptance evidence absent' }
$meta=[pscustomobject]@{
  runtime=$Runtime;repetition=$Repetition;cwd='.';argv_template=@($dispatchArgv | ForEach-Object { if ($_ -eq $finalPath) { "<REPO_ROOT>/outputs/20261012-orchestrator-routing-plan/runtime/$id-$rep-final.txt" } else { $_ } });launcher=$launcher
  requested_model=$allocator;requested_effort='high';effective_controls=$effectiveControlState;observed_serving_identity='unknown'
  started=$started.ToString('o');ended=$ended.ToString('o');duration_seconds=[math]::Round($clock.Elapsed.TotalSeconds,3);timeout_seconds=600;timed_out=(!$finished);exit_code=$exitCode
  stdin_sha256=$requestHash;stdin_bytes=$inputBytes.Length;stdin_write_error=$stdinError
  stdout_path=(Split-Path $stdoutPath -Leaf);stderr_path=(Split-Path $stderrPath -Leaf);final_path=$finalPathRelative
  stdout_sha256=(Get-FileHash -LiteralPath $stdoutPath -Algorithm SHA256).Hash.ToLowerInvariant();stderr_sha256=(Get-FileHash -LiteralPath $stderrPath -Algorithm SHA256).Hash.ToLowerInvariant()
  final_sha256=$finalHash
  strict_wrapper=$strict;events_usage_path=(Split-Path $eventsPath -Leaf);artifact_only_capture=$true
}
$meta|ConvertTo-Json -Depth 8|Set-Content -LiteralPath $metadataPath -Encoding utf8
Write-Output (Get-Content -LiteralPath $metadataPath -Raw)
