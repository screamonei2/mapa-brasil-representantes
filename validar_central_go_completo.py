#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que o representante Central Representações (ID 32.0)
atende TODAS as cidades do estado de Goiás (GO).

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

def validar_central_go():
    """
    Valida se Central Representações atende todas as cidades do GO
    """
    print("=== VALIDAÇÃO CENTRAL REPRESENTAÇÕES GO ===")
    print()
    
    # 1. Carregar todas as cidades do GO do arquivo de municípios
    print("1. Carregando cidades do GO do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_go = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'GO':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_go.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_go = sorted(list(set(todas_cidades_go)))
    print(f"   Total de cidades no GO (municípios.json): {len(todas_cidades_go)}")
    
    # 2. Carregar cidades da Central Representações
    print("2. Carregando cidades da Central Representações...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar Central Representações
    central_info = None
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '32.0':
            central_info = rep
            break
    
    if not central_info:
        print("   ERRO: Central Representações não encontrado!")
        return False
    
    cidades_central = central_info['estados']['GO']['cidades']
    cidades_central_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_central]
    cidades_central_normalized = sorted(list(set(cidades_central_normalized)))
    
    print(f"   Nome: {central_info['nome']}")
    print(f"   Código: {central_info['codigo']}")
    print(f"   Total de cidades da Central: {len(cidades_central_normalized)}")
    
    # 3. Comparação e validação
    print()
    print("3. Validação:")
    
    # Cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_go:
        if cidade not in cidades_central_normalized:
            cidades_faltantes.append(cidade)
    
    # Cidades extras (que Central tem mas não existem no GO)
    cidades_extras = []
    for cidade in cidades_central_normalized:
        if cidade not in todas_cidades_go:
            cidades_extras.append(cidade)
    
    # Resultados da validação
    print(f"   ✓ Cidades no arquivo municípios.json: {len(todas_cidades_go)}")
    print(f"   ✓ Cidades atendidas pela Central: {len(cidades_central_normalized)}")
    print(f"   ✓ Cidades faltantes: {len(cidades_faltantes)}")
    print(f"   ✓ Cidades extras: {len(cidades_extras)}")
    
    # 4. Relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    
    if len(cidades_faltantes) == 0 and len(cidades_extras) == 0:
        print("🎉 SUCESSO! Central Representações atende TODAS as cidades do estado de Goiás!")
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
    
    # 5. Verificação do Distrito Federal
    print()
    print("=== VERIFICAÇÃO DISTRITO FEDERAL ===")
    
    # Verificar se Central não está atendendo DF (como solicitado)
    if 'DF' in central_info.get('estados', {}):
        print("⚠️  ATENÇÃO: Central Representações está atendendo DF (deveria ser apenas RUMO CERTO)")
    else:
        print("✅ CORRETO: Central Representações não atende DF (fica com RUMO CERTO)")
    
    # Verificar se RUMO CERTO ainda atende DF
    rumo_certo_df = False
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '50.01' and 'DF' in rep.get('estados', {}):
            rumo_certo_df = True
            df_cidades = rep['estados']['DF']['total_cidades']
            print(f"✅ RUMO CERTO mantém DF: {df_cidades} cidades")
            break
    
    if not rumo_certo_df:
        print("⚠️  ATENÇÃO: RUMO CERTO não está atendendo DF!")
    
    # 6. Estatísticas finais
    print()
    print("=== ESTATÍSTICAS FINAIS ===")
    print(f"Representante: {central_info['nome']}")
    print(f"Código: {central_info['codigo']}")
    print(f"Estado: GO (Goiás)")
    print(f"Cidades atendidas: {len(cidades_central_normalized)}")
    print(f"Total de cidades no GO: {len(todas_cidades_go)}")
    
    if cobertura_completa:
        print(f"Cobertura: 100% ✅")
    else:
        cobertura_pct = (len(cidades_central_normalized) - len(cidades_extras)) / len(todas_cidades_go) * 100
        print(f"Cobertura: {cobertura_pct:.1f}% ⚠️")
    
    return cobertura_completa

if __name__ == "__main__":
    try:
        sucesso = validar_central_go()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")