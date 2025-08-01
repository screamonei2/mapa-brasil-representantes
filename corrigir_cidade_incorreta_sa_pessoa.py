#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir cidade incorreta do representante SA & Pessoa:
- Corrigir BATAIPORA para BATAYPORA

Autor: Assistente AI
"""

import json
import shutil
from datetime import datetime

def fazer_backup(arquivo):
    """Faz backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_sa_pessoa_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_cidade_incorreta():
    """Corrige a cidade incorreta do SA & Pessoa"""
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção de Cidade Incorreta - SA & Pessoa ===")
    print()
    
    # Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # Carregar arquivo
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encontrar SA & Pessoa
    sa_pessoa_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '34.0':
            sa_pessoa_key = key
            break
    
    if not sa_pessoa_key:
        print("ERRO: SA & Pessoa não encontrado!")
        return False
    
    # Cidades atuais
    cidades_atuais = data['representantes'][sa_pessoa_key]['estados']['MS']['cidades']
    print(f"Cidades atuais: {len(cidades_atuais)}")
    
    # Aplicar correções
    cidades_corrigidas = []
    correções_feitas = []
    
    for cidade in cidades_atuais:
        if cidade == 'BATAIPORA':
            # Corrigir para a grafia oficial
            cidades_corrigidas.append('BATAYPORA')
            correções_feitas.append("✏️  Corrigindo: BATAIPORA → BATAYPORA")
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
    data['representantes'][sa_pessoa_key]['estados']['MS']['cidades'] = cidades_corrigidas
    data['representantes'][sa_pessoa_key]['estados']['MS']['total_cidades'] = len(cidades_corrigidas)
    data['representantes'][sa_pessoa_key]['total_cidades'] = len(cidades_corrigidas)
    
    # Salvar arquivo
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][sa_pessoa_key]['nome']}")
    print(f"Estado: MS")
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