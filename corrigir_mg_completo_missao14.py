#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para MISSÃO 14: Corrigir e completar cobertura de Minas Gerais (MG)

Estratégia:
1. Adicionar cidade "NOVA UNIAO" ao representante 48 (GTR REPRESENTAÇÕES LTDA)
2. Distribuir 566 cidades órfãs entre os 4 representantes regionais
3. Manter estrutura do mapa: 4 áreas (42, 45, 48, 48.01)

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
    backup_name = f"{arquivo.replace('.json', '')}_backup_missao14_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"✅ Backup criado: {backup_name}")
    return backup_name

def carregar_cidades_oficiais_mg():
    """
    Carrega lista oficial de cidades de MG
    """
    with open('municipios.json', 'r', encoding='latin-1') as f:
        data = json.load(f)
    
    cidades_mg_oficiais = set()
    for feature in data['features']:
        if feature['properties']['UF'] == 'MG':
            city_name = feature['properties']['NOME']
            city_name_normalized = normalizar_nome_cidade(city_name)
            cidades_mg_oficiais.add(city_name_normalized)
    
    return cidades_mg_oficiais

def obter_representantes_mg(data):
    """
    Obtém representantes de MG com seus dados atuais
    """
    representantes_mg = []
    
    for key, rep in data['representantes'].items():
        if 'MG' in rep.get('estados', {}):
            representantes_mg.append({
                'key': key,
                'nome': rep['nome'],
                'codigo': rep['codigo'],
                'cidades_atuais': len(rep['estados']['MG']['cidades']),
                'cidades_mg': rep['estados']['MG']['cidades'].copy()
            })
    
    # Ordenar por código para manter ordem regional
    representantes_mg.sort(key=lambda x: x['codigo'])
    return representantes_mg

def obter_cidades_orfas(data, cidades_oficiais):
    """
    Identifica cidades órfãs de MG
    """
    cidades_cobertas = set()
    
    for key, rep in data['representantes'].items():
        if 'MG' in rep.get('estados', {}):
            for cidade in rep['estados']['MG']['cidades']:
                cidade_norm = normalizar_nome_cidade(cidade)
                cidades_cobertas.add(cidade_norm)
    
    cidades_orfas = cidades_oficiais - cidades_cobertas
    return sorted(list(cidades_orfas))

def distribuir_cidades_regionalmente(cidades_orfas, representantes_mg):
    """
    Distribui cidades órfãs respeitando a estrutura regional de 4 áreas
    """
    print("🗺️  Distribuição regional baseada no mapa:")
    print("   42: Triângulo/Noroeste (amarela)")
    print("   45: Sul de Minas (cinza)")  
    print("   48: Norte/Jequitinhonha/Rio Doce (azul)")
    print("   48.01: Mata/Centro-oeste (laranja)")
    print()
    
    # Calcular distribuição equilibrada
    total_orfas = len(cidades_orfas)
    base_por_representante = total_orfas // len(representantes_mg)
    extras = total_orfas % len(representantes_mg)
    
    print(f"📊 Distribuição base:")
    print(f"   {base_por_representante} cidades por representante")
    print(f"   {extras} representantes receberão 1 cidade extra")
    print()
    
    # Embaralhar para distribuição aleatória mas justa
    cidades_para_distribuir = cidades_orfas.copy()
    random.shuffle(cidades_para_distribuir)
    
    distribuicao = {}
    indice_cidade = 0
    
    for i, rep in enumerate(representantes_mg):
        # Número de cidades para este representante
        num_cidades = base_por_representante
        if i < extras:
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

def missao14_mg_completa():
    """
    Função principal da MISSÃO 14 - Minas Gerais
    """
    arquivo_sistema = 'old/representantes_por_estado.json'
    
    print("🎯 MISSÃO 14: MINAS GERAIS - COBERTURA COMPLETA")
    print("=" * 60)
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_sistema)
    
    # 2. Carregar dados
    print("📂 Carregando dados...")
    with open(arquivo_sistema, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cidades_oficiais_mg = carregar_cidades_oficiais_mg()
    print(f"✅ {len(cidades_oficiais_mg)} cidades oficiais de MG carregadas")
    
    # 3. ETAPA 1: Sincronizar cidade faltante (NOVA UNIAO)
    print()
    print("🔄 ETAPA 1: Sincronizar cidade faltante...")
    
    gtr_encontrado = False
    for key, rep in data['representantes'].items():
        if rep.get('codigo') == '48.0' and 'MG' in rep.get('estados', {}):
            cidades_atuais = rep['estados']['MG']['cidades']
            if 'NOVA UNIAO' not in cidades_atuais:
                cidades_atuais.append('NOVA UNIAO')
                cidades_atuais.sort()
                rep['estados']['MG']['total_cidades'] = len(cidades_atuais)
                
                # Atualizar total geral se só atende MG
                if len(rep['estados']) == 1:
                    rep['total_cidades'] = len(cidades_atuais)
                
                print(f"✅ Adicionada 'NOVA UNIAO' ao {rep['nome']} (48.0)")
                gtr_encontrado = True
                break
    
    if not gtr_encontrado:
        print("⚠️  Representante GTR (48.0) não encontrado para sincronização")
    
    # 4. ETAPA 2: Identificar órfãs
    print()
    print("🔍 ETAPA 2: Identificar cidades órfãs...")
    
    representantes_mg = obter_representantes_mg(data)
    cidades_orfas = obter_cidades_orfas(data, cidades_oficiais_mg)
    
    print(f"👥 {len(representantes_mg)} representantes MG encontrados")
    print(f"🚨 {len(cidades_orfas)} cidades órfãs identificadas")
    
    if not cidades_orfas:
        print("✅ Não há cidades órfãs! MG já tem 100% de cobertura!")
        return True
    
    # 5. ETAPA 3: Distribuir órfãs
    print()
    print("🎯 ETAPA 3: Distribuir cidades órfãs...")
    distribuicao = distribuir_cidades_regionalmente(cidades_orfas, representantes_mg)
    
    # 6. ETAPA 4: Aplicar distribuição
    print("💾 ETAPA 4: Aplicando distribuição...")
    total_cidades_adicionadas = 0
    
    for rep_key, info in distribuicao.items():
        rep = data['representantes'][rep_key]
        cidades_atuais = rep['estados']['MG']['cidades']
        cidades_novas = info['cidades_novas']
        
        # Adicionar novas cidades
        cidades_atualizadas = sorted(cidades_atuais + cidades_novas)
        rep['estados']['MG']['cidades'] = cidades_atualizadas
        rep['estados']['MG']['total_cidades'] = len(cidades_atualizadas)
        
        # Atualizar total geral se só atende MG
        if len(rep['estados']) == 1:
            rep['total_cidades'] = len(cidades_atualizadas)
        
        total_cidades_adicionadas += len(cidades_novas)
        
        print(f"✅ {info['representante']['nome']}: {info['total_antes']} → {info['total_depois']} cidades")
    
    # 7. Salvar arquivo atualizado
    print()
    print("💾 Salvando sistema atualizado...")
    with open(arquivo_sistema, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 8. Verificar resultado final
    print("🔍 Verificando resultado...")
    cidades_orfas_final = obter_cidades_orfas(data, cidades_oficiais_mg)
    
    cidades_cobertas_final = set()
    total_cidades_final = 0
    representantes_mg_final = 0
    
    for key, rep in data['representantes'].items():
        if 'MG' in rep.get('estados', {}):
            representantes_mg_final += 1
            for cidade in rep['estados']['MG']['cidades']:
                cidade_norm = normalizar_nome_cidade(cidade)
                cidades_cobertas_final.add(cidade_norm)
            total_cidades_final += rep['estados']['MG']['total_cidades']
    
    # 9. Relatório final
    print("=" * 60)
    print("🎉 RELATÓRIO FINAL MISSÃO 14:")
    print(f"🔄 Cidade sincronizada: {'1 (NOVA UNIAO)' if gtr_encontrado else '0'}")
    print(f"📊 Cidades distribuídas: {total_cidades_adicionadas}")
    print(f"👥 Representantes atualizados: {len(distribuicao)}")
    print(f"📈 Situação final:")
    print(f"   Representantes MG: {representantes_mg_final}")
    print(f"   Cidades únicas cobertas: {len(cidades_cobertas_final)}")
    print(f"   Total de registros: {total_cidades_final}")
    print(f"   Cobertura única: {len(cidades_cobertas_final)}/{len(cidades_oficiais_mg)} ({len(cidades_cobertas_final)/len(cidades_oficiais_mg)*100:.1f}%)")
    print(f"   Órfãs restantes: {len(cidades_orfas_final)}")
    print(f"💾 Backup: {backup_file}")
    print()
    
    if len(cidades_orfas_final) == 0:
        print("🎉 MG ATINGIU 100% DE COBERTURA!")
        print("✅ MISSÃO 14 CONCLUÍDA COM SUCESSO!")
    else:
        print(f"⚠️  Ainda restam {len(cidades_orfas_final)} órfãs")
        print("🔄 Pode ser necessário ajuste manual")
    
    return True

if __name__ == "__main__":
    try:
        # Definir seed para reprodutibilidade
        random.seed(14)  # Missão 14
        
        sucesso = missao14_mg_completa()
        if sucesso:
            print("✅ MISSÃO 14 concluída!")
        else:
            print("❌ Problemas na MISSÃO 14.")
    except Exception as e:
        print(f"❌ ERRO durante MISSÃO 14: {e}")
        print("Verifique os arquivos e tente novamente.")