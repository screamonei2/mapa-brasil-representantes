#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para FASE 3: Distribuir cidades órfãs entre representantes de SP

MISSÃO 13 - FASE 3: Completar cobertura

Autor: Assistente AI
Data: $(date +%Y-%m-%d)
"""

import json
import shutil
from datetime import datetime
import unicodedata
import re
import random

def normalizar_nome_cidade(nome):
    """
    Normaliza nomes de cidades removendo acentos e caracteres especiais
    """
    nome = unicodedata.normalize('NFD', nome)
    nome = ''.join(char for char in nome if unicodedata.category(char) != 'Mn')
    nome = nome.upper()
    nome = re.sub(r'[^A-Z0-9\s\-\']', '', nome)
    nome = ' '.join(nome.split())
    return nome

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_fase3_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"✅ Backup criado: {backup_name}")
    return backup_name

def carregar_cidades_oficiais_sp():
    """
    Carrega lista oficial de cidades de SP
    """
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    cidades_sp_oficiais = set()
    for feature in data['features']:
        if feature['properties']['UF'] == 'SP':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            cidades_sp_oficiais.add(city_name_normalized)
    
    return cidades_sp_oficiais

def obter_cidades_orfas(data, cidades_oficiais):
    """
    Identifica cidades órfãs que não estão sendo atendidas
    """
    cidades_cobertas = set()
    
    for key, rep in data['representantes'].items():
        if 'SP' in rep.get('estados', {}):
            for cidade in rep['estados']['SP']['cidades']:
                cidade_norm = normalizar_nome_cidade(cidade)
                cidades_cobertas.add(cidade_norm)
    
    cidades_orfas = cidades_oficiais - cidades_cobertas
    return sorted(list(cidades_orfas))

def obter_representantes_sp(data):
    """
    Obtém lista de representantes que atendem SP com seus dados
    """
    representantes_sp = []
    
    for key, rep in data['representantes'].items():
        if 'SP' in rep.get('estados', {}):
            cidades_atuais = len(rep['estados']['SP']['cidades'])
            representantes_sp.append({
                'key': key,
                'nome': rep['nome'],
                'codigo': rep['codigo'],
                'cidades_atuais': cidades_atuais,
                'cidades_sp': rep['estados']['SP']['cidades'].copy()
            })
    
    # Ordenar por número de cidades (menores primeiro para equilibrar)
    representantes_sp.sort(key=lambda x: x['cidades_atuais'])
    return representantes_sp

def distribuir_cidades_inteligente(cidades_orfas, representantes_sp):
    """
    Distribui cidades órfãs de forma equilibrada entre representantes
    """
    print("🧠 Algoritmo de distribuição inteligente:")
    print(f"   Cidades a distribuir: {len(cidades_orfas)}")
    print(f"   Representantes disponíveis: {len(representantes_sp)}")
    print()
    
    # Calcular distribuição base
    cidades_por_rep = len(cidades_orfas) // len(representantes_sp)
    cidades_extras = len(cidades_orfas) % len(representantes_sp)
    
    print(f"📊 Distribuição base:")
    print(f"   {cidades_por_rep} cidades por representante")
    print(f"   {cidades_extras} representantes receberão 1 cidade extra")
    print()
    
    # Embaralhar cidades para distribuição aleatória mas justa
    cidades_para_distribuir = cidades_orfas.copy()
    random.shuffle(cidades_para_distribuir)
    
    distribuicao = {}
    indice_cidade = 0
    
    for i, rep in enumerate(representantes_sp):
        # Número de cidades para este representante
        num_cidades = cidades_por_rep
        if i < cidades_extras:
            num_cidades += 1
        
        # Selecionar cidades
        cidades_para_rep = cidades_para_distribuir[indice_cidade:indice_cidade + num_cidades]
        distribuicao[rep['key']] = {
            'representante': rep,
            'cidades_novas': cidades_para_rep,
            'total_antes': rep['cidades_atuais'],
            'total_depois': rep['cidades_atuais'] + len(cidades_para_rep)
        }
        
        indice_cidade += num_cidades
        
        print(f"📋 {rep['nome']} ({rep['codigo']}):")
        print(f"   Antes: {rep['cidades_atuais']} cidades")
        print(f"   Adicionando: {len(cidades_para_rep)} cidades")
        print(f"   Depois: {rep['cidades_atuais'] + len(cidades_para_rep)} cidades")
        print()
    
    return distribuicao

def fase3_distribuir_orfas():
    """
    Função principal da FASE 3
    """
    arquivo_sistema = 'old/representantes_por_estado.json'
    
    print("🎯 FASE 3: DISTRIBUIR CIDADES ÓRFÃS")
    print("=" * 60)
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_sistema)
    
    # 2. Carregar dados
    print("📂 Carregando dados...")
    with open(arquivo_sistema, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cidades_oficiais_sp = carregar_cidades_oficiais_sp()
    print(f"✅ {len(cidades_oficiais_sp)} cidades oficiais de SP carregadas")
    
    # 3. Identificar órfãs
    cidades_orfas = obter_cidades_orfas(data, cidades_oficiais_sp)
    print(f"🚨 {len(cidades_orfas)} cidades órfãs identificadas")
    
    if not cidades_orfas:
        print("✅ Não há cidades órfãs! SP já tem 100% de cobertura!")
        return True
    
    # 4. Obter representantes
    representantes_sp = obter_representantes_sp(data)
    print(f"👥 {len(representantes_sp)} representantes de SP encontrados")
    
    # 5. Distribuir cidades
    print("🔄 Iniciando distribuição...")
    distribuicao = distribuir_cidades_inteligente(cidades_orfas, representantes_sp)
    
    # 6. Aplicar distribuição
    print("💾 Aplicando distribuição ao sistema...")
    total_cidades_adicionadas = 0
    
    for rep_key, info in distribuicao.items():
        rep = data['representantes'][rep_key]
        cidades_atuais = rep['estados']['SP']['cidades']
        cidades_novas = info['cidades_novas']
        
        # Adicionar novas cidades
        cidades_atualizadas = sorted(cidades_atuais + cidades_novas)
        rep['estados']['SP']['cidades'] = cidades_atualizadas
        rep['estados']['SP']['total_cidades'] = len(cidades_atualizadas)
        
        # Atualizar total geral se só atende SP
        if len(rep['estados']) == 1:
            rep['total_cidades'] = len(cidades_atualizadas)
        
        total_cidades_adicionadas += len(cidades_novas)
        
        print(f"✅ {info['representante']['nome']}: {info['total_antes']} → {info['total_depois']} cidades")
    
    # 7. Salvar arquivo atualizado
    print("💾 Salvando sistema atualizado...")
    with open(arquivo_sistema, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 8. Verificar resultado final
    print("🔍 Verificando resultado...")
    cidades_orfas_final = obter_cidades_orfas(data, cidades_oficiais_sp)
    
    cidades_cobertas_final = set()
    total_cidades_final = 0
    representantes_sp_final = 0
    
    for key, rep in data['representantes'].items():
        if 'SP' in rep.get('estados', {}):
            representantes_sp_final += 1
            for cidade in rep['estados']['SP']['cidades']:
                cidade_norm = normalizar_nome_cidade(cidade)
                cidades_cobertas_final.add(cidade_norm)
            total_cidades_final += rep['estados']['SP']['total_cidades']
    
    # 9. Relatório final
    print("=" * 60)
    print("🎉 RELATÓRIO FINAL FASE 3:")
    print(f"📊 Cidades distribuídas: {total_cidades_adicionadas}")
    print(f"👥 Representantes atualizados: {len(distribuicao)}")
    print(f"📈 Situação final:")
    print(f"   Representantes SP: {representantes_sp_final}")
    print(f"   Cidades únicas cobertas: {len(cidades_cobertas_final)}")
    print(f"   Total de registros: {total_cidades_final}")
    print(f"   Cobertura única: {len(cidades_cobertas_final)}/645 ({len(cidades_cobertas_final)/645*100:.1f}%)")
    print(f"   Órfãs restantes: {len(cidades_orfas_final)}")
    print(f"💾 Backup: {backup_file}")
    print()
    
    if len(cidades_orfas_final) == 0:
        print("🎉 SP ATINGIU 100% DE COBERTURA!")
        print("✅ MISSÃO 13 CONCLUÍDA COM SUCESSO!")
        print("🎯 PRÓXIMO: FASE 4 - Relatórios finais")
    else:
        print(f"⚠️  Ainda restam {len(cidades_orfas_final)} órfãs")
        print("🔄 Pode ser necessário ajuste manual")
    
    return True

if __name__ == "__main__":
    try:
        # Definir seed para reprodutibilidade
        random.seed(42)
        
        sucesso = fase3_distribuir_orfas()
        if sucesso:
            print("✅ FASE 3 concluída!")
        else:
            print("❌ Problemas na FASE 3.")
    except Exception as e:
        print(f"❌ ERRO durante FASE 3: {e}")
        print("Verifique os arquivos e tente novamente.")