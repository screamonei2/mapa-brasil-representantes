# Script simples para corrigir Lugus
Write-Host "Corrigindo representante Lugus..."

# Backup do arquivo original
Copy-Item "old\representantes.json" "old\representantes_backup.json"
Write-Host "Backup criado: representantes_backup.json"

# Ler arquivo
$content = Get-Content "old\representantes.json" -Raw

# Lista de cidades do Amazonas
$novasCidades = '"ALVARÃES","AMATURÁ","ANAMÃ","ANORI","APUÍ","ATALAIA DO NORTE","AUTAZES","BARCELOS","BARREIRINHA","BENJAMIN CONSTANT","BERURI","BOA VISTA DO RAMOS","BOCA DO ACRE","BORBA","CAAPIRANGA","CANUTAMA","CARAUARI","CAREIRO","CAREIRO DA VÁRZEA","COARI","CODAJÁS","EIRUNEPÉ","ENVIRA","FONTE BOA","GUAJARÁ","HUMAITÁ","IPIXUNA","IRANDUBA","ITACOATIARA","ITAMARATI","ITAPIRANGA","JAPURÁ","JURUÁ","JUTAÍ","LÁBREA","MANACAPURU","MANAQUIRI","MANAUS","MANICORÉ","MARAÃ","MAUÉS","NHAMUNDÁ","NOVA OLINDA DO NORTE","NOVO AIRÃO","NOVO ARIPUANÃ","PARINTINS","PAUINI","PRESIDENTE FIGUEIREDO","RIO PRETO DA EVA","SANTA ISABEL DO RIO NEGRO","SANTO ANTÔNIO DO IÇÁ","SÃO GABRIEL DA CACHOEIRA","SÃO PAULO DE OLIVENÇA","SÃO SEBASTIÃO DO UATUMÃ","SILVES","TABATINGA","TAPAUÁ","TEFÉ","TONANTINS","UARINI","URUCARÁ","URUCURITUBA"'

# Substituir as cidades do Lugus
$pattern = '("lugus representacao ltda":[^}]*"cidades":\s*)\[[^\]]*\]'
$replacement = "`$1[$novasCidades]"
$content = $content -replace $pattern, $replacement

# Atualizar total_cidades para 62
$pattern2 = '("lugus representacao ltda":[^}]*"total_cidades":\s*)\d+'
$replacement2 = '$1 62'
$content = $content -replace $pattern2, $replacement2

# Salvar arquivo
$content | Out-File "old\representantes.json" -Encoding UTF8

Write-Host "Lugus corrigido com sucesso!"
Write-Host "- Agora atende todos os 62 municipios do Amazonas"
Write-Host "- Estados: apenas AM"
Write-Host "- Arquivo salvo em: old\representantes.json"