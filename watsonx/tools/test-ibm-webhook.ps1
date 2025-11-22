param(
  [Parameter(Mandatory = $true)] [string] $Action,
  [Parameter(Mandatory = $true)] [hashtable] $Payload,
  [string] $BaseUrl = "http://localhost:8000",
  [string] $ApiKey = $env:IBM_ORCH_API_KEY
)

if (-not $ApiKey) {
  Write-Error "IBM_ORCH_API_KEY is not set. Pass -ApiKey or set the env var." -ErrorAction Stop
}

$uri = "$BaseUrl/webhooks/ibm-orchestrate"
$body = @{ action = $Action; payload = $Payload } | ConvertTo-Json -Depth 10

try {
  $response = Invoke-RestMethod -Method Post -Uri $uri -Headers @{ "X-IBM-ORCH-KEY" = $ApiKey } -ContentType "application/json" -Body $body
  $response | ConvertTo-Json -Depth 10
} catch {
  Write-Error $_
  if ($_.Exception.Response -ne $null) { $_.Exception.Response | Format-List * }
  exit 1
}
