# Script PowerShell para corrigir representante Lugus
Write-Host "=== CORREÇÃO DO REPRESENTANTE LUGUS (53.02) ===" -ForegroundColor Yellow
Write-Host "Carregando dados do arquivo JSON..." -ForegroundColor Cyan

try {
    # Ler o arquivo JSON
    $jsonContent = Get-Content -Path "old\representantes.json" -Raw -Encoding UTF8
    $data = $jsonContent | ConvertFrom-Json
    
    Write-Host "✓ Arquivo carregado com sucesso" -ForegroundColor Green
    
    # Lista completa dos 62 municípios do Amazonas
    $municipiosAmazonas = @(
        "ALVARÃES", "AMATURÁ", "ANAMÃ", "ANORI", "APUÍ", "ATALAIA DO NORTE",
        "AUTAZES", "BARCELOS", "BARREIRINHA", "BENJAMIN CONSTANT", "BERURI",
        "BOA VISTA DO RAMOS", "BOCA DO ACRE", "BORBA", "CAAPIRANGA", "CANUTAMA",
        "CARAUARI", "CAREIRO", "CAREIRO DA VÁRZEA", "COARI", "CODAJÁS",
        "EIRUNEPÉ", "ENVIRA", "FONTE BOA", "GUAJARÁ", "HUMAITÁ", "IPIXUNA",
        "IRANDUBA", "ITACOATIARA", "ITAMARATI", "ITAPIRANGA", "JAPURÁ",
        "JURUÁ", "JUTAÍ", "LÁBREA", "MANACAPURU", "MANAQUIRI", "MANAUS",
        "MANICORÉ", "MARAÃ", "MAUÉS", "NHAMUNDÁ", "NOVA OLINDA DO NORTE",
        "NOVO AIRÃO", "NOVO ARIPUANÃ", "PARINTINS", "PAUINI", "PRESIDENTE FIGUEIREDO",
        "RIO PRETO DA EVA", "SANTA ISABEL DO RIO NEGRO", "SANTO ANTÔNIO DO IÇÁ",
        "SÃO GABRIEL DA CACHOEIRA", "SÃO PAULO DE OLIVENÇA", "SÃO SEBASTIÃO DO UATUMÃ",
        "SILVES", "TABATINGA", "TAPAUÁ", "TEFÉ", "TONANTINS", "UARINI",
        "URUCARÁ", "URUCURITUBA"
    )
    
    Write-Host "✓ Lista de municípios do Amazonas carregada: $($municipiosAmazonas.Count) municípios" -ForegroundColor Green
    
    # Encontrar o representante Lugus
    $lugusEncontrado = $false
    $lugusKey = $null
    
    foreach ($key in $data.representantes.PSObject.Properties.Name) {
        $rep = $data.representantes.$key
        if ($key -like "*lugus*" -or $rep.codigo -eq "53.02") {
            $lugusKey = $key
            $lugusEncontrado = $true
            Write-Host "✓ Representante encontrado: $($rep.nome)" -ForegroundColor Green
            Write-Host "  Código: $($rep.codigo)" -ForegroundColor White
            Write-Host "  Cidades antes: $($rep.cidades.Count)" -ForegroundColor White
            break
        }
    }
    
    if (-not $lugusEncontrado) {
        Write-Host "❌ Representante Lugus não encontrado!" -ForegroundColor Red
        exit 1
    }
    
    # Atualizar dados do Lugus
    $data.representantes.$lugusKey.cidades = $municipiosAmazonas
    $data.representantes.$lugusKey.total_cidades = $municipiosAmazonas.Count
    $data.representantes.$lugusKey.estados = @("AM")
    $data.representantes.$lugusKey.estados_atendidos = @("AM")
    
    Write-Host "✓ Dados do representante atualizados" -ForegroundColor Green
    Write-Host "  Cidades depois: $($municipiosAmazonas.Count)" -ForegroundColor White
    
    # Atualizar mapeamento de cidades
    $cidadesRemovidas = 0
    $mapeamentoKeys = @($data.mapeamento_cidades.PSObject.Properties.Name)
    
    foreach ($cidade in $mapeamentoKeys) {
        if ($data.mapeamento_cidades.$cidade -eq "LUGUS REPRESENTACAO LTDA") {
            $data.mapeamento_cidades.PSObject.Properties.Remove($cidade)
            $cidadesRemovidas++
        }
    }
    
    # Adicionar novos mapeamentos
    foreach ($cidade in $municipiosAmazonas) {
        $cidadeLower = $cidade.ToLower()
        $data.mapeamento_cidades | Add-Member -MemberType NoteProperty -Name $cidadeLower -Value "LUGUS REPRESENTACAO LTDA" -Force
    }
    
    Write-Host "✓ Removidos $cidadesRemovidas mapeamentos antigos" -ForegroundColor Green
    Write-Host "✓ Adicionados $($municipiosAmazonas.Count) novos mapeamentos" -ForegroundColor Green
    
    # Salvar arquivo atualizado
    $jsonOutput = $data | ConvertTo-Json -Depth 10 -Compress:$false
    $jsonOutput | Out-File -FilePath "old\representantes.json" -Encoding UTF8
    
    Write-Host "" 
    Write-Host "✅ LUGUS CORRIGIDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "✓ Agora atende TODO o estado do Amazonas (AM)" -ForegroundColor Green
    Write-Host "✓ Total de municípios: $($municipiosAmazonas.Count)" -ForegroundColor Green
    Write-Host "✓ Estados: apenas AM" -ForegroundColor Green
    Write-Host "✓ Inclui cidades importantes: MANAUS, PARINTINS, ITACOATIARA, COARI, TABATINGA" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Erro ao processar: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}