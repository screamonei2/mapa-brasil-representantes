#!/bin/bash

# Busca os IDs de todas as mesorregiões de SP direto da API
meso_ids=($(curl -s "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/mesorregioes" | jq -r '.[].id'))

echo "["

for i in "${!meso_ids[@]}"; do
  id=${meso_ids[$i]}

  # Nome da mesorregião
  nome_meso=$(curl -s "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes/$id" | jq -r '.nome')

  # Lista de municípios
  municipios=$(curl -s "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes/$id/municipios" | jq -c '[.[].nome]')

  # Se for o último elemento, não coloca vírgula
  if [ $i -lt $((${#meso_ids[@]} - 1)) ]; then
    echo "  {\"mesorregiao\": \"$nome_meso\", \"municipios\": $municipios},"
  else
    echo "  {\"mesorregiao\": \"$nome_meso\", \"municipios\": $municipios}"
  fi
done

echo "]"
