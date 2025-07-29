#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se LUGUS atende todos os 62 municípios do Amazonas
"""

import json
from datetime import datetime

def obter_municipios_amazonas_completos():
    """
    Lista completa dos 62 municípios do Amazonas (conforme IBGE)
    """
    return {
        'ALVARAES', 'AMATURÁ', 'ANAMA', 'ANORI', 'APUI', 'ATALAIA DO NORTE',
        'AUTAZES', 'BARCELOS', 'BARREIRINHA', 'BENJAMIN CONSTANT', 'BERURI',
        'BOA VISTA DO RAMOS', 'BOCA DO ACRE', 'BORBA', 'CAAPIRANGA', 'CANUTAMA',
        'CARAUARI', 'CAREIRO', 'CAREIRO DA VÁRZEA', 'COARI', 'CODAJÁS',
        'EIRUNEPE', 'ENVIRA', 'FONTE BOA', 'GUAJARÁ', 'HUMAITÁ', 'IPIXUNA',
        'IRANDUBA', 'ITACOATIARA', 'ITAMARATI', 'ITAPIRANGA', 'JAPURÁ',
        'JURUÁ', 'JUTAI', 'LÁBREA', 'MANACAPURU', 'MANAQUIRI', 'MANAUS',
        'MANICORE', 'MARAA', 'MAUES', 'NHAMUNDÁ', 'NOVA OLINDA DO NORTE',
        'NOVO AIRAO', 'NOVO ARIPUANA', 'PARINTINS', 'PAUINI', 'PRESIDENTE FIGUEIREDO',
        'RIO PRETO DA EVA', 'SANTA ISABEL DO RIO NEGRO', 'SANTO ANTONIO DO ICÁ',
        'SAO GABRIEL DA CACHOEIRA', 'SAO PAULO DE OLIVENCA', 'SAO SEBASTIAO DO UATUMA',
        'SILVES', 'TABATINGA', 'TAPAUÁ', 'TEFE', 'TONANTINS', 'UARINI',
        'URUCARÁ', 'URUCURITUBA'
    }

def verificar_lugus_amazonas():
    """
    Verifica se LUGUS atende todos os municípios do Amazonas
    """
    
    print("=== VERIFICAÇÃO LUGUS - AMAZONAS ===")
    print(f"Verificando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Carregar dados dos representantes
    try:
        with open('representantes.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar representantes.json: {e}")
        return False
    
    # Verificar se AMAZONAS existe
    if 'AMAZONAS' not in dados:
        print("❌ Estado AMAZONAS não encontrado no arquivo")
        return False
    
    # Verificar se LUGUS existe no Amazonas
    amazonas = dados['AMAZONAS']
    lugus_encontrado = None
    
    for nome_rep, info_rep in amazonas.items():
        if 'LUGUS' in nome_rep.upper():
            lugus_encontrado = nome_rep
            break
    
    if not lugus_encontrado:
        print("❌ LUGUS REPRESENTACAO LTDA não encontrado no Amazonas")
        return False
    
    print(f"✅ Representante encontrado: {lugus_encontrado}")
    
    # Obter cidades atendidas pelo LUGUS
    cidades_lugus = set(amazonas[lugus_encontrado].get('cidades_atendidas', []))
    print(f"📊 Cidades atendidas pelo LUGUS: {len(cidades_lugus)}")
    
    # Obter lista completa de municípios do Amazonas
    municipios_amazonas = obter_municipios_amazonas_completos()
    print(f"📋 Total de municípios do Amazonas: {len(municipios_amazonas)}")
    
    # Verificar cidades faltando
    cidades_faltando = municipios_amazonas - cidades_lugus
    cidades_extras = cidades_lugus - municipios_amazonas
    
    print("\n🔍 ANÁLISE DETALHADA:")
    
    if cidades_faltando:
        print(f"❌ CIDADES FALTANDO ({len(cidades_faltando)}):")
        for cidade in sorted(cidades_faltando):
            print(f"  - {cidade}")
    else:
        print("✅ Nenhuma cidade faltando")
    
    if cidades_extras:
        print(f"\n⚠️  CIDADES EXTRAS ({len(cidades_extras)}):")
        for cidade in sorted(cidades_extras):
            print(f"  - {cidade}")
    else:
        print("\n✅ Nenhuma cidade extra")
    
    # Verificar código do representante
    codigo = amazonas[lugus_encontrado].get('dados_contato', {}).get('codigo_representante', '')
    print(f"\n📋 Código do representante: {codigo}")
    
    if codigo != '53.02':
        print(f"⚠️  Código incorreto! Esperado: 53.02, Atual: {codigo}")
    else:
        print("✅ Código correto")
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL:")
    print(f"  • Cidades atendidas: {len(cidades_lugus)}")
    print(f"  • Cidades esperadas: {len(municipios_amazonas)}")
    print(f"  • Cidades faltando: {len(cidades_faltando)}")
    print(f"  • Cidades extras: {len(cidades_extras)}")
    
    sucesso = len(cidades_faltando) == 0 and codigo == '53.02'
    
    if sucesso:
        print("\n✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🎯 LUGUS atende todos os municípios do Amazonas corretamente")
    else:
        print("\n⚠️  VERIFICAÇÃO DETECTOU PROBLEMAS!")
        if cidades_faltando:
            print("🔧 Necessário adicionar as cidades faltando")
        if codigo != '53.02':
            print("🔧 Necessário corrigir o código do representante")
    
    print("\n" + "=" * 60)
    return sucesso

if __name__ == '__main__':
    try:
        verificar_lugus_amazonas()
    except Exception as e:
        print(f"❌ Erro durante a verificação: {e}")
        import traceback
        traceback.print_exc()