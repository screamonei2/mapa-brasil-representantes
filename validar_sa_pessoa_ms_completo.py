#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que o representante SA & Pessoa (ID 34.0)
atende TODAS as cidades do Mato Grosso do Sul (MS).

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

def validar_sa_pessoa_ms():
    """
    Valida se SA & Pessoa atende todas as cidades do MS
    """
    print("=== VALIDAÇÃO SA & PESSOA MS ===")
    print()
    
    # 1. Carregar todas as cidades do MS do arquivo de municípios
    print("1. Carregando cidades do MS do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_ms = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'MS':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_ms.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_ms = sorted(list(set(todas_cidades_ms)))
    print(f"   Total de cidades no MS (municípios.json): {len(todas_cidades_ms)}")
    
    # 2. Carregar cidades do SA & Pessoa
    print("2. Carregando cidades do SA & Pessoa...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar SA & Pessoa
    sa_pessoa_info = None
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '34.0':
            sa_pessoa_info = rep
            break
    
    if not sa_pessoa_info:
        print("   ERRO: SA & Pessoa não encontrado!")
        return False
    
    cidades_sa_pessoa = sa_pessoa_info['estados']['MS']['cidades']
    cidades_sa_pessoa_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_sa_pessoa]
    cidades_sa_pessoa_normalized = sorted(list(set(cidades_sa_pessoa_normalized)))
    
    print(f"   Nome: {sa_pessoa_info['nome']}")
    print(f"   Código: {sa_pessoa_info['codigo']}")
    print(f"   Total de cidades do SA & Pessoa: {len(cidades_sa_pessoa_normalized)}")
    
    # 3. Comparação e validação
    print()
    print("3. Validação:")
    
    # Cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_ms:
        if cidade not in cidades_sa_pessoa_normalized:
            cidades_faltantes.append(cidade)
    
    # Cidades extras (que SA & Pessoa tem mas não existem no MS)
    cidades_extras = []
    for cidade in cidades_sa_pessoa_normalized:
        if cidade not in todas_cidades_ms:
            cidades_extras.append(cidade)
    
    # Resultados da validação
    print(f"   ✓ Cidades no arquivo municípios.json: {len(todas_cidades_ms)}")
    print(f"   ✓ Cidades atendidas pelo SA & Pessoa: {len(cidades_sa_pessoa_normalized)}")
    print(f"   ✓ Cidades faltantes: {len(cidades_faltantes)}")
    print(f"   ✓ Cidades extras: {len(cidades_extras)}")
    
    # 4. Relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    
    if len(cidades_faltantes) == 0 and len(cidades_extras) == 0:
        print("🎉 SUCESSO! SA & Pessoa atende TODAS as cidades do Mato Grosso do Sul!")
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
    print(f"Representante: {sa_pessoa_info['nome']}")
    print(f"Código: {sa_pessoa_info['codigo']}")
    print(f"Estado: MS (Mato Grosso do Sul)")
    print(f"Cidades atendidas: {len(cidades_sa_pessoa_normalized)}")
    print(f"Total de cidades no MS: {len(todas_cidades_ms)}")
    
    if cobertura_completa:
        print(f"Cobertura: 100% ✅")
    else:
        cobertura_pct = (len(cidades_sa_pessoa_normalized) - len(cidades_extras)) / len(todas_cidades_ms) * 100
        print(f"Cobertura: {cobertura_pct:.1f}% ⚠️")
    
    return cobertura_completa

if __name__ == "__main__":
    try:
        sucesso = validar_sa_pessoa_ms()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")