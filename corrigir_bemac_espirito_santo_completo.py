#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir e adicionar TODAS as cidades do Espírito Santo (ES)
para o representante BEMAC Representações (ID 44.0).

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

def carregar_cidades_es():
    """
    Carrega todas as cidades do Espírito Santo do arquivo municipios.json
    """
    print("Carregando todas as cidades do Espírito Santo...")
    
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    es_cities = []
    for feature in data['features']:
        if feature['properties']['UF'] == 'ES':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            es_cities.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    es_cities = sorted(list(set(es_cities)))
    
    print(f"Total de cidades encontradas no ES: {len(es_cities)}")
    return es_cities

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_bemac_es_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_bemac_es():
    """
    Função principal para adicionar todas as cidades faltantes do ES ao representante BEMAC
    """
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção BEMAC ES - Todas as Cidades ===")
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # 2. Carregar todas as cidades do ES
    todas_cidades_es = carregar_cidades_es()
    
    # 3. Carregar arquivo de representantes
    print("Carregando arquivo de representantes...")
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 4. Encontrar o representante BEMAC
    bemac_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '44.0':
            bemac_key = key
            break
    
    if not bemac_key:
        print("ERRO: Representante BEMAC (código 44.0) não encontrado!")
        return False
    
    print(f"Representante encontrado: {data['representantes'][bemac_key]['nome']}")
    
    # 5. Verificar cidades atuais
    cidades_atuais = data['representantes'][bemac_key]['estados']['ES']['cidades']
    cidades_atuais_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_atuais]
    
    print(f"Cidades atuais do BEMAC: {len(cidades_atuais)}")
    print(f"Total de cidades no ES: {len(todas_cidades_es)}")
    
    # 6. Identificar cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_es:
        if cidade not in cidades_atuais_normalized:
            cidades_faltantes.append(cidade)
    
    print(f"Cidades faltantes: {len(cidades_faltantes)}")
    
    if len(cidades_faltantes) == 0:
        print("BEMAC já atende todas as cidades do ES!")
        return True
    
    # 7. Mostrar relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    print()
    print("Cidades atuais do BEMAC:")
    for i, cidade in enumerate(sorted(cidades_atuais_normalized), 1):
        print(f"  {i:3d}. {cidade}")
    
    print()
    print("Cidades faltantes a serem adicionadas:")
    for i, cidade in enumerate(sorted(cidades_faltantes), 1):
        print(f"  {i:3d}. {cidade}")
    
    # 8. Confirmar alteração
    print()
    resposta = input(f"Confirma a adição de {len(cidades_faltantes)} cidades faltantes do Espírito Santo? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # 9. Atualizar lista de cidades
    todas_cidades_es_final = sorted(list(set(cidades_atuais_normalized + cidades_faltantes)))
    
    # 10. Atualizar dados do representante
    data['representantes'][bemac_key]['estados']['ES']['cidades'] = todas_cidades_es_final
    data['representantes'][bemac_key]['estados']['ES']['total_cidades'] = len(todas_cidades_es_final)
    data['representantes'][bemac_key]['total_cidades'] = len(todas_cidades_es_final)
    
    # 11. Salvar arquivo atualizado
    print()
    print("Salvando arquivo atualizado...")
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 12. Relatório final
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {data['representantes'][bemac_key]['nome']}")
    print(f"Código: {data['representantes'][bemac_key]['codigo']}")
    print(f"Estado: ES (Espírito Santo)")
    print(f"Cidades antes: {len(cidades_atuais)}")
    print(f"Cidades adicionadas: {len(cidades_faltantes)}")
    print(f"Total final: {len(todas_cidades_es_final)}")
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup salvo em: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = corrigir_bemac_es()
        if sucesso:
            print()
            print("Script executado com sucesso!")
        else:
            print()
            print("Script finalizado com problemas.")
    except Exception as e:
        print(f"ERRO durante a execução: {e}")
        print("Verifique os arquivos e tente novamente.")