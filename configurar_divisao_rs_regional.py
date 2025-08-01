#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar divisão regional específica do Rio Grande do Sul (RS):
- Representante 29.01 (ATTEX): Lista específica de 32 cidades (região metropolitana)
- Representante 28.0 (MYRALP): Resto do estado (464 cidades restantes)

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

def carregar_cidades_rs():
    """
    Carrega todas as cidades do Rio Grande do Sul do arquivo municipios.json
    """
    print("Carregando todas as cidades do Rio Grande do Sul...")
    
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    rs_cities = []
    for feature in data['features']:
        if feature['properties']['UF'] == 'RS':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            rs_cities.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    rs_cities = sorted(list(set(rs_cities)))
    
    print(f"Total de cidades encontradas no RS: {len(rs_cities)}")
    return rs_cities

def obter_lista_especifica_rep29():
    """
    Retorna a lista específica de cidades para o representante 29
    """
    cidades_rep29_raw = [
        'Estância Velha', 'Araricá', 'Sapiranga', 'São Leopoldo', 'Esteio', 
        'Dois Irmãos', 'Sapucaia do Sul', 'Campo Bom', 'Cachoeirinha', 'Ivoti', 
        'Nova Hartz', 'Parobé', 'Taquara', 'Rolante', 'Santo Antônio da Patrulha', 
        'Glorinha', 'Gravataí', 'Alvorada', 'Viamão', 'Porto Alegre', 'Canoas', 
        'Nova Santa Rita', 'Portão', 'Capela de Santana', 'Montenegro', 'Triunfo', 
        'Charqueadas', 'Eldorado do Sul', 'Guaíba', 'Arroio dos Ratos', 'São Jerônimo', 
        'Novo Hamburgo'
    ]
    
    # Normalizar a lista
    cidades_rep29_normalized = []
    for cidade in cidades_rep29_raw:
        cidade_norm = normalizar_nome_cidade(cidade)
        cidades_rep29_normalized.append(cidade_norm)
    
    return sorted(cidades_rep29_normalized)

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_divisao_rs_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def configurar_divisao_rs():
    """
    Função principal para configurar a divisão regional do RS
    """
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Configuração Divisão Regional RS ===")
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # 2. Carregar todas as cidades do RS
    todas_cidades_rs = carregar_cidades_rs()
    
    # 3. Obter lista específica para representante 29
    cidades_rep29 = obter_lista_especifica_rep29()
    
    # 4. Calcular cidades restantes para representante 28
    cidades_rep28 = []
    for cidade in todas_cidades_rs:
        if cidade not in cidades_rep29:
            cidades_rep28.append(cidade)
    
    cidades_rep28 = sorted(cidades_rep28)
    
    print(f"Divisão planejada:")
    print(f"  Representante 29.01 (ATTEX): {len(cidades_rep29)} cidades (região específica)")
    print(f"  Representante 28.0 (MYRALP): {len(cidades_rep28)} cidades (resto do estado)")
    print(f"  Total: {len(cidades_rep29) + len(cidades_rep28)} cidades")
    print(f"  Verificação: RS tem {len(todas_cidades_rs)} cidades")
    
    if len(cidades_rep29) + len(cidades_rep28) != len(todas_cidades_rs):
        print("ERRO: A soma não confere com o total de cidades do RS!")
        return False
    
    # 5. Carregar arquivo de representantes
    print()
    print("Carregando arquivo de representantes...")
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 6. Encontrar os representantes
    rep29_key = None
    rep28_key = None
    
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '29.01':
            rep29_key = key
        elif rep.get('codigo') == '28.0':
            rep28_key = key
    
    if not rep29_key:
        print("ERRO: Representante 29.01 (ATTEX) não encontrado!")
        return False
    
    if not rep28_key:
        print("ERRO: Representante 28.0 (MYRALP) não encontrado!")
        return False
    
    print(f"Representante 29.01 encontrado: {data['representantes'][rep29_key]['nome']}")
    print(f"Representante 28.0 encontrado: {data['representantes'][rep28_key]['nome']}")
    
    # 7. Mostrar relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    print()
    print(f"Cidades para representante 29.01 ({len(cidades_rep29)} cidades):")
    for i, cidade in enumerate(cidades_rep29, 1):
        print(f"  {i:2d}. {cidade}")
    
    print()
    print(f"Primeiras 30 cidades para representante 28.0 ({len(cidades_rep28)} cidades):")
    for i, cidade in enumerate(cidades_rep28[:30], 1):
        print(f"  {i:3d}. {cidade}")
    
    if len(cidades_rep28) > 30:
        print(f"  ... e mais {len(cidades_rep28) - 30} cidades")
    
    # 8. Confirmar alteração
    print()
    resposta = input(f"Confirma a divisão regional do RS conforme especificado? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # 9. Atualizar dados dos representantes
    
    # Configurar representante 29.01 (ATTEX)
    if 'RS' not in data['representantes'][rep29_key]['estados']:
        data['representantes'][rep29_key]['estados']['RS'] = {}
        # Adicionar RS aos estados atendidos se não estiver
        if 'RS   ' not in data['representantes'][rep29_key]['estados_atendidos']:
            data['representantes'][rep29_key]['estados_atendidos'].append('RS   ')
    
    data['representantes'][rep29_key]['estados']['RS']['cidades'] = cidades_rep29
    data['representantes'][rep29_key]['estados']['RS']['total_cidades'] = len(cidades_rep29)
    data['representantes'][rep29_key]['total_cidades'] = len(cidades_rep29)
    
    # Configurar representante 28.0 (MYRALP)
    if 'RS' not in data['representantes'][rep28_key]['estados']:
        data['representantes'][rep28_key]['estados']['RS'] = {}
        # Adicionar RS aos estados atendidos se não estiver
        if 'RS   ' not in data['representantes'][rep28_key]['estados_atendidos']:
            data['representantes'][rep28_key]['estados_atendidos'].append('RS   ')
    
    data['representantes'][rep28_key]['estados']['RS']['cidades'] = cidades_rep28
    data['representantes'][rep28_key]['estados']['RS']['total_cidades'] = len(cidades_rep28)
    data['representantes'][rep28_key]['total_cidades'] = len(cidades_rep28)
    
    # 10. Salvar arquivo atualizado
    print()
    print("Salvando arquivo atualizado...")
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 11. Relatório final
    print()
    print("=== DIVISÃO REGIONAL CONCLUÍDA ===")
    print(f"Estado: RS (Rio Grande do Sul)")
    print(f"Total de cidades: {len(todas_cidades_rs)}")
    print()
    print(f"Representante 29.01 (ATTEX):")
    print(f"  Nome: {data['representantes'][rep29_key]['nome']}")
    print(f"  Cidades: {len(cidades_rep29)} (região específica)")
    print()
    print(f"Representante 28.0 (MYRALP):")
    print(f"  Nome: {data['representantes'][rep28_key]['nome']}")
    print(f"  Cidades: {len(cidades_rep28)} (resto do estado)")
    print()
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup salvo em: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = configurar_divisao_rs()
        if sucesso:
            print()
            print("Script executado com sucesso!")
        else:
            print()
            print("Script finalizado com problemas.")
    except Exception as e:
        print(f"ERRO durante a execução: {e}")
        print("Verifique os arquivos e tente novamente.")