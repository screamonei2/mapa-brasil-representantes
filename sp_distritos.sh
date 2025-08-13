#!/bin/bash
# Script: sp_distritos.sh
# Objetivo: pegar todos os distritos de todos os municípios de SP (código estado: 35) usando API do IBGE

echo "{"
curl -s "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios" \
| jq -r '.[] | "\(.id)|\(.nome)"' \
| while IFS="|" read -r id nome; do
    distritos=$(curl -s "https://servicodados.ibge.gov.br/api/v1/localidades/municipios/$id/distritos" \
        | jq -c '[.[].nome]')
    echo "  \"${nome}\": ${distritos}"
done | sed '$!s/$/,/'
echo "}"
