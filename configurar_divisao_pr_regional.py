#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar divisão regional específica do Paraná (PR):
- Representante 36.01 (ROUND): Lista específica de 112 cidades
- Representante 40.01 (LIBER): Resto do estado (287 cidades restantes)

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

def carregar_cidades_pr():
    """
    Carrega todas as cidades do Paraná do arquivo municipios.json
    """
    print("Carregando todas as cidades do Paraná...")
    
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    pr_cities = []
    for feature in data['features']:
        if feature['properties']['UF'] == 'PR':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            pr_cities.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    pr_cities = sorted(list(set(pr_cities)))
    
    print(f"Total de cidades encontradas no PR: {len(pr_cities)}")
    return pr_cities

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_divisao_pr_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def configurar_divisao_pr():
    """
    Função principal para configurar a divisão regional do PR
    """
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Configuração Quarta Divisão Regional PR ===")
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # 2. Carregar todas as cidades do PR
    todas_cidades_pr = carregar_cidades_pr()
    
    # 3. Definir cidades específicas para representante 36.01 (lista do usuário)
    # Nota: Removidas inconsistências: "SAO MIGUEL", "TAMA", "JOANDAIA DO SUL", "POPECATU", "CAMBA"
    # que não existem no PR ou são duplicatas
    cidades_especificas_36 = [
        "ALTO PIQUIRI", "ALTONIA", "ALVORADA DO SUL", "AMPERE", "ANDIRA", "APUCARANA", 
        "ARAPONGAS", "ARAPOTI", "ARARUNA", "ASSAI", "ASSIS CHATEAUBRIAND", "ASTORGA", 
        "BOM SUCESSO", "CAFELANDIA", "CAMBARA", "CAMBE", "CAMPO MOURAO", 
        "CANDIDO DE ABREU", "CARAMBEI", "CAPANEMA", "CAPITAO LEONIDAS MARQUES", "CASCAVEL", 
        "CATANDUVAS", "CENTENARIO DO SUL", "CEU AZUL", "CHOPINZINHO", "CIANORTE", 
        "CIDADE GAUCHA", "COLORADO", "CORBELIA", "CORNELIO PROCOPIO", "CORONEL VIVIDA", 
        "CRUZEIRO DO IGUACU", "CRUZEIRO DO OESTE", "DOIS VIZINHOS", "ENTRE RIOS DO OESTE", 
        "FIGUEIRA", "FORMOSA DO OESTE", "FOZ DO IGUACU", "GUAIRA", "GUARACI", "IBEMA", 
        "IBIPORA", "IPORA", "ITAIPULANDIA", "JACAREZINHO", "JAGUAPITA", "JAGUARIAIVA", 
        "JANDAIA DO SUL", "JATAIZINHO", "JOAQUIM TAVORA", "JURANDA", 
        "LARANJEIRAS DO SUL", "LOANDA", "LONDRINA", "MANDAGUACU", "MANDAGUARI", 
        "MANGUEIRINHA", "MARECHAL CANDIDO RONDON", "MARIALVA", "MARINGA", "MARIPA", 
        "MARMELEIRO", "MATELANDIA", "MEDIANEIRA", "NOVA AURORA", "NOVA ESPERANCA", 
        "NOVA LONDRINA", "NOVA PRATA DO IGUACU", "NOVA SANTA ROSA", "PALOTINA", "PAICANDU", 
        "PARAISO DO NORTE", "PARANAVAI", "PATO BRAGADO", "PEROLA", "PLANALTO", 
        "PRANCHITA", "PRESIDENTE CASTELO BRANCO", "QUATRO PONTES", "QUEDAS DO IGUACU", 
        "REALEZA", "RENASCENCA", "RIO NEGRO", "ROLANDIA", "SANTA FE", "SANTA HELENA", 
        "SANTA TEREZA DO OESTE", "SANTA TEREZINHA DE ITAIPU", "SANTO ANTONIO DA PLATINA", 
        "SANTO ANTONIO DO SUDOESTE", "SAO CARLOS DO IVAI", "SAO JOAO", 
        "SAO MIGUEL DO IGUACU", "SAO PEDRO DO PARANA", "SAO TOME", "SARANDI", "SERTANOPOLIS", 
        "TAMARANA", "TAPEJARA", "TERRA BOA", "TERRA RICA", "TRES BARRAS DO PARANA", 
        "TOLEDO", "TOMAZINA", "UBIRATA", "UMUARAMA"
    ]
    
    # Normalizar nomes
    cidades_especificas_36_normalized = []
    for cidade in cidades_especificas_36:
        cidade_norm = normalizar_nome_cidade(cidade)
        cidades_especificas_36_normalized.append(cidade_norm)
    
    cidades_especificas_36_normalized = sorted(list(set(cidades_especificas_36_normalized)))
    
    # 4. Calcular cidades restantes para representante 40.01
    cidades_resto_pr = []
    for cidade in todas_cidades_pr:
        if cidade not in cidades_especificas_36_normalized:
            cidades_resto_pr.append(cidade)
    
    cidades_resto_pr = sorted(cidades_resto_pr)
    
    print(f"Divisão planejada:")
    print(f"  Representante 36.01 (ROUND): {len(cidades_especificas_36_normalized)} cidades (lista específica)")
    print(f"  Representante 40.01 (LIBER): {len(cidades_resto_pr)} cidades (resto do estado)")
    print(f"  Total: {len(cidades_especificas_36_normalized) + len(cidades_resto_pr)} cidades")
    print(f"  Verificação: PR tem {len(todas_cidades_pr)} cidades")
    
    if len(cidades_especificas_36_normalized) + len(cidades_resto_pr) != len(todas_cidades_pr):
        print("ERRO: A soma não confere com o total de cidades do PR!")
        return False
    
    # 5. Carregar arquivo de representantes
    print()
    print("Carregando arquivo de representantes...")
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 6. Encontrar os representantes
    rep36_key = None
    rep40_key = None
    
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '36.01':
            rep36_key = key
        elif rep.get('codigo') == '40.01':
            rep40_key = key
    
    if not rep36_key:
        print("ERRO: Representante 36.01 (ROUND) não encontrado!")
        return False
    
    if not rep40_key:
        print("ERRO: Representante 40.01 (LIBER) não encontrado!")
        return False
    
    print(f"Representante 36.01 encontrado: {data['representantes'][rep36_key]['nome']}")
    print(f"Representante 40.01 encontrado: {data['representantes'][rep40_key]['nome']}")
    
    # 7. Verificar configuração atual
    cidades_atuais_36 = data['representantes'][rep36_key]['estados']['PR']['cidades'] if 'PR' in data['representantes'][rep36_key]['estados'] else []
    cidades_atuais_40 = data['representantes'][rep40_key]['estados']['PR']['cidades'] if 'PR' in data['representantes'][rep40_key]['estados'] else []
    
    print()
    print("=== SITUAÇÃO ATUAL ===")
    print(f"ROUND (36.01) - Cidades atuais: {len(cidades_atuais_36)}")
    print(f"LIBER (40.01) - Cidades atuais: {len(cidades_atuais_40)}")
    
    # 8. Mostrar relatório detalhado
    print()
    print("=== CONFIGURAÇÃO FINAL ===")
    print()
    print(f"ROUND (36.01) - Lista específica ({len(cidades_especificas_36_normalized)} cidades):")
    for i, cidade in enumerate(cidades_especificas_36_normalized[:30], 1):
        print(f"  {i:2d}. {cidade}")
    
    if len(cidades_especificas_36_normalized) > 30:
        print(f"  ... e mais {len(cidades_especificas_36_normalized) - 30} cidades")
    
    print()
    print(f"Primeiras 30 cidades para LIBER (40.01) ({len(cidades_resto_pr)} cidades):")
    for i, cidade in enumerate(cidades_resto_pr[:30], 1):
        print(f"  {i:3d}. {cidade}")
    
    if len(cidades_resto_pr) > 30:
        print(f"  ... e mais {len(cidades_resto_pr) - 30} cidades")
    
    # 9. Confirmar alteração
    print()
    resposta = input(f"Confirma a divisão regional do PR conforme especificado? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # 10. Atualizar dados dos representantes
    
    # Configurar representante 36.01 (ROUND) com lista específica
    if 'PR' not in data['representantes'][rep36_key]['estados']:
        data['representantes'][rep36_key]['estados']['PR'] = {}
        if 'PR   ' not in data['representantes'][rep36_key]['estados_atendidos']:
            data['representantes'][rep36_key]['estados_atendidos'].append('PR   ')
    
    data['representantes'][rep36_key]['estados']['PR']['cidades'] = cidades_especificas_36_normalized
    data['representantes'][rep36_key]['estados']['PR']['total_cidades'] = len(cidades_especificas_36_normalized)
    data['representantes'][rep36_key]['total_cidades'] = len(cidades_especificas_36_normalized)
    
    # Configurar representante 40.01 (LIBER) com resto do estado
    if 'PR' not in data['representantes'][rep40_key]['estados']:
        data['representantes'][rep40_key]['estados']['PR'] = {}
        if 'PR   ' not in data['representantes'][rep40_key]['estados_atendidos']:
            data['representantes'][rep40_key]['estados_atendidos'].append('PR   ')
    
    data['representantes'][rep40_key]['estados']['PR']['cidades'] = cidades_resto_pr
    data['representantes'][rep40_key]['estados']['PR']['total_cidades'] = len(cidades_resto_pr)
    data['representantes'][rep40_key]['total_cidades'] = len(cidades_resto_pr)
    
    # 11. Salvar arquivo atualizado
    print()
    print("Salvando arquivo atualizado...")
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 12. Relatório final
    print()
    print("=== QUARTA DIVISÃO REGIONAL CONCLUÍDA ===")
    print(f"Estado: PR (Paraná)")
    print(f"Total de cidades: {len(todas_cidades_pr)}")
    print()
    print(f"Representante 36.01 (ROUND):")
    print(f"  Nome: {data['representantes'][rep36_key]['nome']}")
    print(f"  Cidades: {len(cidades_especificas_36_normalized)} (lista específica)")
    print()
    print(f"Representante 40.01 (LIBER):")
    print(f"  Nome: {data['representantes'][rep40_key]['nome']}")
    print(f"  Cidades: {len(cidades_resto_pr)} (resto do estado)")
    print()
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup salvo em: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = configurar_divisao_pr()
        if sucesso:
            print()
            print("Script executado com sucesso!")
        else:
            print()
            print("Script finalizado com problemas.")
    except Exception as e:
        print(f"ERRO durante a execução: {e}")
        print("Verifique os arquivos e tente novamente.")