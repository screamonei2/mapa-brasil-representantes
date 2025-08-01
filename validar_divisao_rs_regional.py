#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validação para confirmar que a divisão regional do Rio Grande do Sul (RS)
foi configurada corretamente entre os representantes ATTEX (29.01) e MYRALP (28.0).

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

def obter_lista_especifica_esperada():
    """
    Retorna a lista específica esperada para o representante 29.01
    """
    cidades_esperadas_raw = [
        'Estância Velha', 'Araricá', 'Sapiranga', 'São Leopoldo', 'Esteio', 
        'Dois Irmãos', 'Sapucaia do Sul', 'Campo Bom', 'Cachoeirinha', 'Ivoti', 
        'Nova Hartz', 'Parobé', 'Taquara', 'Rolante', 'Santo Antônio da Patrulha', 
        'Glorinha', 'Gravataí', 'Alvorada', 'Viamão', 'Porto Alegre', 'Canoas', 
        'Nova Santa Rita', 'Portão', 'Capela de Santana', 'Montenegro', 'Triunfo', 
        'Charqueadas', 'Eldorado do Sul', 'Guaíba', 'Arroio dos Ratos', 'São Jerônimo', 
        'Novo Hamburgo'
    ]
    
    # Normalizar a lista
    cidades_esperadas = []
    for cidade in cidades_esperadas_raw:
        cidade_norm = normalizar_nome_cidade(cidade)
        cidades_esperadas.append(cidade_norm)
    
    return sorted(cidades_esperadas)

def validar_divisao_rs():
    """
    Valida se a divisão regional do RS foi configurada corretamente
    """
    print("=== VALIDAÇÃO DIVISÃO REGIONAL RS ===")
    print()
    
    # 1. Carregar todas as cidades do RS do arquivo de municípios
    print("1. Carregando cidades do RS do arquivo municípios.json...")
    with open('municipios.json', 'r', encoding='latin-1') as f:
        municipios_data = json.load(f)
    
    todas_cidades_rs = []
    for feature in municipios_data['features']:
        if feature['properties']['UF'] == 'RS':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            todas_cidades_rs.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    todas_cidades_rs = sorted(list(set(todas_cidades_rs)))
    print(f"   Total de cidades no RS (municípios.json): {len(todas_cidades_rs)}")
    
    # 2. Obter lista específica esperada
    cidades_esperadas_rep29 = obter_lista_especifica_esperada()
    print(f"   Lista específica esperada para rep 29.01: {len(cidades_esperadas_rep29)} cidades")
    
    # 3. Carregar cidades dos representantes
    print("2. Carregando cidades dos representantes...")
    with open('old/representantes_por_estado.json', 'r', encoding='utf-8') as f:
        rep_data = json.load(f)
    
    # Encontrar representantes
    attex_info = None
    myralp_info = None
    
    for key, rep in rep_data['representantes'].items():
        if rep.get('codigo') == '29.01':
            attex_info = rep
        elif rep.get('codigo') == '28.0':
            myralp_info = rep
    
    if not attex_info:
        print("   ERRO: ATTEX (29.01) não encontrado!")
        return False
    
    if not myralp_info:
        print("   ERRO: MYRALP (28.0) não encontrado!")
        return False
    
    # Verificar se ambos atendem RS
    if 'RS' not in attex_info.get('estados', {}):
        print("   ERRO: ATTEX não atende RS!")
        return False
    
    if 'RS' not in myralp_info.get('estados', {}):
        print("   ERRO: MYRALP não atende RS!")
        return False
    
    cidades_attex = attex_info['estados']['RS']['cidades']
    cidades_myralp = myralp_info['estados']['RS']['cidades']
    
    # Normalizar listas
    cidades_attex_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_attex]
    cidades_myralp_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_myralp]
    
    cidades_attex_normalized = sorted(list(set(cidades_attex_normalized)))
    cidades_myralp_normalized = sorted(list(set(cidades_myralp_normalized)))
    
    print(f"   ATTEX: {len(cidades_attex_normalized)} cidades")
    print(f"   MYRALP: {len(cidades_myralp_normalized)} cidades")
    
    # 4. Validações principais
    print()
    print("3. Validações:")
    
    # Validação 1: ATTEX tem a lista específica correta
    print("   a) Verificando lista específica do ATTEX...")
    
    cidades_attex_faltantes = []
    for cidade in cidades_esperadas_rep29:
        if cidade not in cidades_attex_normalized:
            cidades_attex_faltantes.append(cidade)
    
    cidades_attex_extras = []
    for cidade in cidades_attex_normalized:
        if cidade not in cidades_esperadas_rep29:
            cidades_attex_extras.append(cidade)
    
    if len(cidades_attex_faltantes) == 0 and len(cidades_attex_extras) == 0:
        print("      ✅ ATTEX tem exatamente a lista específica correta!")
        attex_ok = True
    else:
        print("      ❌ ATTEX não tem a lista específica correta:")
        if cidades_attex_faltantes:
            print(f"         Faltantes: {cidades_attex_faltantes}")
        if cidades_attex_extras:
            print(f"         Extras: {cidades_attex_extras}")
        attex_ok = False
    
    # Validação 2: MYRALP tem todas as outras cidades
    print("   b) Verificando se MYRALP tem o resto do estado...")
    
    cidades_esperadas_myralp = []
    for cidade in todas_cidades_rs:
        if cidade not in cidades_esperadas_rep29:
            cidades_esperadas_myralp.append(cidade)
    
    cidades_myralp_faltantes = []
    for cidade in cidades_esperadas_myralp:
        if cidade not in cidades_myralp_normalized:
            cidades_myralp_faltantes.append(cidade)
    
    cidades_myralp_extras = []
    for cidade in cidades_myralp_normalized:
        if cidade not in cidades_esperadas_myralp:
            cidades_myralp_extras.append(cidade)
    
    if len(cidades_myralp_faltantes) == 0 and len(cidades_myralp_extras) == 0:
        print("      ✅ MYRALP tem exatamente as cidades restantes!")
        myralp_ok = True
    else:
        print("      ❌ MYRALP não tem as cidades restantes corretas:")
        if cidades_myralp_faltantes:
            print(f"         Faltantes: {len(cidades_myralp_faltantes)} cidades")
        if cidades_myralp_extras:
            print(f"         Extras: {len(cidades_myralp_extras)} cidades")
        myralp_ok = False
    
    # Validação 3: Verificar sobreposição
    print("   c) Verificando sobreposição...")
    
    sobreposicao = []
    for cidade in cidades_attex_normalized:
        if cidade in cidades_myralp_normalized:
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
    
    total_cobertura = len(cidades_attex_normalized) + len(cidades_myralp_normalized)
    if total_cobertura == len(todas_cidades_rs) and sem_sobreposicao:
        print(f"      ✅ Soma total correta: {total_cobertura}/{len(todas_cidades_rs)} cidades")
        soma_ok = True
    else:
        print(f"      ❌ Soma total incorreta: {total_cobertura}/{len(todas_cidades_rs)} cidades")
        soma_ok = False
    
    # 5. Relatório final
    print()
    print("=== RELATÓRIO FINAL ===")
    
    divisao_perfeita = attex_ok and myralp_ok and sem_sobreposicao and soma_ok
    
    if divisao_perfeita:
        print("🎉 SUCESSO! Divisão regional do RS configurada perfeitamente!")
        print("   Cobertura: 100% do estado")
    else:
        print("⚠️  ATENÇÃO! Existem problemas na divisão:")
        if not attex_ok:
            print("   - ATTEX não tem a lista específica correta")
        if not myralp_ok:
            print("   - MYRALP não tem as cidades restantes corretas")
        if not sem_sobreposicao:
            print("   - Há sobreposição entre representantes")
        if not soma_ok:
            print("   - A soma total não confere")
    
    # 6. Estatísticas finais
    print()
    print("=== ESTATÍSTICAS FINAIS ===")
    print(f"Estado: RS (Rio Grande do Sul)")
    print(f"Total de cidades: {len(todas_cidades_rs)}")
    print()
    print(f"ATTEX (29.01):")
    print(f"  Nome: {attex_info['nome']}")
    print(f"  Cidades: {len(cidades_attex_normalized)}")
    print(f"  Tipo: Região específica (metropolitana)")
    print()
    print(f"MYRALP (28.0):")
    print(f"  Nome: {myralp_info['nome']}")
    print(f"  Cidades: {len(cidades_myralp_normalized)}")
    print(f"  Tipo: Resto do estado")
    
    if divisao_perfeita:
        print(f"\nCobertura: 100% ✅")
    else:
        cobertura_pct = (total_cobertura - len(sobreposicao)) / len(todas_cidades_rs) * 100
        print(f"\nCobertura: {cobertura_pct:.1f}% ⚠️")
    
    return divisao_perfeita

if __name__ == "__main__":
    try:
        sucesso = validar_divisao_rs()
        print()
        if sucesso:
            print("✅ Validação concluída com sucesso!")
        else:
            print("❌ Validação encontrou problemas.")
    except Exception as e:
        print(f"ERRO durante a validação: {e}")