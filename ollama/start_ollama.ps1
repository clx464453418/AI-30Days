# ============================================================
#  启动本地模型（Ollama）
#  双击桌面的「启动本地模型」即可运行
#  ⚠️ 必须先把模型目录指到 D:\OllamaModels，否则它会去 C 盘找
# ============================================================
$ErrorActionPreference = 'SilentlyContinue'
$env:OLLAMA_MODELS = 'D:\OllamaModels'
$Port = 11434

Write-Host ''
Write-Host '=== 启动本地模型（Ollama）===' -ForegroundColor Cyan
Write-Host ('模型目录: ' + $env:OLLAMA_MODELS)

if (Get-Process -Name 'ollama*') {
    Write-Host 'Ollama 已经在运行了，跳过启动。' -ForegroundColor Yellow
} else {
    Write-Host '正在启动 Ollama...'
    Start-Process -FilePath 'D:\Ollama\ollama app.exe'
}

# 就绪探测：裸 TCP 连端口（比 HTTP 快、且不受系统代理影响）
Write-Host -NoNewline '等待服务就绪'
$ok = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $c = New-Object System.Net.Sockets.TcpClient
        $c.Connect('127.0.0.1', $Port)
        $c.Close()
        $ok = $true
        break
    } catch { }
    Write-Host -NoNewline '.'
    Start-Sleep -Seconds 1
}
Write-Host ''

if ($ok) {
    Write-Host ('端口 ' + $Port + ' 已就绪') -ForegroundColor Green
    Write-Host '已安装的模型：'
    & 'D:\Ollama\ollama.exe' list
    Write-Host ''
    Write-Host '接口地址:    http://localhost:11434'
    Write-Host 'OpenAI 兼容: http://localhost:11434/v1'
} else {
    Write-Host '启动超时（30 秒）。' -ForegroundColor Red
    Write-Host '请手动双击 D:\Ollama\ollama app.exe，看有没有报错。'
}
Write-Host ''
Write-Host '（这个窗口可以关掉，模型服务会继续在后台运行）' -ForegroundColor DarkGray
Start-Sleep -Seconds 4