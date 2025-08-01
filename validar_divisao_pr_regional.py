#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que a divisão regional do Paraná (PR)
foi configurada corretamente entre os representantes ROUND (36.01) e LIBER (40.01).

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

def validar_divisao_pr():
    """
    Valida se a divisão regional do PR foi configurada corretamente
    """
    print("=== VALIDAÇÃO QUARTA DIVISÃO REGIONAL PR ===")
    print()
    
    # 1. Carregar todas as cidades do PR do arquivo de municípios
    print("1. Carregando cidades do PR do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_pr = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'PR':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_pr.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_pr = sorted(list(set(todas_cidades_pr)))
    print(f"   Total de cidades no PR (municípios.json): {len(todas_cidades_pr)}")
    
    # 2. Carregar cidades dos representantes
    print("2. Carregando cidades dos representantes...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar representantes
    round_info = None
    liber_info = None
    
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '36.01':
            round_info = rep
        elif rep.get('codigo') == '40.01':
            liber_info = rep
    
    if not round_info:
        print("   ERRO: ROUND (36.01) não encontrado!")
        return False
    
    if not liber_info:
        print("   ERRO: LIBER (40.01) não encontrado!")
        return False
    
    # Verificar se ambos atendem PR
    if 'PR' not in round_info.get('estados', {}):
        print("   ERRO: ROUND não atende PR!")
        return False
    
    if 'PR' not in liber_info.get('estados', {}):
        print("   ERRO: LIBER não atende PR!")
        return False
    
    cidades_round = round_info['estados']['PR']['cidades']
    cidades_liber = liber_info['estados']['PR']['cidades']
    
    # Normalizar listas
    cidades_round_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_round]
    cidades_liber_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_liber]
    
    cidades_round_normalized = sorted(list(set(cidades_round_normalized)))
    cidades_liber_normalized = sorted(list(set(cidades_liber_normalized)))
    
    print(f"   ROUND: {len(cidades_round_normalized)} cidades")
    print(f"   LIBER: {len(cidades_liber_normalized)} cidades")
    
    # 3. Validações principais
    print()
    print("3. Validações:")
    
    # Validação 1: ROUND tem lista específica
    print("   a) Verificando se ROUND tem a lista específica...")
    
    lista_esperada_round = [
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
    
    # Normalizar lista esperada
    lista_esperada_round_norm = [normalizar_nome_cidade(cidade) for cidade in lista_esperada_round]
    lista_esperada_round_norm = sorted(list(set(lista_esperada_round_norm)))
    
    if cidades_round_normalized == lista_esperada_round_norm:
        print("      ✅ ROUND tem exatamente a lista específica!")
        round_ok = True
    else:
        print("      ❌ ROUND não tem a lista específica correta:")
        print(f"         Atual: {len(cidades_round_normalized)} cidades")
        print(f"         Esperado: {len(lista_esperada_round_norm)} cidades")
        round_ok = False
    
    # Validação 2: LIBER tem todas as outras cidades
    print("   b) Verificando se LIBER tem o resto do estado...")
    
    cidades_esperadas_liber = []
    for cidade in todas_cidades_pr:
        if cidade not in lista_esperada_round_norm:
            cidades_esperadas_liber.append(cidade)
    
    cidades_liber_faltantes = []
    for cidade in cidades_esperadas_liber:
        if cidade not in cidades_liber_normalized:
            cidades_liber_faltantes.append(cidade)
    
    cidades_liber_extras = []
    for cidade in cidades_liber_normalized:
        if cidade not in cidades_esperadas_liber:
            cidades_liber_extras.append(cidade)
    
    if len(cidades_liber_faltantes) == 0 and len(cidades_liber_extras) == 0:
        print("      ✅ LIBER tem exatamente as cidades restantes!")
        liber_ok = True
    else:
        print("      ❌ LIBER não tem as cidades restantes corretas:")
        if cidades_liber_faltantes:
            print(f"         Faltantes: {len(cidades_liber_faltantes)} cidades")
        if cidades_liber_extras:
            print(f"         Extras: {len(cidades_liber_extras)} cidades")
        liber_ok = False
    
    # Validação 3: Verificar sobreposição
    print("   c) Verificando sobreposição...")
    
    sobreposicao = []
    for cidade in cidades_round_normalized:
        if cidade in cidades_liber_normalized:
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
    
    total_cobertura = len(cidades_round_normalized) + len(cidades_liber_normalized)
    if total_cobertura == len(todas_cidades_pr) and sem_sobreposicao:
        print(f"      ✅ Soma total correta: {total_cobertura}/{len(todas_cidades_pr)} cidades")
        soma_ok = True
    else:
        print(f"      ❌ Soma total incorreta: {total_cobertura}/{len(todas_cidades_pr)} cidades")
        soma_ok = False
    
    # 5. Relatório final
    print()
    print("=== RELATÓRIO FINAL ===")
    
    divisao_perfeita = round_ok and liber_ok and sem_sobreposicao and soma_ok
    
    if divisao_perfeita:
        print("🎉 SUCESSO! Quarta divisão regional do PR configurada perfeitamente!")
        print("   Cobertura: 100% do estado")
    else:
        print("⚠️  ATENÇÃO! Existem problemas na divisão:")
        if not round_ok:
            print("   - ROUND não tem a lista específica correta")
        if not liber_ok:
            print("   - LIBER não tem as cidades restantes corretas")
        if not sem_sobreposicao:
            print("   - Há sobreposição entre representantes")
        if not soma_ok:
            print("   - A soma total não confere")
    
    # 6. Estatísticas finais
    print()
    print("=== ESTATÍSTICAS FINAIS ===")
    print(f"Estado: PR (Paraná)")
    print(f"Total de cidades: {len(todas_cidades_pr)}")
    print()
    print(f"ROUND (36.01):")
    print(f"  Nome: {round_info['nome']}")
    print(f"  Cidades: {len(cidades_round_normalized)}")
    print(f"  Tipo: Lista específica")
    print()
    print(f"LIBER (40.01):")
    print(f"  Nome: {liber_info['nome']}")
    print(f"  Cidades: {len(cidades_liber_normalized)}")
    print(f"  Tipo: Resto do estado")
    
    if divisao_perfeita:
        print(f"\nCobertura: 100% ✅")
    else:
        cobertura_pct = (total_cobertura - len(sobreposicao)) / len(todas_cidades_pr) * 100
        print(f"\nCobertura: {cobertura_pct:.1f}% ⚠️")
    
    return divisao_perfeita

if __name__ == "__main__":
    try:
        sucesso = validar_divisao_pr()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")