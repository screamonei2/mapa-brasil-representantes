#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que a divisão regional do Rio de Janeiro (RJ)
foi configurada corretamente entre os representantes MRB (52.0) e L323 (52.01).

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

def validar_divisao_rj():
    """
    Valida se a divisão regional do RJ foi configurada corretamente
    """
    print("=== VALIDAÇÃO DIVISÃO REGIONAL RJ ===")
    print()
    
    # 1. Carregar todas as cidades do RJ do arquivo de municípios
    print("1. Carregando cidades do RJ do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_rj = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'RJ':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_rj.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_rj = sorted(list(set(todas_cidades_rj)))
    print(f"   Total de cidades no RJ (municípios.json): {len(todas_cidades_rj)}")
    
    # 2. Carregar cidades dos representantes
    print("2. Carregando cidades dos representantes...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar representantes
    mrb_info = None
    l323_info = None
    
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '52.0':
            mrb_info = rep
        elif rep.get('codigo') == '52.01':
            l323_info = rep
    
    if not mrb_info:
        print("   ERRO: MRB (52.0) não encontrado!")
        return False
    
    if not l323_info:
        print("   ERRO: L323 (52.01) não encontrado!")
        return False
    
    # Verificar se ambos atendem RJ
    if 'RJ' not in mrb_info.get('estados', {}):
        print("   ERRO: MRB não atende RJ!")
        return False
    
    if 'RJ' not in l323_info.get('estados', {}):
        print("   ERRO: L323 não atende RJ!")
        return False
    
    cidades_mrb = mrb_info['estados']['RJ']['cidades']
    cidades_l323 = l323_info['estados']['RJ']['cidades']
    
    # Normalizar listas
    cidades_mrb_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_mrb]
    cidades_l323_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_l323]
    
    cidades_mrb_normalized = sorted(list(set(cidades_mrb_normalized)))
    cidades_l323_normalized = sorted(list(set(cidades_l323_normalized)))
    
    print(f"   MRB: {len(cidades_mrb_normalized)} cidades")
    print(f"   L323: {len(cidades_l323_normalized)} cidades")
    
    # 3. Validações principais
    print()
    print("3. Validações:")
    
    # Validação 1: MRB tem apenas Rio de Janeiro
    print("   a) Verificando se MRB tem apenas a capital...")
    
    capital_esperada = ['RIO DE JANEIRO']
    
    if cidades_mrb_normalized == capital_esperada:
        print("      ✅ MRB tem apenas Rio de Janeiro (capital)!")
        mrb_ok = True
    else:
        print("      ❌ MRB não tem apenas a capital:")
        print(f"         Atual: {cidades_mrb_normalized}")
        print(f"         Esperado: {capital_esperada}")
        mrb_ok = False
    
    # Validação 2: L323 tem todas as outras cidades
    print("   b) Verificando se L323 tem o resto do estado...")
    
    cidades_esperadas_l323 = []
    for cidade in todas_cidades_rj:
        if cidade not in capital_esperada:
            cidades_esperadas_l323.append(cidade)
    
    cidades_l323_faltantes = []
    for cidade in cidades_esperadas_l323:
        if cidade not in cidades_l323_normalized:
            cidades_l323_faltantes.append(cidade)
    
    cidades_l323_extras = []
    for cidade in cidades_l323_normalized:
        if cidade not in cidades_esperadas_l323:
            cidades_l323_extras.append(cidade)
    
    if len(cidades_l323_faltantes) == 0 and len(cidades_l323_extras) == 0:
        print("      ✅ L323 tem exatamente as cidades restantes!")
        l323_ok = True
    else:
        print("      ❌ L323 não tem as cidades restantes corretas:")
        if cidades_l323_faltantes:
            print(f"         Faltantes: {len(cidades_l323_faltantes)} cidades")
        if cidades_l323_extras:
            print(f"         Extras: {len(cidades_l323_extras)} cidades")
        l323_ok = False
    
    # Validação 3: Verificar sobreposição
    print("   c) Verificando sobreposição...")
    
    sobreposicao = []
    for cidade in cidades_mrb_normalized:
        if cidade in cidades_l323_normalized:
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
    
    total_cobertura = len(cidades_mrb_normalized) + len(cidades_l323_normalized)
    if total_cobertura == len(todas_cidades_rj) and sem_sobreposicao:
        print(f"      ✅ Soma total correta: {total_cobertura}/{len(todas_cidades_rj)} cidades")
        soma_ok = True
    else:
        print(f"      ❌ Soma total incorreta: {total_cobertura}/{len(todas_cidades_rj)} cidades")
        soma_ok = False
    
    # 5. Relatório final
    print()
    print("=== RELATÓRIO FINAL ===")
    
    divisao_perfeita = mrb_ok and l323_ok and sem_sobreposicao and soma_ok
    
    if divisao_perfeita:
        print("🎉 SUCESSO! Divisão regional do RJ configurada perfeitamente!")
        print("   Cobertura: 100% do estado")
    else:
        print("⚠️  ATENÇÃO! Existem problemas na divisão:")
        if not mrb_ok:
            print("   - MRB não tem apenas a capital")
        if not l323_ok:
            print("   - L323 não tem as cidades restantes corretas")
        if not sem_sobreposicao:
            print("   - Há sobreposição entre representantes")
        if not soma_ok:
            print("   - A soma total não confere")
    
    # 6. Estatísticas finais
    print()
    print("=== ESTATÍSTICAS FINAIS ===")
    print(f"Estado: RJ (Rio de Janeiro)")
    print(f"Total de cidades: {len(todas_cidades_rj)}")
    print()
    print(f"MRB (52.0):")
    print(f"  Nome: {mrb_info['nome']}")
    print(f"  Cidades: {len(cidades_mrb_normalized)}")
    print(f"  Tipo: Capital")
    print()
    print(f"L323 (52.01):")
    print(f"  Nome: {l323_info['nome']}")
    print(f"  Cidades: {len(cidades_l323_normalized)}")
    print(f"  Tipo: Resto do estado")
    
    if divisao_perfeita:
        print(f"\nCobertura: 100% ✅")
    else:
        cobertura_pct = (total_cobertura - len(sobreposicao)) / len(todas_cidades_rj) * 100
        print(f"\nCobertura: {cobertura_pct:.1f}% ⚠️")
    
    return divisao_perfeita

if __name__ == "__main__":
    try:
        sucesso = validar_divisao_rj()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")