#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar divisão regional específica do Rio de Janeiro (RJ):
- Representante 52.0 (MRB): Capital Rio de Janeiro (já configurado)
- Representante 52.01 (L323): Resto do estado (172 cidades restantes)

Autor: Assistente AI
Data: $(date +%Y-%m-%d)
"""

import json
import shutil
from datetime import datetime
import unicodedata
import re

def normalizar_nome_cidade(nome):
    """
    Normaliza nomes de cidades removendo acentos e caracteres especiais
    """
    # Remove acentos
    nome = unicodedata.normalize('NFD', nome)
    nome = ''.join(char for char in nome if unicodedata.category(char) != 'Mn')
    
    # Converte para maiúscula
    nome = nome.upper()
    
    # Remove caracteres especiais extras, mantendo apenas letras, números e espaços/hifens
    nome = re.sub(r'[^A-Z0-9\s\-\']', '', nome)
    
    # Remove espaços extras
    nome = ' '.join(nome.split())
    
    return nome

def carregar_cidades_rj():
    """
    Carrega todas as cidades do Rio de Janeiro do arquivo municipios.json
    """
    print("Carregando todas as cidades do Rio de Janeiro...")
    
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    rj_cities = []
    for feature in data['features']:
        if feature['properties']['UF'] == 'RJ':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            rj_cities.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    rj_cities = sorted(list(set(rj_cities)))
    
    print(f"Total de cidades encontradas no RJ: {len(rj_cities)}")
    return rj_cities

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_divisao_rj_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def configurar_divisao_rj():
    """
    Função principal para configurar a divisão regional do RJ
    """
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Configuração Divisão Regional RJ ===")
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # 2. Carregar todas as cidades do RJ
    todas_cidades_rj = carregar_cidades_rj()
    
    # 3. Definir cidade da capital (representante 52.0)
    capital_rj = ['RIO DE JANEIRO']
    
    # 4. Calcular cidades restantes para representante 52.01
    cidades_resto_rj = []
    for cidade in todas_cidades_rj:
        if cidade not in capital_rj:
            cidades_resto_rj.append(cidade)
    
    cidades_resto_rj = sorted(cidades_resto_rj)
    
    print(f"Divisão planejada:")
    print(f"  Representante 52.0 (MRB): {len(capital_rj)} cidade (capital)")
    print(f"  Representante 52.01 (L323): {len(cidades_resto_rj)} cidades (resto do estado)")
    print(f"  Total: {len(capital_rj) + len(cidades_resto_rj)} cidades")
    print(f"  Verificação: RJ tem {len(todas_cidades_rj)} cidades")
    
    if len(capital_rj) + len(cidades_resto_rj) != len(todas_cidades_rj):
        print("ERRO: A soma não confere com o total de cidades do RJ!")
        return False
    
    # 5. Carregar arquivo de representantes
    print()
    print("Carregando arquivo de representantes...")
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 6. Encontrar os representantes
    rep52_key = None
    rep521_key = None
    
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '52.0':
            rep52_key = key
        elif rep.get('codigo') == '52.01':
            rep521_key = key
    
    if not rep52_key:
        print("ERRO: Representante 52.0 (MRB) não encontrado!")
        return False
    
    if not rep521_key:
        print("ERRO: Representante 52.01 (L323) não encontrado!")
        return False
    
    print(f"Representante 52.0 encontrado: {data['representantes'][rep52_key]['nome']}")
    print(f"Representante 52.01 encontrado: {data['representantes'][rep521_key]['nome']}")
    
    # 7. Verificar configuração atual
    cidades_atuais_52 = data['representantes'][rep52_key]['estados']['RJ']['cidades']
    cidades_atuais_521 = data['representantes'][rep521_key]['estados']['RJ']['cidades']
    
    print()
    print("=== SITUAÇÃO ATUAL ===")
    print(f"MRB (52.0) - Cidades atuais: {len(cidades_atuais_52)} - {cidades_atuais_52}")
    print(f"L323 (52.01) - Cidades atuais: {len(cidades_atuais_521)}")
    
    # 8. Mostrar relatório detalhado
    print()
    print("=== CONFIGURAÇÃO FINAL ===")
    print()
    print(f"MRB (52.0) - Capital ({len(capital_rj)} cidade):")
    for i, cidade in enumerate(capital_rj, 1):
        print(f"  {i}. {cidade}")
    
    print()
    print(f"Primeiras 30 cidades para L323 (52.01) ({len(cidades_resto_rj)} cidades):")
    for i, cidade in enumerate(cidades_resto_rj[:30], 1):
        print(f"  {i:3d}. {cidade}")
    
    if len(cidades_resto_rj) > 30:
        print(f"  ... e mais {len(cidades_resto_rj) - 30} cidades")
    
    # 9. Confirmar alteração
    print()
    resposta = input(f"Confirma a divisão regional do RJ conforme especificado? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # 10. Atualizar dados dos representantes
    
    # Manter representante 52.0 (MRB) com apenas Rio de Janeiro
    data['representantes'][rep52_key]['estados']['RJ']['cidades'] = capital_rj
    data['representantes'][rep52_key]['estados']['RJ']['total_cidades'] = len(capital_rj)
    data['representantes'][rep52_key]['total_cidades'] = len(capital_rj)
    
    # Configurar representante 52.01 (L323) com resto do estado
    data['representantes'][rep521_key]['estados']['RJ']['cidades'] = cidades_resto_rj
    data['representantes'][rep521_key]['estados']['RJ']['total_cidades'] = len(cidades_resto_rj)
    data['representantes'][rep521_key]['total_cidades'] = len(cidades_resto_rj)
    
    # 11. Salvar arquivo atualizado
    print()
    print("Salvando arquivo atualizado...")
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 12. Relatório final
    print()
    print("=== DIVISÃO REGIONAL CONCLUÍDA ===")
    print(f"Estado: RJ (Rio de Janeiro)")
    print(f"Total de cidades: {len(todas_cidades_rj)}")
    print()
    print(f"Representante 52.0 (MRB):")
    print(f"  Nome: {data['representantes'][rep52_key]['nome']}")
    print(f"  Cidades: {len(capital_rj)} (capital)")
    print()
    print(f"Representante 52.01 (L323):")
    print(f"  Nome: {data['representantes'][rep521_key]['nome']}")
    print(f"  Cidades: {len(cidades_resto_rj)} (resto do estado)")
    print()
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup salvo em: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = configurar_divisao_rj()
        if sucesso:
            print()
            print("Script executado com sucesso!")
        else:
            print()
            print("Script finalizado com problemas.")
    except Exception as e:
        print(f"ERRO durante a execução: {e}")
        print("Verifique os arquivos e tente novamente.")