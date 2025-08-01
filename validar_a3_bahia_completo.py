#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que o representante A3 (ID 51.0)
atende TODAS as cidades da Bahia (BA).

Autor: Assistente AI
Data: $(date +%Y-%m-%d)
"""

import json
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

def validar_a3_ba():
    """
    Valida se A3 atende todas as cidades da BA
    """
    print("=== VALIDAÇÃO A3 BA ===")
    print()
    
    # 1. Carregar todas as cidades da BA do arquivo de municípios
    print("1. Carregando cidades da BA do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_ba = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'BA':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_ba.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_ba = sorted(list(set(todas_cidades_ba)))
    print(f"   Total de cidades na BA (municípios.json): {len(todas_cidades_ba)}")
    
    # 2. Carregar cidades do A3
    print("2. Carregando cidades do A3...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar A3
    a3_info = None
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '51.0':
            a3_info = rep
            break
    
    if not a3_info:
        print("   ERRO: A3 não encontrado!")
        return False
    
    cidades_a3 = a3_info['estados']['BA']['cidades']
    cidades_a3_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_a3]
    cidades_a3_normalized = sorted(list(set(cidades_a3_normalized)))
    
    print(f"   Nome: {a3_info['nome']}")
    print(f"   Código: {a3_info['codigo']}")
    print(f"   Total de cidades do A3: {len(cidades_a3_normalized)}")
    
    # 3. Comparação e validação
    print()
    print("3. Validação:")
    
    # Cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_ba:
        if cidade not in cidades_a3_normalized:
            cidades_faltantes.append(cidade)
    
    # Cidades extras (que A3 tem mas não existem na BA)
    cidades_extras = []
    for cidade in cidades_a3_normalized:
        if cidade not in todas_cidades_ba:
            cidades_extras.append(cidade)
    
    # Resultados da validação
    print(f"   ✓ Cidades no arquivo municípios.json: {len(todas_cidades_ba)}")
    print(f"   ✓ Cidades atendidas pelo A3: {len(cidades_a3_normalized)}")
    print(f"   ✓ Cidades faltantes: {len(cidades_faltantes)}")
    print(f"   ✓ Cidades extras: {len(cidades_extras)}")
    
    # 4. Relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    
    if len(cidades_faltantes) == 0 and len(cidades_extras) == 0:
        print("🎉 SUCESSO! A3 atende TODAS as cidades da Bahia!")
        print("   Cobertura: 100%")
        cobertura_completa = True
    else:
        print("⚠️  ATENÇÃO! Existem divergências:")
        cobertura_completa = False
        
        if len(cidades_faltantes) > 0:
            print(f"   Cidades faltantes ({len(cidades_faltantes)}):")
            for i, cidade in enumerate(cidades_faltantes[:20], 1):
                print(f"     {i:3d}. {cidade}")
            if len(cidades_faltantes) > 20:
                print(f"     ... e mais {len(cidades_faltantes) - 20} cidades")
        
        if len(cidades_extras) > 0:
            print(f"   Cidades extras ({len(cidades_extras)}):")
            for i, cidade in enumerate(cidades_extras[:20], 1):
                print(f"     {i:3d}. {cidade}")
            if len(cidades_extras) > 20:
                print(f"     ... e mais {len(cidades_extras) - 20} cidades")
    
    # 5. Estatísticas finais
    print()
    print("=== ESTATÍSTICAS FINAIS ===")
    print(f"Representante: {a3_info['nome']}")
    print(f"Código: {a3_info['codigo']}")
    print(f"Estado: BA (Bahia)")
    print(f"Cidades atendidas: {len(cidades_a3_normalized)}")
    print(f"Total de cidades na BA: {len(todas_cidades_ba)}")
    
    if cobertura_completa:
        print(f"Cobertura: 100% ✅")
    else:
        cobertura_pct = (len(cidades_a3_normalized) - len(cidades_extras)) / len(todas_cidades_ba) * 100
        print(f"Cobertura: {cobertura_pct:.1f}% ⚠️")
    
    return cobertura_completa

if __name__ == "__main__":
    try:
        sucesso = validar_a3_ba()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")