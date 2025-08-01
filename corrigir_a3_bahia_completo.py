#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir e adicionar TODAS as cidades da Bahia (BA)
para o representante A3 Consultoria (ID 51.0).

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

def carregar_cidades_ba():
    """
    Carrega todas as cidades da Bahia do arquivo municipios.json
    """
    print("Carregando todas as cidades da Bahia...")
    
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    ba_cities = []
    for feature in data['features']:
        if feature['properties']['UF'] == 'BA':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            ba_cities.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    ba_cities = sorted(list(set(ba_cities)))
    
    print(f"Total de cidades encontradas na BA: {len(ba_cities)}")
    return ba_cities

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_a3_ba_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_a3_ba():
    """
    Função principal para adicionar todas as cidades faltantes da BA ao representante A3
    """
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção A3 BA - Todas as Cidades ===")
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # 2. Carregar todas as cidades da BA
    todas_cidades_ba = carregar_cidades_ba()
    
    # 3. Carregar arquivo de representantes
    print("Carregando arquivo de representantes...")
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 4. Encontrar o representante A3
    a3_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '51.0':
            a3_key = key
            break
    
    if not a3_key:
        print("ERRO: Representante A3 (código 51.0) não encontrado!")
        return False
    
    print(f"Representante encontrado: {data['representantes'][a3_key]['nome']}")
    
    # 5. Verificar cidades atuais
    cidades_atuais = data['representantes'][a3_key]['estados']['BA']['cidades']
    cidades_atuais_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_atuais]
    
    print(f"Cidades atuais do A3: {len(cidades_atuais)}")
    print(f"Total de cidades na BA: {len(todas_cidades_ba)}")
    
    # 6. Identificar cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_ba:
        if cidade not in cidades_atuais_normalized:
            cidades_faltantes.append(cidade)
    
    print(f"Cidades faltantes: {len(cidades_faltantes)}")
    
    if len(cidades_faltantes) == 0:
        print("A3 já atende todas as cidades da BA!")
        return True
    
    # 7. Mostrar relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    print()
    print("Primeiras 20 cidades atuais do A3:")
    for i, cidade in enumerate(sorted(cidades_atuais_normalized)[:20], 1):
        print(f"  {i:3d}. {cidade}")
    
    if len(cidades_atuais_normalized) > 20:
        print(f"  ... e mais {len(cidades_atuais_normalized) - 20} cidades")
    
    print()
    print("Primeiras 30 cidades faltantes a serem adicionadas:")
    for i, cidade in enumerate(sorted(cidades_faltantes)[:30], 1):
        print(f"  {i:3d}. {cidade}")
    
    if len(cidades_faltantes) > 30:
        print(f"  ... e mais {len(cidades_faltantes) - 30} cidades")
    
    # 8. Confirmar alteração
    print()
    resposta = input(f"Confirma a adição de {len(cidades_faltantes)} cidades faltantes da Bahia? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # 9. Atualizar lista de cidades
    todas_cidades_ba_final = sorted(list(set(cidades_atuais_normalized + cidades_faltantes)))
    
    # 10. Atualizar dados do representante
    data['representantes'][a3_key]['estados']['BA']['cidades'] = todas_cidades_ba_final
    data['representantes'][a3_key]['estados']['BA']['total_cidades'] = len(todas_cidades_ba_final)
    data['representantes'][a3_key]['total_cidades'] = len(todas_cidades_ba_final)
    
    # 11. Salvar arquivo atualizado
    print()
    print("Salvando arquivo atualizado...")
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 12. Relatório final
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][a3_key]['nome']}")
    print(f"Código: {data['representantes'][a3_key]['codigo']}")
    print(f"Estado: BA (Bahia)")
    print(f"Cidades antes: {len(cidades_atuais)}")
    print(f"Cidades adicionadas: {len(cidades_faltantes)}")
    print(f"Total final: {len(todas_cidades_ba_final)}")
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup salvo em: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = corrigir_a3_ba()
        if sucesso:
            print()
            print("Script executado com sucesso!")
        else:
            print()
            print("Script finalizado com problemas.")
    except Exception as e:
        print(f"ERRO durante a execução: {e}")
        print("Verifique os arquivos e tente novamente.")