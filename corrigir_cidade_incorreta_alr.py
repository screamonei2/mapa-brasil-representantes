#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cidade incorreta do representante ALR:
- Verificar e corrigir TAMBAUZINHO

Autor: Assistente AI
"""

import json
import shutil
from datetime import datetime

def fazer_backup(arquivo):
    """Faz backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_alr_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_cidade_incorreta():
    """Corrige a cidade incorreta do ALR"""
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção de Cidade Incorreta - ALR ===")
    print()
    
    # Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # Carregar arquivo
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encontrar ALR
    alr_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '19.0':
            alr_key = key
            break
    
    if not alr_key:
        print("ERRO: ALR não encontrado!")
        return False
    
    # Cidades atuais
    cidades_atuais = data['representantes'][alr_key]['estados']['PB']['cidades']
    print(f"Cidades atuais: {len(cidades_atuais)}")
    
    # Verificar se TAMBAUZINHO existe
    if 'TAMBAUZINHO' in cidades_atuais:
        print("Encontrou TAMBAUZINHO na lista")
        
        # Buscar se existe uma cidade similar no arquivo oficial
        resposta = input("TAMBAUZINHO não existe na PB. Remover? (s/N): ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            # Remover TAMBAUZINHO
            cidades_corrigidas = [cidade for cidade in cidades_atuais if cidade != 'TAMBAUZINHO']
            print(f"  ❌ Removendo: TAMBAUZINHO (não existe na PB)")
        else:
            print("Operação cancelada")
            return False
    else:
        print("TAMBAUZINHO não encontrado na lista")
        return False
    
    print()
    print(f"Cidades após correção: {len(cidades_corrigidas)}")
    
    # Atualizar dados
    data['representantes'][alr_key]['estados']['PB']['cidades'] = cidades_corrigidas
    data['representantes'][alr_key]['estados']['PB']['total_cidades'] = len(cidades_corrigidas)
    data['representantes'][alr_key]['total_cidades'] = len(cidades_corrigidas)
    
    # Salvar arquivo
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][alr_key]['nome']}")
    print(f"Estado: PB")
    print(f"Total final de cidades: {len(cidades_corrigidas)}")
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = corrigir_cidade_incorreta()
        if sucesso:
            print("\n✅ Correção executada com sucesso!")
        else:
            print("\n❌ Erro na correção.")
    except Exception as e:
        print(f"ERRO: {e}")