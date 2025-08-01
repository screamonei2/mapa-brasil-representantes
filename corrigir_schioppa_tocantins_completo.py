#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir e adicionar TODAS as cidades do Tocantins (TO)
para o representante Schioppa (ID 01).

Autor: Assistente AI
Data: $(date +%Y-%m-%d)
"""

import json
import shutil
from datetime import datetime
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

def carregar_cidades_to():
    """
    Carrega todas as cidades do Tocantins do arquivo municipios.json
    """
    print("Carregando todas as cidades do Tocantins...")
    
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    to_cities = []
    for feature in data['features']:
        if feature['properties']['UF'] == 'TO':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            to_cities.append(city_name_normalized)
    
    # Remove duplicatas e ordena
    to_cities = sorted(list(set(to_cities)))
    
    print(f"Total de cidades encontradas no TO: {len(to_cities)}")
    return to_cities

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_schioppa_to_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"Backup criado: {backup_name}")
    return backup_name

def corrigir_schioppa_to():
    """
    Função principal para adicionar todas as cidades do TO ao representante Schioppa
    """
    arquivo_representantes = 'old/representantes_por_estado.json'
    
    print("=== Correção Schioppa TO - Todas as Cidades ===")
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_representantes)
    
    # 2. Carregar todas as cidades do TO
    todas_cidades_to = carregar_cidades_to()
    
    # 3. Carregar arquivo de representantes
    print("Carregando arquivo de representantes...")
    with open(arquivo_representantes, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 4. Encontrar o representante Schioppa
    schioppa_key = None
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '01':
            schioppa_key = key
            break
    
    if not schioppa_key:
        print("ERRO: Representante Schioppa (código 01) não encontrado!")
        return False
    
    print(f"Representante encontrado: {data['representantes'][schioppa_key]['nome']}")
    
    # 5. Verificar situação atual
    rep_info = data['representantes'][schioppa_key]
    estados_atuais = list(rep_info['estados'].keys())
    cidades_totais_atuais = rep_info['total_cidades']
    
    print(f"Estados atuais: {estados_atuais}")
    print(f"Total de cidades atuais: {cidades_totais_atuais}")
    
    # 6. Verificar se TO já existe
    if 'TO' in rep_info['estados']:
        print(f"TO já existe - cidades atuais: {len(rep_info['estados']['TO']['cidades'])}")
        cidades_atuais_to = rep_info['estados']['TO']['cidades']
        cidades_atuais_to_normalized = [normalizar_nome_cidade(cidade) for cidade in cidades_atuais_to]
    else:
        print("TO não existe - será criado do zero")
        cidades_atuais_to_normalized = []
    
    # 7. Identificar cidades faltantes
    cidades_faltantes = []
    for cidade in todas_cidades_to:
        if cidade not in cidades_atuais_to_normalized:
            cidades_faltantes.append(cidade)
    
    print(f"Cidades faltantes no TO: {len(cidades_faltantes)}")
    
    if len(cidades_faltantes) == 0:
        print("Schioppa já atende todas as cidades do TO!")
        return True
    
    # 8. Mostrar relatório detalhado
    print()
    print("=== RELATÓRIO DETALHADO ===")
    print()
    if 'TO' in rep_info['estados']:
        print("Cidades atuais do Schioppa no TO:")
        for i, cidade in enumerate(sorted(cidades_atuais_to_normalized), 1):
            print(f"  {i:3d}. {cidade}")
    else:
        print("Schioppa não atende nenhuma cidade do TO atualmente.")
    
    print()
    print("Cidades faltantes a serem adicionadas:")
    for i, cidade in enumerate(sorted(cidades_faltantes), 1):
        print(f"  {i:3d}. {cidade}")
    
    # 9. Confirmar alteração
    print()
    resposta = input(f"Confirma a adição de {len(cidades_faltantes)} cidades do TO ao Schioppa? (s/N): ").strip().lower()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Operação cancelada pelo usuário.")
        return False
    
    # 10. Atualizar lista de cidades do TO
    todas_cidades_to_final = sorted(list(set(cidades_atuais_to_normalized + cidades_faltantes)))
    
    # 11. Atualizar dados do representante
    # Criar/atualizar estado TO
    rep_info['estados']['TO'] = {
        'cidades': todas_cidades_to_final,
        'total_cidades': len(todas_cidades_to_final)
    }
    
    # Adicionar TO aos estados atendidos se não existir
    if 'TO   ' not in rep_info['estados_atendidos']:
        rep_info['estados_atendidos'].append('TO   ')
        rep_info['estados_atendidos'].sort()
    
    # Recalcular total de cidades
    total_cidades_novo = 0
    for estado, info in rep_info['estados'].items():
        total_cidades_novo += info['total_cidades']
    
    rep_info['total_cidades'] = total_cidades_novo
    
    # 12. Salvar arquivo atualizado
    print()
    print("Salvando arquivo atualizado...")
    with open(arquivo_representantes, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 13. Relatório final
    print()
    print("=== CORREÇÃO CONCLUÍDA ===")
    print(f"Representante: {rep_info['nome']}")
    print(f"Código: {rep_info['codigo']}")
    print(f"Estado adicionado: TO (Tocantins)")
    print(f"Cidades no TO antes: {len(cidades_atuais_to_normalized)}")
    print(f"Cidades adicionadas: {len(cidades_faltantes)}")
    print(f"Total no TO agora: {len(todas_cidades_to_final)}")
    print(f"Total geral de cidades: {total_cidades_novo}")
    print(f"Estados atendidos: {len(rep_info['estados_atendidos'])}")
    print(f"Arquivo atualizado: {arquivo_representantes}")
    print(f"Backup salvo em: {backup_file}")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = corrigir_schioppa_to()
        if sucesso:
            print()
            print("Script executado com sucesso!")
        else:
            print()
            print("Script finalizado com problemas.")
    except Exception as e:
        print(f"ERRO durante a execução: {e}")
        print("Verifique os arquivos e tente novamente.")