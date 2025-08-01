#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que o representante ALR (ID 19.0)
atende TODAS as cidades da Paraíba (PB).

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

def validar_alr_pb():
    """
    Valida se ALR atende todas as cidades da PB
    """
    print("=== VALIDAÇÃO ALR PB ===")
    print()
    
    # 1. Carregar todas as cidades da PB do arquivo de municípios
    print("1. Carregando cidades da PB do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_pb = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'PB':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_pb.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_pb = sorted(list(set(todas_cidades_pb)))
    print(f"   Total de cidades na PB (municípios.json): {len(todas_cidades_pb)}")
    
    # 2. Carregar cidades do ALR
    print("2. Carregando cidades do ALR...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar ALR
    alr_info = None
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '19.0':
            alr_info = rep
            break
    
    if not alr_info:
        print("   ERRO: ALR não encontrado!")
        return False
    
    cidades_alr = alr_info['estados']['PB']['cidades']
    cidades_alr_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_alr]
    cidades_alr_normalized = sorted(list(set(cidades_alr_normalized)))
    
    print(f"   Nome: {alr_info['nome']}")
    print(f"   Código: {alr_info['codigo']}")
    print(f"   Total de cidades do ALR: {len(cidades_alr_normalized)}")
    
    # 3. Comparação e validação
    print()
    print("3. Validação:")
    
    # Cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_pb:
        if cidade not in cidades_alr_normalized:
            cidades_faltantes.append(cidade)
    
    # Cidades extras (que ALR tem mas não existem na PB)
    cidades_extras = []
    for cidade in cidades_alr_normalized:
        if cidade not in todas_cidades_pb:
            cidades_extras.append(cidade)
    
    # Resultados da validação
    print(f"   ✓ Cidades no arquivo municípios.json: {len(todas_cidades_pb)}")
    print(f"   ✓ Cidades atendidas pelo ALR: {len(cidades_alr_normalized)}")
    print(f"   ✓ Cidades faltantes: {len(cidades_faltantes)}")
    print(f"   ✓ Cidades extras: {len(cidades_extras)}")
    
    # 4. Relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    
    if len(cidades_faltantes) == 0 and len(cidades_extras) == 0:
        print("🎉 SUCESSO! ALR atende TODAS as cidades da Paraíba!")
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
    print(f"Representante: {alr_info['nome']}")
    print(f"Código: {alr_info['codigo']}")
    print(f"Estado: PB (Paraíba)")
    print(f"Cidades atendidas: {len(cidades_alr_normalized)}")
    print(f"Total de cidades na PB: {len(todas_cidades_pb)}")
    
    if cobertura_completa:
        print(f"Cobertura: 100% ✅")
    else:
        cobertura_pct = (len(cidades_alr_normalized) - len(cidades_extras)) / len(todas_cidades_pb) * 100
        print(f"Cobertura: {cobertura_pct:.1f}% ⚠️")
    
    return cobertura_completa

if __name__ == "__main__":
    try:
        sucesso = validar_alr_pb()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")