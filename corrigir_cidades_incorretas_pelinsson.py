#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cidades incorretas do representante Pelinsson:
- Remover APARECIDA DO TABOADO (é do MS, não MT)
- Corrigir NOVA CANAA para NOVA CANAA DO NORTE

Autor: Assistente AI
"""

import json
import shutil
from datetime import datetime

def fazer_backup(arquivo):
    """Faz backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_cidades_incorretas():
    """Corrige as cidades incorretas do Pelinsson"""
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção de Cidades Incorretas - Pelinsson ===")
    print()
    
    # Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # Carregar arquivo
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encontrar Pelinsson
    pelinsson_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '33.0':
            pelinsson_key = key
            break
    
    if not pelinsson_key:
        print("ERRO: Pelinsson não encontrado!")
        return False
    
    # Cidades atuais
    cidades_atuais = data['representantes'][pelinsson_key]['estados']['MT']['cidades']
    print(f"Cidades atuais: {len(cidades_atuais)}")
    
    # Correções a fazer
    cidades_corrigidas = []
    
    for cidade in cidades_atuais:
        if cidade == "APARECIDA DO TABOADO":
            print(f"  ❌ Removendo: {cidade} (é do MS, não MT)")
            # Não adiciona à lista corrigida
        elif cidade == "NOVA CANAA":
            print(f"  ✏️  Corrigindo: {cidade} → NOVA CANAA DO NORTE")
            cidades_corrigidas.append("NOVA CANAA DO NORTE")
        else:
            cidades_corrigidas.append(cidade)
    
    # Ordenar lista final
    cidades_corrigidas.sort()
    
    print()
    print(f"Cidades após correção: {len(cidades_corrigidas)}")
    
    # Atualizar dados
    data['representantes'][pelinsson_key]['estados']['MT']['cidades'] = cidades_corrigidas
    data['representantes'][pelinsson_key]['estados']['MT']['total_cidades'] = len(cidades_corrigidas)
    data['representantes'][pelinsson_key]['total_cidades'] = len(cidades_corrigidas)
    
    # Salvar arquivo
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][pelinsson_key]['nome']}")
    print(f"Estado: MT")
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