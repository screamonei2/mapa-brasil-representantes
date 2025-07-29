#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir dados do Ceará - manter apenas representantes com código 43.0
Remove todos os representantes do Ceará que não tenham código 43.0
"""

import json
import os
from datetime import datetime

def corrigir_ceara_43_0():
    """
    Remove todos os representantes do Ceará que não tenham código 43.0
    """
    
    # Carregar dados
    with open('representantes.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print("=== CORREÇÃO CEARÁ - MANTER APENAS CÓDIGO 43.0 ===")
    print(f"Processando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar se existe a seção CEARA
    if 'CEARA' not in dados:
        print("❌ Seção CEARA não encontrada nos dados")
        return
    
    ceara_original = dados['CEARA'].copy()
    representantes_removidos = []
    representantes_mantidos = []
    
    print("📋 REPRESENTANTES ENCONTRADOS NO CEARÁ:")
    for nome_rep, info_rep in ceara_original.items():
        codigo = info_rep.get('dados_contato', {}).get('codigo_representante', 'N/A')
        print(f"  • {nome_rep} - Código: {codigo}")
        
        if codigo == '43.0':
            representantes_mantidos.append((nome_rep, codigo))
            print(f"    ✅ MANTIDO (código 43.0)")
        else:
            representantes_removidos.append((nome_rep, codigo))
            print(f"    ❌ SERÁ REMOVIDO (código {codigo})")
    
    print()
    
    # Aplicar correções
    if representantes_removidos:
        print("🔧 APLICANDO CORREÇÕES...")
        
        # Criar nova estrutura do Ceará apenas com representantes 43.0
        nova_ceara = {}
        for nome_rep, info_rep in ceara_original.items():
            codigo = info_rep.get('dados_contato', {}).get('codigo_representante', 'N/A')
            if codigo == '43.0':
                nova_ceara[nome_rep] = info_rep
        
        # Atualizar dados
        dados['CEARA'] = nova_ceara
        
        # Salvar backup
        backup_file = f'representantes_backup_ceara_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump({'CEARA_ORIGINAL': ceara_original}, f, ensure_ascii=False, indent=2)
        print(f"💾 Backup salvo: {backup_file}")
        
        # Salvar arquivo corrigido
        with open('representantes.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        print("✅ Arquivo representantes.json atualizado")
        print()
        
        # Relatório final
        print("📊 RELATÓRIO FINAL:")
        print(f"  • Representantes mantidos: {len(representantes_mantidos)}")
        for nome, codigo in representantes_mantidos:
            print(f"    - {nome} (código {codigo})")
        
        print(f"  • Representantes removidos: {len(representantes_removidos)}")
        for nome, codigo in representantes_removidos:
            print(f"    - {nome} (código {codigo})")
        
        print()
        print("🎯 CORREÇÃO CONCLUÍDA: Apenas representantes com código 43.0 permanecem no Ceará")
        
    else:
        print("✅ Nenhuma correção necessária - apenas representantes com código 43.0 encontrados")
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    try:
        corrigir_ceara_43_0()
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()