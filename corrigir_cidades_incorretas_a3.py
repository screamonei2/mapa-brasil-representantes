#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cidades incorretas do representante A3:
- Corrigir DIAS D AVILA para DIAS D'AVILA
- Remover HUMILDES (não existe na BA)

Autor: Assistente AI
"""

import json
import shutil
from datetime import datetime

def fazer_backup(arquivo):
    """Faz backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_a3_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_cidades_incorretas():
    """Corrige as cidades incorretas do A3"""
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção de Cidades Incorretas - A3 ===")
    print()
    
    # Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # Carregar arquivo
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encontrar A3
    a3_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '51.0':
            a3_key = key
            break
    
    if not a3_key:
        print("ERRO: A3 não encontrado!")
        return False
    
    # Cidades atuais
    cidades_atuais = data['representantes'][a3_key]['estados']['BA']['cidades']
    print(f"Cidades atuais: {len(cidades_atuais)}")
    
    # Aplicar correções
    cidades_corrigidas = []
    correções_feitas = []
    
    for cidade in cidades_atuais:
        if cidade == 'DIAS D AVILA':
            # Corrigir para a grafia oficial
            cidades_corrigidas.append('DIAS D\'AVILA')
            correções_feitas.append("✏️  Corrigindo: DIAS D AVILA → DIAS D'AVILA")
        elif cidade == 'HUMILDES':
            # Remover - não existe na BA
            correções_feitas.append("❌ Removendo: HUMILDES (não existe na BA)")
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
    data['representantes'][a3_key]['estados']['BA']['cidades'] = cidades_corrigidas
    data['representantes'][a3_key]['estados']['BA']['total_cidades'] = len(cidades_corrigidas)
    data['representantes'][a3_key]['total_cidades'] = len(cidades_corrigidas)
    
    # Salvar arquivo
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][a3_key]['nome']}")
    print(f"Estado: BA")
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