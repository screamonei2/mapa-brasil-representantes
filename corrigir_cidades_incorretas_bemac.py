#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cidades incorretas do representante BEMAC:
- Remover ITAOCA (pertence ao RJ)
- Corrigir SAO ROQUE DO CANNAA para SAO ROQUE DO CANAA
- Remover TIMBUI (não existe)
- Remover VINHATICO (não existe)

Autor: Assistente AI
"""

import json
import shutil
from datetime import datetime

def fazer_backup(arquivo):
    """Faz backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_bemac_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_cidades_incorretas():
    """Corrige as cidades incorretas do BEMAC"""
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção de Cidades Incorretas - BEMAC ===")
    print()
    
    # Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # Carregar arquivo
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encontrar BEMAC
    bemac_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '44.0':
            bemac_key = key
            break
    
    if not bemac_key:
        print("ERRO: BEMAC não encontrado!")
        return False
    
    # Cidades atuais
    cidades_atuais = data['representantes'][bemac_key]['estados']['ES']['cidades']
    print(f"Cidades atuais: {len(cidades_atuais)}")
    
    # Aplicar correções
    cidades_corrigidas = []
    correções_feitas = []
    
    for cidade in cidades_atuais:
        if cidade == 'ITAOCA':
            # Remover - pertence ao RJ (ITAOCARA)
            correções_feitas.append("❌ Removendo: ITAOCA (pertence ao RJ)")
        elif cidade == 'SAO ROQUE DO CANNAA':
            # Corrigir grafia
            cidades_corrigidas.append('SAO ROQUE DO CANAA')
            correções_feitas.append("✏️  Corrigindo: SAO ROQUE DO CANNAA → SAO ROQUE DO CANAA")
        elif cidade == 'TIMBUI':
            # Remover - não existe
            correções_feitas.append("❌ Removendo: TIMBUI (não existe)")
        elif cidade == 'VINHATICO':
            # Remover - não existe
            correções_feitas.append("❌ Removendo: VINHATICO (não existe)")
        else:
            # Manter a cidade
            cidades_corrigidas.append(cidade)
    
    print()
    print("Correções aplicadas:")
    for correcao in correções_feitas:
        print(f"  {correcao}")
    
    print()
    print(f"Cidades após correção: {len(cidades_corrigidas)}")
    
    # Confirmar alteração
    resposta = input("Confirma as correções? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # Atualizar dados
    data['representantes'][bemac_key]['estados']['ES']['cidades'] = cidades_corrigidas
    data['representantes'][bemac_key]['estados']['ES']['total_cidades'] = len(cidades_corrigidas)
    data['representantes'][bemac_key]['total_cidades'] = len(cidades_corrigidas)
    
    # Salvar arquivo
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][bemac_key]['nome']}")
    print(f"Estado: ES")
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