#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cidades incorretas do representante Central Representações:
- Remover CORREGO RICO (não existe)
- Remover VALPARAISO (duplicata incorreta de VALPARAÍSO DE GOIÁS)

Autor: Assistente AI
"""

import json
import shutil
from datetime import datetime

def fazer_backup(arquivo):
    """Faz backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_central_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_cidades_incorretas():
    """Corrige as cidades incorretas da Central Representações"""
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção de Cidades Incorretas - Central Representações ===")
    print()
    
    # Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # Carregar arquivo
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encontrar Central Representações
    central_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '32.0':
            central_key = key
            break
    
    if not central_key:
        print("ERRO: Central Representações não encontrado!")
        return False
    
    # Cidades atuais
    cidades_atuais = data['representantes'][central_key]['estados']['GO']['cidades']
    print(f"Cidades atuais: {len(cidades_atuais)}")
    
    # Aplicar correções
    cidades_corrigidas = []
    correções_feitas = []
    
    for cidade in cidades_atuais:
        if cidade == 'CORREGO RICO':
            # Remover esta cidade (não existe)
            correções_feitas.append("❌ Removendo: CORREGO RICO (cidade inexistente)")
        elif cidade == 'VALPARAISO':
            # Remover esta duplicata incorreta (já existe VALPARAÍSO DE GOIÁS)
            correções_feitas.append("❌ Removendo: VALPARAISO (duplicata de VALPARAÍSO DE GOIÁS)")
        else:
            # Manter a cidade
            cidades_corrigidas.append(cidade)
    
    print()
    if correções_feitas:
        print("Correções aplicadas:")
        for correcao in correções_feitas:
            print(f"  {correcao}")
    else:
        print("Nenhuma correção necessária.")
        return True
    
    print()
    print(f"Cidades após correção: {len(cidades_corrigidas)}")
    
    # Confirmar alteração
    resposta = input("Confirma as correções? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # Atualizar dados
    data['representantes'][central_key]['estados']['GO']['cidades'] = cidades_corrigidas
    data['representantes'][central_key]['estados']['GO']['total_cidades'] = len(cidades_corrigidas)
    data['representantes'][central_key]['total_cidades'] = len(cidades_corrigidas)
    
    # Salvar arquivo
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][central_key]['nome']}")
    print(f"Estado: GO")
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