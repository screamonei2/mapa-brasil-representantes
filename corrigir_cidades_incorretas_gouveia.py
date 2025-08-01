#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cidades incorretas do representante A.Gouveia:
- Corrigir nomes de cidades que estão errados ou com grafias diferentes

Autor: Assistente AI
"""

import json
import shutil
from datetime import datetime

def fazer_backup(arquivo):
    """Faz backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_gouveia_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_cidades_incorretas():
    """Corrige as cidades incorretas do A.Gouveia"""
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção de Cidades Incorretas - A.Gouveia ===")
    print()
    
    # Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # Carregar arquivo
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encontrar A.Gouveia
    gouveia_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '17.0':
            gouveia_key = key
            break
    
    if not gouveia_key:
        print("ERRO: A.Gouveia não encontrado!")
        return False
    
    # Cidades atuais
    cidades_atuais = data['representantes'][gouveia_key]['estados']['PE']['cidades']
    print(f"Cidades atuais: {len(cidades_atuais)}")
    
    # Correções a fazer baseadas na investigação
    cidades_corrigidas = []
    
    for cidade in cidades_atuais:
        if cidade == "CABO":
            # CABO deve ser CABO DE SANTO AGOSTINHO (que já existe)
            print(f"  ❌ Removendo: {cidade} (duplicata de CABO DE SANTO AGOSTINHO)")
            # Não adiciona à lista corrigida
        elif cidade == "GOIANIA":
            print(f"  ❌ Removendo: {cidade} (é capital de Goiás, não PE)")
            # Não adiciona à lista corrigida
        elif cidade == "SANTO AGOSTINHO":
            print(f"  ❌ Removendo: {cidade} (duplicata de CABO DE SANTO AGOSTINHO)")
            # Não adiciona à lista corrigida
        elif cidade == "SAO CAETANO DO NAVIO":
            print(f"  ❌ Removendo: {cidade} (não existe no PE)")
            # Não adiciona à lista corrigida
        else:
            cidades_corrigidas.append(cidade)
    
    # Ordenar lista final
    cidades_corrigidas.sort()
    
    print()
    print(f"Cidades após correção: {len(cidades_corrigidas)}")
    
    # Atualizar dados
    data['representantes'][gouveia_key]['estados']['PE']['cidades'] = cidades_corrigidas
    data['representantes'][gouveia_key]['estados']['PE']['total_cidades'] = len(cidades_corrigidas)
    data['representantes'][gouveia_key]['total_cidades'] = len(cidades_corrigidas)
    
    # Salvar arquivo
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][gouveia_key]['nome']}")
    print(f"Estado: PE")
    print(f"Total final de cidades: {len(cidades_corrigidas)}")
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = corrigir_cidades_incorretas()
        if sucesso:
            print("\n✅ Correção executada com sucesso!")
        else:
            print("\n❌ Erro na correção.")
    except Exception as e:
        print(f"ERRO: {e}")