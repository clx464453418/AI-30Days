# ============================================================
#  关闭本地模型（Ollama）—— 腾出显存
#  双击桌面的「关闭本地模型」即可运行
# ============================================================
Write-Host ''
Write-Host '=== 关闭本地模型（Ollama）===' -ForegroundColor Cyan

$before = (& nvidia-smi --query-gpu=memory.used --format=csv,noheader) 2>$null
$procs = @(Get-Process -Name 'ollama*' -ErrorAction SilentlyContinue)
if ($procs.Count -eq 0) {
    Write-Host '没有正在运行的 Ollama 进程。' -ForegroundColor Yellow
} else {
    foreach ($p in $procs) { Write-Host ('  结束: ' + $p.ProcessName + ' (PID ' + $p.Id + ')') }
    $procs | Stop-Process -Force
    Start-Sleep -Seconds 2
}
$after = (& nvidia-smi --query-gpu=memory.used --format=csv,noheader) 2>$null

Write-Host ''
Write-Host ('显存占用: ' + $before + '  ->  ' + $after)
Write-Host '已关闭' -ForegroundColor Green
Start-Sleep -Seconds 4