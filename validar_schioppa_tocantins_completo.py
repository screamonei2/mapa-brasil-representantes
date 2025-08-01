#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que o representante Schioppa (ID 01)
atende TODAS as cidades do Tocantins (TO).

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

def validar_schioppa_to():
    """
    Valida se Schioppa atende todas as cidades do TO
    """
    print("=== VALIDAÇÃO SCHIOPPA TO ===")
    print()
    
    # 1. Carregar todas as cidades do TO do arquivo de municípios
    print("1. Carregando cidades do TO do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_to = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'TO':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_to.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_to = sorted(list(set(todas_cidades_to)))
    print(f"   Total de cidades no TO (municípios.json): {len(todas_cidades_to)}")
    
    # 2. Carregar cidades do Schioppa
    print("2. Carregando cidades do Schioppa...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar Schioppa
    schioppa_info = None
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '01':
            schioppa_info = rep
            break
    
    if not schioppa_info:
        print("   ERRO: Schioppa não encontrado!")
        return False
    
    print(f"   Nome: {schioppa_info['nome']}")
    print(f"   Código: {schioppa_info['codigo']}")
    print(f"   Estados atendidos: {len(schioppa_info['estados_atendidos'])}")
    
    # Verificar se TO existe
    if 'TO' not in schioppa_info['estados']:
        print("   ERRO: TO não encontrado nos estados do Schioppa!")
        return False
    
    cidades_schioppa_to = schioppa_info['estados']['TO']['cidades']
    cidades_schioppa_to_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_schioppa_to]
    cidades_schioppa_to_normalized = sorted(list(set(cidades_schioppa_to_normalized)))
    
    print(f"   Total de cidades do Schioppa no TO: {len(cidades_schioppa_to_normalized)}")
    
    # 3. Comparação e validação
    print()
    print("3. Validação:")
    
    # Cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_to:
        if cidade not in cidades_schioppa_to_normalized:
            cidades_faltantes.append(cidade)
    
    # Cidades extras (que Schioppa tem mas não existem no TO)
    cidades_extras = []
    for cidade in cidades_schioppa_to_normalized:
        if cidade not in todas_cidades_to:
            cidades_extras.append(cidade)
    
    # Resultados da validação
    print(f"   ✓ Cidades no arquivo municípios.json: {len(todas_cidades_to)}")
    print(f"   ✓ Cidades atendidas pelo Schioppa no TO: {len(cidades_schioppa_to_normalized)}")
    print(f"   ✓ Cidades faltantes: {len(cidades_faltantes)}")
    print(f"   ✓ Cidades extras: {len(cidades_extras)}")
    
    # 4. Relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    
    if len(cidades_faltantes) == 0 and len(cidades_extras) == 0:
        print("🎉 SUCESSO! Schioppa atende TODAS as cidades do Tocantins!")
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
    print(f"Representante: {schioppa_info['nome']}")
    print(f"Código: {schioppa_info['codigo']}")
    print(f"Estados atendidos: {len(schioppa_info['estados_atendidos'])}")
    print(f"Lista de estados: {', '.join([uf.strip() for uf in schioppa_info['estados_atendidos']])}")
    print(f"Estado: TO (Tocantins)")
    print(f"Cidades atendidas no TO: {len(cidades_schioppa_to_normalized)}")
    print(f"Total de cidades no TO: {len(todas_cidades_to)}")
    print(f"Total geral de cidades: {schioppa_info['total_cidades']}")
    
    if cobertura_completa:
        print(f"Cobertura TO: 100% ✅")
    else:
        cobertura_pct = (len(cidades_schioppa_to_normalized) - len(cidades_extras)) / len(todas_cidades_to) * 100
        print(f"Cobertura TO: {cobertura_pct:.1f}% ⚠️")
    
    return cobertura_completa

if __name__ == "__main__":
    try:
        sucesso = validar_schioppa_to()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")