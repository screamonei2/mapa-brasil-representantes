#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que a divisão regional de Santa Catarina (SC)
foi configurada corretamente entre os representantes IZAFER (37.0) e ZIER (35.01).

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

def validar_divisao_sc():
    """
    Valida se a divisão regional de SC foi configurada corretamente
    """
    print("=== VALIDAÇÃO TERCEIRA DIVISÃO REGIONAL SC ===")
    print()
    
    # 1. Carregar todas as cidades de SC do arquivo de municípios
    print("1. Carregando cidades de SC do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_sc = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'SC':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_sc.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_sc = sorted(list(set(todas_cidades_sc)))
    print(f"   Total de cidades em SC (municípios.json): {len(todas_cidades_sc)}")
    
    # 2. Carregar cidades dos representantes
    print("2. Carregando cidades dos representantes...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar representantes
    izafer_info = None
    zier_info = None
    
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '37.0':
            izafer_info = rep
        elif rep.get('codigo') == '35.01':
            zier_info = rep
    
    if not izafer_info:
        print("   ERRO: IZAFER (37.0) não encontrado!")
        return False
    
    if not zier_info:
        print("   ERRO: ZIER (35.01) não encontrado!")
        return False
    
    # Verificar se ambos atendem SC
    if 'SC' not in izafer_info.get('estados', {}):
        print("   ERRO: IZAFER não atende SC!")
        return False
    
    if 'SC' not in zier_info.get('estados', {}):
        print("   ERRO: ZIER não atende SC!")
        return False
    
    cidades_izafer = izafer_info['estados']['SC']['cidades']
    cidades_zier = zier_info['estados']['SC']['cidades']
    
    # Normalizar listas
    cidades_izafer_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_izafer]
    cidades_zier_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_zier]
    
    cidades_izafer_normalized = sorted(list(set(cidades_izafer_normalized)))
    cidades_zier_normalized = sorted(list(set(cidades_zier_normalized)))
    
    print(f"   IZAFER: {len(cidades_izafer_normalized)} cidades")
    print(f"   ZIER: {len(cidades_zier_normalized)} cidades")
    
    # 3. Validações principais
    print()
    print("3. Validações:")
    
    # Validação 1: IZAFER tem lista específica
    print("   a) Verificando se IZAFER tem a lista específica...")
    
    lista_esperada_izafer = [
        "ANITA GARIBALDI", "ARAQUARI", "BALNEARIO CAMBORIU", "BALNEARIO PICARRAS", 
        "BIGUACU", "BLUMENAU", "BRUSQUE", "CACADOR", "CAMBORIU", "COCAL DO SUL", 
        "CRICIUMA", "CUNHA PORA", "FLORIANOPOLIS", "GASPAR", "GUARAMIRIM", "INDAIAL", 
        "ITAJAI", "ITAPEMA", "JARAGUA DO SUL", "JOINVILLE", "MAFRA", "MORRO DA FUMACA", 
        "NAVEGANTES", "PENHA", "RIO DO SUL", "SANTO AMARO DA IMPERATRIZ", "SAO BENTO DO SUL", 
        "SAO JOAO BATISTA", "SAO JOSE", "TAIO", "TIJUCAS", "TUBARAO", "XANXERE"
    ]
    
    # Normalizar lista esperada
    lista_esperada_izafer_norm = [normalizar_nome_cidade(cidade) for cidade in lista_esperada_izafer]
    lista_esperada_izafer_norm = sorted(list(set(lista_esperada_izafer_norm)))
    
    if cidades_izafer_normalized == lista_esperada_izafer_norm:
        print("      ✅ IZAFER tem exatamente a lista específica!")
        izafer_ok = True
    else:
        print("      ❌ IZAFER não tem a lista específica correta:")
        print(f"         Atual: {len(cidades_izafer_normalized)} cidades")
        print(f"         Esperado: {len(lista_esperada_izafer_norm)} cidades")
        izafer_ok = False
    
    # Validação 2: ZIER tem todas as outras cidades
    print("   b) Verificando se ZIER tem o resto do estado...")
    
    cidades_esperadas_zier = []
    for cidade in todas_cidades_sc:
        if cidade not in lista_esperada_izafer_norm:
            cidades_esperadas_zier.append(cidade)
    
    cidades_zier_faltantes = []
    for cidade in cidades_esperadas_zier:
        if cidade not in cidades_zier_normalized:
            cidades_zier_faltantes.append(cidade)
    
    cidades_zier_extras = []
    for cidade in cidades_zier_normalized:
        if cidade not in cidades_esperadas_zier:
            cidades_zier_extras.append(cidade)
    
    if len(cidades_zier_faltantes) == 0 and len(cidades_zier_extras) == 0:
        print("      ✅ ZIER tem exatamente as cidades restantes!")
        zier_ok = True
    else:
        print("      ❌ ZIER não tem as cidades restantes corretas:")
        if cidades_zier_faltantes:
            print(f"         Faltantes: {len(cidades_zier_faltantes)} cidades")
        if cidades_zier_extras:
            print(f"         Extras: {len(cidades_zier_extras)} cidades")
        zier_ok = False
    
    # Validação 3: Verificar sobreposição
    print("   c) Verificando sobreposição...")
    
    sobreposicao = []
    for cidade in cidades_izafer_normalized:
        if cidade in cidades_zier_normalized:
            sobreposicao.append(cidade)
    
    if len(sobreposicao) == 0:
        print("      ✅ Não há sobreposição entre os representantes!")
        sem_sobreposicao = True
    else:
        print(f"      ❌ Há sobreposição de {len(sobreposicao)} cidades:")
        for cidade in sobreposicao:
            print(f"         - {cidade}")
        sem_sobreposicao = False
    
    # Validação 4: Soma total
    print("   d) Verificando soma total...")
    
    total_cobertura = len(cidades_izafer_normalized) + len(cidades_zier_normalized)
    if total_cobertura == len(todas_cidades_sc) and sem_sobreposicao:
        print(f"      ✅ Soma total correta: {total_cobertura}/{len(todas_cidades_sc)} cidades")
        soma_ok = True
    else:
        print(f"      ❌ Soma total incorreta: {total_cobertura}/{len(todas_cidades_sc)} cidades")
        soma_ok = False
    
    # 5. Relatório final
    print()
    print("=== RELATÓRIO FINAL ===")
    
    divisao_perfeita = izafer_ok and zier_ok and sem_sobreposicao and soma_ok
    
    if divisao_perfeita:
        print("🎉 SUCESSO! Terceira divisão regional de SC configurada perfeitamente!")
        print("   Cobertura: 100% do estado")
    else:
        print("⚠️  ATENÇÃO! Existem problemas na divisão:")
        if not izafer_ok:
            print("   - IZAFER não tem a lista específica correta")
        if not zier_ok:
            print("   - ZIER não tem as cidades restantes corretas")
        if not sem_sobreposicao:
            print("   - Há sobreposição entre representantes")
        if not soma_ok:
            print("   - A soma total não confere")
    
    # 6. Estatísticas finais
    print()
    print("=== ESTATÍSTICAS FINAIS ===")
    print(f"Estado: SC (Santa Catarina)")
    print(f"Total de cidades: {len(todas_cidades_sc)}")
    print()
    print(f"IZAFER (37.0):")
    print(f"  Nome: {izafer_info['nome']}")
    print(f"  Cidades: {len(cidades_izafer_normalized)}")
    print(f"  Tipo: Lista específica")
    print()
    print(f"ZIER (35.01):")
    print(f"  Nome: {zier_info['nome']}")
    print(f"  Cidades: {len(cidades_zier_normalized)}")
    print(f"  Tipo: Resto do estado")
    
    if divisao_perfeita:
        print(f"\nCobertura: 100% ✅")
    else:
        cobertura_pct = (total_cobertura - len(sobreposicao)) / len(todas_cidades_sc) * 100
        print(f"\nCobertura: {cobertura_pct:.1f}% ⚠️")
    
    return divisao_perfeita

if __name__ == "__main__":
    try:
        sucesso = validar_divisao_sc()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")