#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que o representante A.Gouveia (ID 17.0)
atende TODAS as cidades do Pernambuco (PE).

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

def validar_gouveia_pe():
    """
    Valida se A.Gouveia atende todas as cidades do PE
    """
    print("=== VALIDAÇÃO A.GOUVEIA PE ===")
    print()
    
    # 1. Carregar todas as cidades do PE do arquivo de municípios
    print("1. Carregando cidades do PE do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_pe = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'PE':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_pe.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_pe = sorted(list(set(todas_cidades_pe)))
    print(f"   Total de cidades no PE (municípios.json): {len(todas_cidades_pe)}")
    
    # 2. Carregar cidades do A.Gouveia
    print("2. Carregando cidades do A.Gouveia...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar A.Gouveia
    gouveia_info = None
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '17.0':
            gouveia_info = rep
            break
    
    if not gouveia_info:
        print("   ERRO: A.Gouveia não encontrado!")
        return False
    
    cidades_gouveia = gouveia_info['estados']['PE']['cidades']
    cidades_gouveia_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_gouveia]
    cidades_gouveia_normalized = sorted(list(set(cidades_gouveia_normalized)))
    
    print(f"   Nome: {gouveia_info['nome']}")
    print(f"   Código: {gouveia_info['codigo']}")
    print(f"   Total de cidades do A.Gouveia: {len(cidades_gouveia_normalized)}")
    
    # 3. Comparação e validação
    print()
    print("3. Validação:")
    
    # Cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_pe:
        if cidade not in cidades_gouveia_normalized:
            cidades_faltantes.append(cidade)
    
    # Cidades extras (que A.Gouveia tem mas não existem no PE)
    cidades_extras = []
    for cidade in cidades_gouveia_normalized:
        if cidade not in todas_cidades_pe:
            cidades_extras.append(cidade)
    
    # Resultados da validação
    print(f"   ✓ Cidades no arquivo municípios.json: {len(todas_cidades_pe)}")
    print(f"   ✓ Cidades atendidas pelo A.Gouveia: {len(cidades_gouveia_normalized)}")
    print(f"   ✓ Cidades faltantes: {len(cidades_faltantes)}")
    print(f"   ✓ Cidades extras: {len(cidades_extras)}")
    
    # 4. Relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    
    if len(cidades_faltantes) == 0 and len(cidades_extras) == 0:
        print("🎉 SUCESSO! A.Gouveia atende TODAS as cidades do Pernambuco!")
        print("   Cobertura: 100%")
        cobertura_completa = True
    else:
        print("⚠️  ATENÇÃO! Existem divergências:")
        cobertura_completa = False
        
        if len(cidades_faltantes) > 0:
            print(f"   Cidades faltantes ({len(cidades_faltantes)}):")
            for i, cidade in enumerate(cidades_faltantes, 1):
                print(f"     {i:3d}. {cidade}")
        
        if len(cidades_extras) > 0:
            print(f"   Cidades extras ({len(cidades_extras)}):")
            for i, cidade in enumerate(cidades_extras, 1):
                print(f"     {i:3d}. {cidade}")
    
    # 5. Estatísticas finais
    print()
    print("=== ESTATÍSTICAS FINAIS ===")
    print(f"Representante: {gouveia_info['nome']}")
    print(f"Código: {gouveia_info['codigo']}")
    print(f"Estado: PE (Pernambuco)")
    print(f"Cidades atendidas: {len(cidades_gouveia_normalized)}")
    print(f"Total de cidades no PE: {len(todas_cidades_pe)}")
    
    if cobertura_completa:
        print(f"Cobertura: 100% ✅")
    else:
        cobertura_pct = (len(cidades_gouveia_normalized) - len(cidades_extras)) / len(todas_cidades_pe) * 100
        print(f"Cobertura: {cobertura_pct:.1f}% ⚠️")
    
    return cobertura_completa

if __name__ == "__main__":
    try:
        sucesso = validar_gouveia_pe()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")