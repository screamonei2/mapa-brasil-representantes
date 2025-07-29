#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificação para estados com representante único
Verifica se cada estado tem apenas seu representante designado
"""

import json
from datetime import datetime

def obter_estados_esperados():
    """
    Retorna os estados que devem ter representante único
    """
    return {
        'SERGIPE': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'RORAIMA': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'RIO GRANDE DO NORTE': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'ALAGOAS': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'RONDONIA': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'MARANHAO': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'AMAPA': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'ACRE': {'codigo': '01', 'nome': 'SCHIOPPA'},
        'PERNAMBUCO': {'codigo': '17', 'nome': 'A.GOUVEIA REPRESENTACOES  DE EQUIPS LTDA'},
        'PARAIBA': {'codigo': '19', 'nome': 'ALR CONSULTORIA EMPRESARIAL INDUSTRIAL A'},
        'GOIAS': {'codigo': '32', 'nome': 'CENTRAL REPRESENTAÇÕES LTDA'},
        'MATO GROSSO': {'codigo': '33', 'nome': 'PELINSSON REPRESENTAÇÕES LTDA'},
        'MATO GROSSO DO SUL': {'codigo': '34', 'nome': 'SA & PESSOA REPRESENTACAO COMERCIAL LTDA'},
        'CEARA': {'codigo': '43.0', 'nome': 'ROD LON REPRESENTAÇÕES LTDA'},
        'ESPIRITO SANTO': {'codigo': '44', 'nome': 'BEMAC REPRESENTAÇÕES LTDA'},
        'DISTRITO FEDERAL': {'codigo': '50.01', 'nome': 'RUMO CERTO REPRESENTACOES LTDA'},
        'BAHIA': {'codigo': '51', 'nome': 'A3 CONSULTORIA, REPRES E SERVIÇOS EIRELI'},
        'AMAZONAS': {'codigo': '53.02', 'nome': 'LUGUS REPRESENTACAO LTDA'},
        'PIAUI': {'codigo': '54.01', 'nome': 'FERNANDO MURILO REPRESENTAÇÕES LTDA - ME'},
        'PARA': {'codigo': '82.0', 'nome': 'JUMPER COM. SERVIÇOS E REPRES.LTDA-EPP'}
    }

def verificar_estados_unicos():
    """
    Verifica se todos os estados com representante único estão configurados corretamente
    """
    
    print("=== VERIFICAÇÃO ESTADOS COM REPRESENTANTE ÚNICO ===")
    print(f"Verificando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Carregar dados dos representantes
    try:
        with open('representantes.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar representantes.json: {e}")
        return False
    
    estados_esperados = obter_estados_esperados()
    
    print("🔍 VERIFICANDO CONFIGURAÇÃO...")
    estados_corretos = 0
    estados_incorretos = 0
    problemas = []
    
    for estado_nome, info_esperada in estados_esperados.items():
        print(f"\n📍 Verificando {estado_nome}...")
        
        # Verificar se o estado existe
        if estado_nome not in dados:
            problema = f"Estado {estado_nome} não encontrado"
            problemas.append(problema)
            print(f"  ❌ {problema}")
            estados_incorretos += 1
            continue
        
        representantes_estado = dados[estado_nome]
        
        # Verificar se tem exatamente 1 representante
        if len(representantes_estado) != 1:
            problema = f"{estado_nome}: tem {len(representantes_estado)} representantes (esperado: 1)"
            problemas.append(problema)
            print(f"  ❌ {problema}")
            estados_incorretos += 1
            continue
        
        # Verificar se é o representante correto
        nome_rep = list(representantes_estado.keys())[0]
        if nome_rep != info_esperada['nome']:
            problema = f"{estado_nome}: representante '{nome_rep}' (esperado: '{info_esperada['nome']}')"
            problemas.append(problema)
            print(f"  ❌ {problema}")
            estados_incorretos += 1
            continue
        
        # Verificar código do representante
        codigo_atual = representantes_estado[nome_rep]['dados_contato']['codigo_representante']
        if codigo_atual != info_esperada['codigo']:
            problema = f"{estado_nome}: código '{codigo_atual}' (esperado: '{info_esperada['codigo']}')"
            problemas.append(problema)
            print(f"  ❌ {problema}")
            estados_incorretos += 1
            continue
        
        # Verificar se tem cidades atendidas
        cidades_atendidas = representantes_estado[nome_rep].get('cidades_atendidas', [])
        if not cidades_atendidas:
            problema = f"{estado_nome}: nenhuma cidade atendida"
            problemas.append(problema)
            print(f"  ⚠️  {problema}")
        
        print(f"  ✅ {nome_rep} (código {codigo_atual}) - {len(cidades_atendidas)} cidades")
        estados_corretos += 1
    
    # Verificar se há representantes incorretos em outros estados
    print("\n🔍 VERIFICANDO REPRESENTANTES INCORRETOS...")
    representantes_incorretos = []
    
    # Criar mapa de quais representantes devem estar em quais estados
    representantes_permitidos = {}
    for estado, info in estados_esperados.items():
        codigo = info['codigo']
        nome = info['nome']
        if codigo not in representantes_permitidos:
            representantes_permitidos[codigo] = {'nome': nome, 'estados': []}
        representantes_permitidos[codigo]['estados'].append(estado)
    
    # Verificar se há representantes em estados onde não deveriam estar
    for estado_atual, representantes in dados.items():
        if estado_atual not in estados_esperados:
            continue  # Ignorar estados que não são de representante único
            
        for nome_rep, info_rep in representantes.items():
            codigo_rep = info_rep.get('dados_contato', {}).get('codigo_representante', '')
            
            # Verificar se este representante deveria estar neste estado
            info_esperada = estados_esperados[estado_atual]
            if nome_rep != info_esperada['nome'] or codigo_rep != info_esperada['codigo']:
                incorreto = f"Estado {estado_atual}: representante incorreto '{nome_rep}' (código {codigo_rep}), deveria ser '{info_esperada['nome']}' (código {info_esperada['codigo']})"
                representantes_incorretos.append(incorreto)
                print(f"  ❌ {incorreto}")
    
    # Relatório final
    print("\n📊 RESULTADO DA VERIFICAÇÃO:")
    print(f"  • Estados corretos: {estados_corretos}")
    print(f"  • Estados incorretos: {estados_incorretos}")
    print(f"  • Total de estados: {len(estados_esperados)}")
    print(f"  • Representantes incorretos: {len(representantes_incorretos)}")
    
    if problemas:
        print("\n❌ PROBLEMAS ENCONTRADOS:")
        for i, problema in enumerate(problemas, 1):
            print(f"  {i}. {problema}")
    
    if representantes_incorretos:
        print("\n⚠️  REPRESENTANTES INCORRETOS:")
        for i, incorreto in enumerate(representantes_incorretos, 1):
            print(f"  {i}. {incorreto}")
    
    sucesso = estados_incorretos == 0 and len(representantes_incorretos) == 0
    
    if sucesso:
        print("\n✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🎯 Todos os estados estão configurados corretamente")
    else:
        print("\n⚠️  VERIFICAÇÃO DETECTOU PROBLEMAS!")
        print("🔧 Execute novamente o script de correção se necessário")
    
    print("\n" + "=" * 60)
    return sucesso

if __name__ == '__main__':
    try:
        verificar_estados_unicos()
    except Exception as e:
        print(f"❌ Erro durante a verificação: {e}")
        import traceback
        traceback.print_exc()