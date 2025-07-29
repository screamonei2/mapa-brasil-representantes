# Servidor HTTP simples em PowerShell
param(
    [int]$Port = 8001,
    [string]$Path = "./old"
)

Write-Host "Iniciando servidor HTTP na porta $Port..."
Write-Host "Servindo arquivos do diretório: $Path"
Write-Host "Acesse: http://localhost:$Port"
Write-Host "Pressione Ctrl+C para parar o servidor"

# Criar listener HTTP
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()

try {
    while ($listener.IsListening) {
        # Aguardar requisição
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        # Obter caminho do arquivo
        $localPath = $request.Url.LocalPath
        if ($localPath -eq "/") { $localPath = "/index.html" }
        
        $filePath = Join-Path $Path $localPath.TrimStart('/')
        
        Write-Host "$(Get-Date -Format 'HH:mm:ss') - $($request.HttpMethod) $localPath"
        
        if (Test-Path $filePath -PathType Leaf) {
            # Arquivo existe - servir o arquivo
            $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
            
            # Definir Content-Type baseado na extensão
            $extension = [System.IO.Path]::GetExtension($filePath).ToLower()
            switch ($extension) {
                ".html" { $response.ContentType = "text/html; charset=utf-8" }
                ".css"  { $response.ContentType = "text/css" }
                ".js"   { $response.ContentType = "application/javascript" }
                ".json" { $response.ContentType = "application/json" }
                ".svg"  { $response.ContentType = "image/svg+xml" }
                ".png"  { $response.ContentType = "image/png" }
                ".jpg"  { $response.ContentType = "image/jpeg" }
                ".jpeg" { $response.ContentType = "image/jpeg" }
                ".gif"  { $response.ContentType = "image/gif" }
                default { $response.ContentType = "application/octet-stream" }
            }
            
            $response.StatusCode = 200
            $response.ContentLength64 = $fileBytes.Length
            $response.OutputStream.Write($fileBytes, 0, $fileBytes.Length)
        } else {
            # Arquivo não encontrado
            $response.StatusCode = 404
            $errorMessage = "404 - Arquivo não encontrado: $localPath"
            $errorBytes = [System.Text.Encoding]::UTF8.GetBytes($errorMessage)
            $response.ContentType = "text/plain; charset=utf-8"
            $response.ContentLength64 = $errorBytes.Length
            $response.OutputStream.Write($errorBytes, 0, $errorBytes.Length)
        }
        
        $response.OutputStream.Close()
    }
} catch {
    Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    $listener.Stop()
    Write-Host "Servidor parado."
} 