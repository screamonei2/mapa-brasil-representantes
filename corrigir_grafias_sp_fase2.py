#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para FASE 2: Corrigir grafias incorretas e eliminar duplicatas em SP

MISSÃO 13 - FASE 2: Correções de dados

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
    backup_name = f"{arquivo.replace('.json', '')}_backup_fase2_{timestamp}.json"
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

def corrigir_grafias_conhecidas(cidade):
    """
    Corrige grafias conhecidas que são incorretas
    """
    correcoes = {
        'EMBU DAS ARTES': 'EMBU',
        'ESTRELA D OESTE': 'ESTRELA D\'OESTE',
        'JACARE': 'JACAREI',
        'JUNDIA': 'JUNDIAI',
        'PALMEIRA D OESTE': 'PALMEIRA D\'OESTE',
        'SANTA BARBARA D OESTE': 'SANTA BARBARA D\'OESTE',
        'SANTA CLARA D OESTE': 'SANTA CLARA D\'OESTE',
        # Mogi Mirim está correto, não precisa corrigir
        # Primavera precisa ser verificado
    }
    return correcoes.get(cidade, cidade)

def fase2_corrigir_dados():
    """
    Função principal da FASE 2
    """
    arquivo_sistema = 'old/representantes_por_estado.json'
    
    print("🔧 FASE 2: CORREÇÕES DE DADOS SP")
    print("=" * 50)
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_sistema)
    
    # 2. Carregar dados
    print("📂 Carregando dados...")
    with open(arquivo_sistema, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cidades_oficiais_sp = carregar_cidades_oficiais_sp()
    print(f"✅ {len(cidades_oficiais_sp)} cidades oficiais de SP carregadas")
    
    # 3. Analisar e corrigir cada representante
    print()
    print("🔍 ANÁLISE POR REPRESENTANTE:")
    print("-" * 40)
    
    total_correcoes = 0
    total_duplicatas = 0
    total_invalidas = 0
    representantes_corrigidos = 0
    
    for key, rep in data['representantes'].items():
        if 'SP' in rep.get('estados', {}):
            cidades_atuais = rep['estados']['SP']['cidades']
            cidades_corrigidas = []
            correcoes_rep = []
            invalidas_rep = []
            
            print(f"📋 {rep['nome']} ({rep['codigo']})")
            print(f"   Cidades atuais: {len(cidades_atuais)}")
            
            for cidade in cidades_atuais:
                # Aplicar correções conhecidas
                cidade_corrigida = corrigir_grafias_conhecidas(cidade)
                if cidade_corrigida != cidade:
                    correcoes_rep.append(f"{cidade} → {cidade_corrigida}")
                    total_correcoes += 1
                
                # Normalizar para verificação
                cidade_norm = normalizar_nome_cidade(cidade_corrigida)
                
                # Verificar se é válida
                if cidade_norm in cidades_oficiais_sp:
                    # Verificar duplicatas
                    if cidade_corrigida not in cidades_corrigidas:
                        cidades_corrigidas.append(cidade_corrigida)
                    else:
                        total_duplicatas += 1
                        print(f"   🔄 Duplicata removida: {cidade_corrigida}")
                else:
                    invalidas_rep.append(cidade)
                    total_invalidas += 1
            
            # Mostrar correções desta representante
            if correcoes_rep:
                print(f"   ✏️  Correções ({len(correcoes_rep)}):")
                for corr in correcoes_rep:
                    print(f"      {corr}")
            
            if invalidas_rep:
                print(f"   ❌ Inválidas ({len(invalidas_rep)}): {invalidas_rep}")
            
            # Atualizar se houve mudanças
            if len(cidades_corrigidas) != len(cidades_atuais) or correcoes_rep:
                rep['estados']['SP']['cidades'] = sorted(cidades_corrigidas)
                rep['estados']['SP']['total_cidades'] = len(cidades_corrigidas)
                
                # Atualizar total geral se só atende SP
                if len(rep['estados']) == 1:
                    rep['total_cidades'] = len(cidades_corrigidas)
                
                representantes_corrigidos += 1
                print(f"   ✅ Atualizado: {len(cidades_corrigidas)} cidades")
            else:
                print(f"   ✅ Já correto")
            
            print()
    
    # 4. Salvar arquivo corrigido
    print("💾 Salvando correções...")
    with open(arquivo_sistema, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 5. Verificar resultado
    print("🔍 Verificando resultado...")
    total_cidades_final = 0
    representantes_sp_final = 0
    
    for key, rep in data['representantes'].items():
        if 'SP' in rep.get('estados', {}):
            representantes_sp_final += 1
            total_cidades_final += rep['estados']['SP']['total_cidades']
    
    # 6. Relatório final
    print("=" * 50)
    print("📊 RELATÓRIO FASE 2:")
    print(f"✏️  Grafias corrigidas: {total_correcoes}")
    print(f"🔄 Duplicatas removidas: {total_duplicatas}")
    print(f"❌ Cidades inválidas: {total_invalidas}")
    print(f"👥 Representantes corrigidos: {representantes_corrigidos}")
    print(f"📊 Situação final:")
    print(f"   Representantes SP: {representantes_sp_final}")
    print(f"   Total cidades: {total_cidades_final}")
    print(f"   Cobertura: {total_cidades_final}/645 ({total_cidades_final/645*100:.1f}%)")
    print(f"💾 Backup: {backup_file}")
    print()
    
    if total_cidades_final <= 645:
        cidades_faltantes = 645 - total_cidades_final
        print(f"🎯 PRÓXIMO: FASE 3 - Adicionar {cidades_faltantes} cidades órfãs")
        print("✅ FASE 2 CONCLUÍDA!")
    else:
        sobreposicao = total_cidades_final - 645
        print(f"⚠️  Ainda há {sobreposicao} cidades em sobreposição")
        print("🔄 Pode ser necessária análise adicional")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = fase2_corrigir_dados()
        if sucesso:
            print("✅ FASE 2 concluída com sucesso!")
        else:
            print("❌ Problemas na FASE 2.")
    except Exception as e:
        print(f"❌ ERRO durante FASE 2: {e}")
        print("Verifique os arquivos e tente novamente.")