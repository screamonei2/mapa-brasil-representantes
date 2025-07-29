# Script PowerShell para corrigir caracteres especiais deformados
Write-Host "=== CORREÇÃO DE CODIFICAÇÃO UTF-8 ===" -ForegroundColor Green

try {
    # Ler o arquivo
    $filePath = "old\representantes.json"
    $content = Get-Content -Path $filePath -Raw -Encoding UTF8
    
    Write-Host "Arquivo original: $($content.Length) caracteres" -ForegroundColor Yellow
    
    # Fazer backup
    $backupPath = "old\representantes_backup_codificacao.json"
    Copy-Item -Path $filePath -Destination $backupPath -Force
    Write-Host "Backup criado: $backupPath" -ForegroundColor Cyan
    
    # Aplicar correções básicas
    $contentCorrigido = $content
    $totalCorrecoes = 0
    
    # Correções principais para REPRESENTAÇÕES e REPRESENTAÇÃO
    if ($contentCorrigido -match "REPRESENTAÃ") {
        $count1 = ([regex]::Matches($contentCorrigido, "REPRESENTAÃ\\u0087Ã\\u0095ES")).Count
        $contentCorrigido = $contentCorrigido -replace "REPRESENTAÃ\\u0087Ã\\u0095ES", "REPRESENTAÇÕES"
        $totalCorrecoes += $count1
        Write-Host "✓ Corrigido REPRESENTAÇÕES ($count1 ocorrências)" -ForegroundColor Green
        
        $count2 = ([regex]::Matches($contentCorrigido, "REPRESENTAÃ\\u0087Ã\\u0083O")).Count
        $contentCorrigido = $contentCorrigido -replace "REPRESENTAÃ\\u0087Ã\\u0083O", "REPRESENTAÇÃO"
        $totalCorrecoes += $count2
        Write-Host "✓ Corrigido REPRESENTAÇÃO ($count2 ocorrências)" -ForegroundColor Green
    }
    
    # Correções para SERVIÇOS
    if ($contentCorrigido -match "SERVIÃ") {
        $count3 = ([regex]::Matches($contentCorrigido, "SERVIÃ\\u0087OS")).Count
        $contentCorrigido = $contentCorrigido -replace "SERVIÃ\\u0087OS", "SERVIÇOS"
        $totalCorrecoes += $count3
        Write-Host "✓ Corrigido SERVIÇOS ($count3 ocorrências)" -ForegroundColor Green
    }
    
    # Correções de caracteres individuais
    $replacements = @(
        @("Ã\\u0087", "Ç"),
        @("Ã\\u0095", "Õ"),
        @("Ã\\u0089", "É"),
        @("Ã\\u0081", "Á"),
        @("Ã\\u0080", "À"),
        @("Ã\\u0082", "Â"),
        @("Ã\\u0083", "Ã"),
        @("Ã\\u008d", "Í"),
        @("Ã\\u0093", "Ó"),
        @("Ã\\u0094", "Ô"),
        @("Ã\\u009a", "Ú"),
        @("Ã\\u009c", "Ü")
    )
    
    foreach ($replacement in $replacements) {
        $from = $replacement[0]
        $to = $replacement[1]
        if ($contentCorrigido -match [regex]::Escape($from)) {
            $count = ([regex]::Matches($contentCorrigido, [regex]::Escape($from))).Count
            $contentCorrigido = $contentCorrigido -replace [regex]::Escape($from), $to
            $totalCorrecoes += $count
            Write-Host "✓ Corrigido '$from' -> '$to' ($count ocorrências)" -ForegroundColor Green
        }
    }
    
    # Verificar se é JSON válido
    try {
        $jsonData = $contentCorrigido | ConvertFrom-Json
        Write-Host "✓ JSON válido após correções" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Erro de JSON após correções: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Tentando salvar mesmo assim..." -ForegroundColor Yellow
    }
    
    # Salvar arquivo corrigido
    $contentCorrigido | Out-File -FilePath $filePath -Encoding UTF8 -NoNewline
    
    Write-Host "`n✅ CORREÇÃO CONCLUÍDA!" -ForegroundColor Green
    Write-Host "✓ Total de correções aplicadas: $totalCorrecoes" -ForegroundColor Cyan
    Write-Host "✓ Arquivo salvo com codificação UTF-8 correta" -ForegroundColor Cyan
    Write-Host "✓ Caracteres especiais corrigidos" -ForegroundColor Cyan
    Write-Host "✓ Backup salvo em: $backupPath" -ForegroundColor Cyan
    
}
catch {
    Write-Host "❌ Erro ao corrigir codificação: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nCorreção finalizada. Verifique o mapa para confirmar." -ForegroundColor Yellow