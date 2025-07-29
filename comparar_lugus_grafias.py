#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparar grafias das cidades do LUGUS entre arquivo atual e antigo
"""

import json
from datetime import datetime

def normalizar_cidade(nome):
    """
    Normaliza o nome da cidade removendo acentos e convertendo para maiúsculas
    """
    nome = nome.upper()
    # Remover acentos comuns
    nome = nome.replace('Ã', 'A').replace('Õ', 'O').replace('Ç', 'C')
    nome = nome.replace('É', 'E').replace('Í', 'I').replace('Ó', 'O')
    nome = nome.replace('Ú', 'U').replace('Â', 'A').replace('Ê', 'E')
    nome = nome.replace('Ô', 'O').replace('À', 'A').replace('Ü', 'U')
    nome = nome.replace('Ñ', 'N')
    return nome

def comparar_lugus_grafias():
    """
    Compara as grafias das cidades do LUGUS entre arquivo atual e antigo
    """
    
    print("=== COMPARAÇÃO GRAFIAS LUGUS - AMAZONAS ===")
    print(f"Comparando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Carregar arquivo atual
    try:
        with open('representantes.json', 'r', encoding='utf-8') as f:
            dados_atual = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar representantes.json atual: {e}")
        return
    
    # Carregar arquivo antigo
    try:
        with open('old/representantes.json', 'r', encoding='utf-8') as f:
            dados_antigo = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar representantes.json antigo: {e}")
        return
    
    # Obter cidades do LUGUS no arquivo atual
    cidades_atual = set()
    if 'AMAZONAS' in dados_atual:
        for nome_rep, info_rep in dados_atual['AMAZONAS'].items():
            if 'LUGUS' in nome_rep.upper():
                cidades_atual = set(info_rep.get('cidades_atendidas', []))
                break
    
    print(f"📊 Cidades no arquivo atual: {len(cidades_atual)}")
    
    # Obter cidades do LUGUS no arquivo antigo (formato diferente)
    cidades_antigo = set()
    if isinstance(dados_antigo, dict):
        # Procurar por mapeamentos cidade -> representante
        for chave, valor in dados_antigo.items():
            if isinstance(valor, str) and 'LUGUS' in valor.upper():
                cidade_normalizada = normalizar_cidade(chave)
                cidades_antigo.add(cidade_normalizada)
            elif isinstance(valor, dict):
                # Verificar se é estrutura aninhada
                for sub_chave, sub_valor in valor.items():
                    if isinstance(sub_valor, str) and 'LUGUS' in sub_valor.upper():
                        cidade_normalizada = normalizar_cidade(sub_chave)
                        cidades_antigo.add(cidade_normalizada)
    
    print(f"📋 Cidades no arquivo antigo: {len(cidades_antigo)}")
    
    # Normalizar cidades do arquivo atual para comparação
    cidades_atual_norm = {normalizar_cidade(cidade) for cidade in cidades_atual}
    
    # Comparar
    cidades_faltando_atual = cidades_antigo - cidades_atual_norm
    cidades_extras_atual = cidades_atual_norm - cidades_antigo
    
    print("\n🔍 ANÁLISE COMPARATIVA:")
    
    if cidades_faltando_atual:
        print(f"\n❌ CIDADES NO ANTIGO MAS NÃO NO ATUAL ({len(cidades_faltando_atual)}):")
        for cidade in sorted(cidades_faltando_atual):
            print(f"  - {cidade}")
            
            # Procurar grafias similares no atual
            for cidade_atual in cidades_atual:
                if normalizar_cidade(cidade_atual) == cidade:
                    print(f"    → Encontrada grafia similar: '{cidade_atual}'")
                    break
    else:
        print("\n✅ Todas as cidades do arquivo antigo estão no atual")
    
    if cidades_extras_atual:
        print(f"\n⚠️  CIDADES NO ATUAL MAS NÃO NO ANTIGO ({len(cidades_extras_atual)}):")
        for cidade in sorted(cidades_extras_atual):
            print(f"  - {cidade}")
    else:
        print("\n✅ Nenhuma cidade extra no arquivo atual")
    
    # Verificar grafias específicas problemáticas
    print("\n🔍 VERIFICAÇÃO DE GRAFIAS ESPECÍFICAS:")
    
    grafias_problematicas = [
        ('SÃO GABRIEL DA CACHOEIRA', 'SAO GABRIEL DA CACHOEIRA'),
        ('SÃO PAULO DE OLIVENÇA', 'SAO PAULO DE OLIVENCA'),
        ('SÃO SEBASTIÃO DO UATUMÃ', 'SAO SEBASTIAO DO UATUMA'),
        ('SANTO ANTÔNIO DO IÇÁ', 'SANTO ANTONIO DO ICÁ'),
        ('TEFÉ', 'TEFE'),
        ('TAPAUÁ', 'TAPAUA'),
        ('JUTAÍ', 'JUTAI'),
        ('LÁBREA', 'LABREA'),
        ('MARAÃ', 'MARAA'),
        ('MAUÉS', 'MAUES'),
        ('EIRUNEPÉ', 'EIRUNEPE')
    ]
    
    for grafia_com_acento, grafia_sem_acento in grafias_problematicas:
        tem_com_acento = any(grafia_com_acento.upper() in cidade.upper() for cidade in cidades_atual)
        tem_sem_acento = any(grafia_sem_acento.upper() in cidade.upper() for cidade in cidades_atual)
        
        if tem_com_acento:
            print(f"  ✅ {grafia_com_acento} (com acentos)")
        elif tem_sem_acento:
            print(f"  ⚠️  {grafia_sem_acento} (sem acentos)")
        else:
            print(f"  ❌ {grafia_com_acento} / {grafia_sem_acento} (não encontrada)")
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL:")
    print(f"  • Cidades no atual: {len(cidades_atual)}")
    print(f"  • Cidades no antigo: {len(cidades_antigo)}")
    print(f"  • Faltando no atual: {len(cidades_faltando_atual)}")
    print(f"  • Extras no atual: {len(cidades_extras_atual)}")
    
    if len(cidades_faltando_atual) == 0 and len(cidades_extras_atual) == 0:
        print("\n✅ COMPARAÇÃO CONCLUÍDA: Arquivos estão consistentes")
    else:
        print("\n⚠️  COMPARAÇÃO DETECTOU DIFERENÇAS")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        comparar_lugus_grafias()
    except Exception as e:
        print(f"❌ Erro durante a comparação: {e}")
        import traceback
        traceback.print_exc()