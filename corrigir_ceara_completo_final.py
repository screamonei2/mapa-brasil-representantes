#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para correção completa do Ceará
Identifica todas as cidades do CE e remove de representantes que não tenham código 43.0
"""

import json
import os
from datetime import datetime

def extrair_cidades_ceara():
    """
    Extrai todas as cidades do Ceará - usando múltiplas estratégias
    """
    cidades_ce = set()
    
    # Estratégia 1: Tentar carregar municipios.json com diferentes codificações
    for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
        try:
            with open('old/municipios.json', 'r', encoding=encoding) as f:
                municipios = json.load(f)
            
            for municipio in municipios['features']:
                if municipio['properties']['UF'] == 'CE':
                    nome_cidade = municipio['properties']['NOME'].upper()
                    # Normalizar nomes (remover acentos comuns)
                    nome_cidade = nome_cidade.replace('Ã', 'A').replace('Õ', 'O').replace('Ç', 'C')
                    nome_cidade = nome_cidade.replace('É', 'E').replace('Í', 'I').replace('Ó', 'O')
                    nome_cidade = nome_cidade.replace('Ú', 'U').replace('Â', 'A').replace('Ê', 'E')
                    nome_cidade = nome_cidade.replace('Ô', 'O').replace('À', 'A')
                    cidades_ce.add(nome_cidade)
            
            print(f"✅ Arquivo carregado com codificação {encoding}")
            print(f"✅ Encontradas {len(cidades_ce)} cidades do Ceará")
            return cidades_ce
            
        except Exception as e:
            print(f"⚠️  Tentativa com {encoding} falhou: {str(e)[:100]}...")
            continue
    
    # Estratégia 2: Lista manual baseada no que já sabemos
    print("📋 Usando lista manual de cidades do Ceará...")
    cidades_ce_manual = {
        'ACARAPE', 'ACOPIARA', 'ALCANTARAS', 'AQUIRAZ', 'ARACATI', 'BARBALHA', 
        'BEBERIBE', 'CASCAVEL', 'CAUCAIA', 'CHOROZINHO', 'CRATO', 'EUSEBIO', 
        'FORQUILHA', 'FORTALEZA', 'FORTIM', 'HORIZONTE', 'ICAPUI', 'IGUATU', 
        'ITAITINGA', 'ITAPIPOCA', 'JAGUARIBE', 'JUAZEIRO DO NORTE', 
        'LIMOEIRO DO NORTE', 'MARACANAU', 'MARANGUAPE', 'MARCO', 'MAURITI', 
        'MISSAO VELHA', 'PACAJUS', 'PACATUBA', 'PARACURU', 'PENTECOSTE', 
        'QUIXADA', 'RUSSAS', 'SANTANA DO ACARAU', 'SAO GONCALO DO AMARANTE', 
        'SOBRAL', 'TIANGUA', 'TRAIRI', 'GRANJA', 'VIOSA DO CEARA', 'CHAVAL', 
        'BARROQUINHA', 'PORANGA'
    }
    
    print(f"✅ Lista manual: {len(cidades_ce_manual)} cidades do Ceará")
    return cidades_ce_manual

def corrigir_ceara_completo():
    """
    Correção completa: remove cidades do CE de representantes que não tenham código 43.0
    """
    
    print("=== CORREÇÃO COMPLETA CEARÁ - ANÁLISE DETALHADA ===")
    print(f"Processando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Extrair cidades do Ceará
    print("🔍 EXTRAINDO CIDADES DO CEARÁ...")
    cidades_ceara = extrair_cidades_ceara()
    
    if not cidades_ceara:
        print("❌ Não foi possível extrair cidades do Ceará")
        return
    
    print(f"📋 Cidades do Ceará: {sorted(list(cidades_ceara))}")
    print()
    
    # 2. Carregar dados dos representantes
    try:
        with open('representantes.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar representantes.json: {e}")
        return
    
    # 3. Analisar representantes
    print("🔍 ANALISANDO REPRESENTANTES...")
    representantes_problematicos = []
    cidades_removidas_total = []
    
    for estado, representantes in dados.items():
        for nome_rep, info_rep in representantes.items():
            codigo = info_rep.get('dados_contato', {}).get('codigo_representante', 'N/A')
            cidades_atendidas = info_rep.get('cidades_atendidas', [])
            
            # Verificar se atende cidades do Ceará
            cidades_ce_atendidas = []
            for cidade in cidades_atendidas:
                cidade_normalizada = cidade.upper()
                # Normalizar para comparação
                cidade_normalizada = cidade_normalizada.replace('Ã', 'A').replace('Õ', 'O').replace('Ç', 'C')
                cidade_normalizada = cidade_normalizada.replace('É', 'E').replace('Í', 'I').replace('Ó', 'O')
                cidade_normalizada = cidade_normalizada.replace('Ú', 'U').replace('Â', 'A').replace('Ê', 'E')
                cidade_normalizada = cidade_normalizada.replace('Ô', 'O').replace('À', 'A')
                
                if cidade_normalizada in cidades_ceara:
                    cidades_ce_atendidas.append(cidade)
            
            # Se atende cidades do CE mas não tem código 43.0
            if cidades_ce_atendidas and codigo != '43.0':
                representantes_problematicos.append({
                    'estado': estado,
                    'nome': nome_rep,
                    'codigo': codigo,
                    'cidades_ce': cidades_ce_atendidas
                })
    
    if not representantes_problematicos:
        print("✅ Nenhum representante problemático encontrado!")
        print("Todos os representantes que atendem cidades do Ceará têm código 43.0")
        return
    
    print(f"⚠️  ENCONTRADOS {len(representantes_problematicos)} REPRESENTANTES PROBLEMÁTICOS:")
    for rep in representantes_problematicos:
        print(f"  • {rep['nome']} (Estado: {rep['estado']}, Código: {rep['codigo']})")
        print(f"    Cidades do CE: {rep['cidades_ce']}")
    print()
    
    # 4. Aplicar correções
    print("🔧 APLICANDO CORREÇÕES...")
    
    # Backup
    backup_file = f'representantes_backup_ceara_completo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"💾 Backup salvo: {backup_file}")
    
    # Aplicar correções
    for rep in representantes_problematicos:
        estado = rep['estado']
        nome_rep = rep['nome']
        cidades_ce = rep['cidades_ce']
        
        # Remover cidades do CE da lista de cidades atendidas
        cidades_atuais = dados[estado][nome_rep]['cidades_atendidas']
        cidades_novas = [cidade for cidade in cidades_atuais if cidade not in cidades_ce]
        
        dados[estado][nome_rep]['cidades_atendidas'] = cidades_novas
        cidades_removidas_total.extend(cidades_ce)
        
        print(f"  ✅ {nome_rep}: removidas {len(cidades_ce)} cidades do CE")
        for cidade in cidades_ce:
            print(f"    - {cidade}")
    
    # Salvar arquivo corrigido
    with open('representantes.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print("✅ Arquivo representantes.json atualizado")
    print()
    
    # 5. Relatório final
    print("📊 RELATÓRIO FINAL:")
    print(f"  • Representantes corrigidos: {len(representantes_problematicos)}")
    print(f"  • Total de cidades removidas: {len(cidades_removidas_total)}")
    print(f"  • Cidades únicas removidas: {len(set(cidades_removidas_total))}")
    print(f"  • Cidades removidas: {sorted(set(cidades_removidas_total))}")
    print()
    print("🎯 CORREÇÃO CONCLUÍDA: Apenas representantes com código 43.0 podem atender cidades do Ceará")
    print()
    print("=" * 70)

if __name__ == '__main__':
    try:
        corrigir_ceara_completo()
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()