#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar divisão regional específica de Santa Catarina (SC):
- Representante 37.0 (IZAFER): Lista específica de 33 cidades
- Representante 35.01 (ZIER): Resto do estado (264 cidades restantes)

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

def carregar_cidades_sc():
    """
    Carrega todas as cidades de Santa Catarina do arquivo municipios.json
    """
    print("Carregando todas as cidades de Santa Catarina...")
    
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    sc_cities = []
    for feature in data['features']:
        if feature['properties']['UF'] == 'SC':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            sc_cities.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    sc_cities = sorted(list(set(sc_cities)))
    
    print(f"Total de cidades encontradas em SC: {len(sc_cities)}")
    return sc_cities

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_divisao_sc_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def configurar_divisao_sc():
    """
    Função principal para configurar a divisão regional de SC
    """
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Configuração Terceira Divisão Regional SC ===")
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # 2. Carregar todas as cidades de SC
    todas_cidades_sc = carregar_cidades_sc()
    
    # 3. Definir cidades específicas para representante 37.0 (lista do usuário)
    # Nota: Removido "PICARRAS" pois não existe em SC (já temos "BALNEARIO PICARRAS")
    cidades_especificas_37 = [
        "BALNEARIO PICARRAS", "BLUMENAU", "BRUSQUE", "CRICIUMA", "CUNHA PORA", 
        "ITAJAI", "JARAGUA DO SUL", "JOINVILLE", "RIO DO SUL", 
        "SANTO AMARO DA IMPERATRIZ", "TUBARAO", "BALNEARIO CAMBORIU", "FLORIANOPOLIS", 
        "TAIO", "COCAL DO SUL", "NAVEGANTES", "PENHA", "XANXERE", "INDAIAL", 
        "ITAPEMA", "MAFRA", "MORRO DA FUMACA", "SAO BENTO DO SUL", "SAO JOAO BATISTA", 
        "SAO JOSE", "TIJUCAS", "ANITA GARIBALDI", "BIGUACU", "CACADOR", "GASPAR", 
        "GUARAMIRIM", "ARAQUARI", "CAMBORIU"
    ]
    
    # Normalizar nomes
    cidades_especificas_37_normalized = []
    for cidade in cidades_especificas_37:
        cidade_norm = normalizar_nome_cidade(cidade)
        cidades_especificas_37_normalized.append(cidade_norm)
    
    cidades_especificas_37_normalized = sorted(list(set(cidades_especificas_37_normalized)))
    
    # 4. Calcular cidades restantes para representante 35.01
    cidades_resto_sc = []
    for cidade in todas_cidades_sc:
        if cidade not in cidades_especificas_37_normalized:
            cidades_resto_sc.append(cidade)
    
    cidades_resto_sc = sorted(cidades_resto_sc)
    
    print(f"Divisão planejada:")
    print(f"  Representante 37.0 (IZAFER): {len(cidades_especificas_37_normalized)} cidades (lista específica)")
    print(f"  Representante 35.01 (ZIER): {len(cidades_resto_sc)} cidades (resto do estado)")
    print(f"  Total: {len(cidades_especificas_37_normalized) + len(cidades_resto_sc)} cidades")
    print(f"  Verificação: SC tem {len(todas_cidades_sc)} cidades")
    
    if len(cidades_especificas_37_normalized) + len(cidades_resto_sc) != len(todas_cidades_sc):
        print("ERRO: A soma não confere com o total de cidades de SC!")
        return False
    
    # 5. Carregar arquivo de representantes
    print()
    print("Carregando arquivo de representantes...")
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 6. Encontrar os representantes
    rep37_key = None
    rep351_key = None
    
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '37.0':
            rep37_key = key
        elif rep.get('codigo') == '35.01':
            rep351_key = key
    
    if not rep37_key:
        print("ERRO: Representante 37.0 (IZAFER) não encontrado!")
        return False
    
    if not rep351_key:
        print("ERRO: Representante 35.01 (ZIER) não encontrado!")
        return False
    
    print(f"Representante 37.0 encontrado: {data['representantes'][rep37_key]['nome']}")
    print(f"Representante 35.01 encontrado: {data['representantes'][rep351_key]['nome']}")
    
    # 7. Verificar configuração atual
    cidades_atuais_37 = data['representantes'][rep37_key]['estados']['SC']['cidades']
    cidades_atuais_351 = data['representantes'][rep351_key]['estados']['SC']['cidades']
    
    print()
    print("=== SITUAÇÃO ATUAL ===")
    print(f"IZAFER (37.0) - Cidades atuais: {len(cidades_atuais_37)}")
    print(f"ZIER (35.01) - Cidades atuais: {len(cidades_atuais_351)}")
    
    # 8. Mostrar relatório detalhado
    print()
    print("=== CONFIGURAÇÃO FINAL ===")
    print()
    print(f"IZAFER (37.0) - Lista específica ({len(cidades_especificas_37_normalized)} cidades):")
    for i, cidade in enumerate(cidades_especificas_37_normalized, 1):
        print(f"  {i:2d}. {cidade}")
    
    print()
    print(f"Primeiras 30 cidades para ZIER (35.01) ({len(cidades_resto_sc)} cidades):")
    for i, cidade in enumerate(cidades_resto_sc[:30], 1):
        print(f"  {i:3d}. {cidade}")
    
    if len(cidades_resto_sc) > 30:
        print(f"  ... e mais {len(cidades_resto_sc) - 30} cidades")
    
    # 9. Confirmar alteração
    print()
    resposta = input(f"Confirma a divisão regional de SC conforme especificado? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # 10. Atualizar dados dos representantes
    
    # Configurar representante 37.0 (IZAFER) com lista específica
    data['representantes'][rep37_key]['estados']['SC']['cidades'] = cidades_especificas_37_normalized
    data['representantes'][rep37_key]['estados']['SC']['total_cidades'] = len(cidades_especificas_37_normalized)
    data['representantes'][rep37_key]['total_cidades'] = len(cidades_especificas_37_normalized)
    
    # Configurar representante 35.01 (ZIER) com resto do estado
    data['representantes'][rep351_key]['estados']['SC']['cidades'] = cidades_resto_sc
    data['representantes'][rep351_key]['estados']['SC']['total_cidades'] = len(cidades_resto_sc)
    data['representantes'][rep351_key]['total_cidades'] = len(cidades_resto_sc)
    
    # 11. Salvar arquivo atualizado
    print()
    print("Salvando arquivo atualizado...")
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 12. Relatório final
    print()
    print("=== TERCEIRA DIVISÃO REGIONAL CONCLUÍDA ===")
    print(f"Estado: SC (Santa Catarina)")
    print(f"Total de cidades: {len(todas_cidades_sc)}")
    print()
    print(f"Representante 37.0 (IZAFER):")
    print(f"  Nome: {data['representantes'][rep37_key]['nome']}")
    print(f"  Cidades: {len(cidades_especificas_37_normalized)} (lista específica)")
    print()
    print(f"Representante 35.01 (ZIER):")
    print(f"  Nome: {data['representantes'][rep351_key]['nome']}")
    print(f"  Cidades: {len(cidades_resto_sc)} (resto do estado)")
    print()
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup salvo em: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = configurar_divisao_sc()
        if sucesso:
            print()
            print("Script executado com sucesso!")
        else:
            print()
            print("Script finalizado com problemas.")
    except Exception as e:
        print(f"ERRO durante a execução: {e}")
        print("Verifique os arquivos e tente novamente.")