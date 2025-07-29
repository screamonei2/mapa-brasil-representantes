#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificação final - Ceará
Verifica se apenas representantes com código 43.0 atendem cidades do Ceará
"""

import json
from datetime import datetime

def verificar_ceara_final():
    """
    Verificação final: confirma que apenas código 43.0 atende cidades do CE
    """
    
    print("=== VERIFICAÇÃO FINAL - CEARÁ ===")
    print(f"Verificando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Lista de cidades do Ceará
    cidades_ceara = {
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
    
    # Carregar dados dos representantes
    try:
        with open('representantes.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar representantes.json: {e}")
        return
    
    print("🔍 VERIFICANDO REPRESENTANTES...")
    representantes_corretos = []
    representantes_incorretos = []
    
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
            
            # Classificar representante
            if cidades_ce_atendidas:
                if codigo == '43.0':
                    representantes_corretos.append({
                        'estado': estado,
                        'nome': nome_rep,
                        'codigo': codigo,
                        'cidades_ce': cidades_ce_atendidas
                    })
                else:
                    representantes_incorretos.append({
                        'estado': estado,
                        'nome': nome_rep,
                        'codigo': codigo,
                        'cidades_ce': cidades_ce_atendidas
                    })
    
    # Relatório
    print("📊 RESULTADO DA VERIFICAÇÃO:")
    print()
    
    if representantes_corretos:
        print(f"✅ REPRESENTANTES CORRETOS (código 43.0): {len(representantes_corretos)}")
        for rep in representantes_corretos:
            print(f"  • {rep['nome']} (Estado: {rep['estado']})")
            print(f"    Cidades do CE: {len(rep['cidades_ce'])} cidades")
            # Mostrar algumas cidades como exemplo
            cidades_exemplo = rep['cidades_ce'][:5]
            if len(rep['cidades_ce']) > 5:
                cidades_exemplo.append('...')
            print(f"    Exemplos: {cidades_exemplo}")
        print()
    
    if representantes_incorretos:
        print(f"❌ REPRESENTANTES INCORRETOS (sem código 43.0): {len(representantes_incorretos)}")
        for rep in representantes_incorretos:
            print(f"  • {rep['nome']} (Estado: {rep['estado']}, Código: {rep['codigo']})")
            print(f"    Cidades do CE: {rep['cidades_ce']}")
        print()
        print("⚠️  ATENÇÃO: Ainda existem representantes incorretos!")
    else:
        print("✅ NENHUM REPRESENTANTE INCORRETO ENCONTRADO!")
        print("🎯 Todos os representantes que atendem cidades do Ceará têm código 43.0")
    
    print()
    print("=" * 50)
    
    return len(representantes_incorretos) == 0

if __name__ == '__main__':
    try:
        sucesso = verificar_ceara_final()
        if sucesso:
            print("🎉 VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        else:
            print("⚠️  VERIFICAÇÃO DETECTOU PROBLEMAS!")
    except Exception as e:
        print(f"❌ Erro durante a verificação: {e}")
        import traceback
        traceback.print_exc()