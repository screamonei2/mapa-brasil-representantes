#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script genérico para correção de estados com único representante
Garante que cada representante atenda TODAS as cidades do seu estado
"""

import json
import os
from datetime import datetime

def obter_mapeamento_representantes():
    """
    Retorna o mapeamento de estados para seus respectivos representantes únicos
    """
    return {
        'SERGIPE': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'RORAIMA': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'RIO GRANDE DO NORTE': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'ALAGOAS': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'RONDONIA': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'MARANHAO': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'AMAPA': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'ACRE': {
            'codigo': '01',
            'nome': 'SCHIOPPA',
            'contato': 'Schioppa',
            'email': 'vendas@schioppa.com.br',
            'celular': '11-99154-6727'
        },
        'PERNAMBUCO': {
            'codigo': '17',
            'nome': 'A.GOUVEIA REPRESENTACOES  DE EQUIPS LTDA',
            'contato': 'Amaro',
            'email': 'agouveiarepresentacoes@gmail.com',
            'celular': '81-3466-8096 / 81-3482-2432 / 81-99948-9294'
        },
        'PARAIBA': {
            'codigo': '19',
            'nome': 'ALR CONSULTORIA EMPRESARIAL INDUSTRIAL A',
            'contato': 'Leonardo',
            'email': 'ara.leonardo@terra.com.br',
            'celular': '83-99197-8448 / 11-98459-9879'
        },
        'GOIAS': {
            'codigo': '32',
            'nome': 'CENTRAL REPRESENTAÇÕES LTDA',
            'contato': 'Washington',
            'email': 'centralrep@hotmail.com.br',
            'celular': '62-32330021 / 62-98124-7000 / 62-98520-0021 / 62-98142-9116'
        },
        'MATO GROSSO': {
            'codigo': '33',
            'nome': 'PELINSSON REPRESENTAÇÕES LTDA',
            'contato': 'Adair',
            'email': 'adairpelinsson@gmail.com',
            'celular': '66-99984-1208'
        },
        'MATO GROSSO DO SUL': {
            'codigo': '34',
            'nome': 'SA & PESSOA REPRESENTACAO COMERCIAL LTDA',
            'contato': 'Linaldo/Waldir',
            'email': 'saepessoa@gmail.com',
            'celular': '67-3351-5374 / 67-99236-6225 / 67-98415-2730 / 67-99198-4096'
        },
        'CEARA': {
            'codigo': '43.0',
            'nome': 'ROD LON REPRESENTAÇÕES LTDA',
            'contato': 'Odilon',
            'email': 'pedidoreol@yahoo.com.br',
            'celular': '85-99174-9392 / 85-98833-3396 / 85-3221-6816'
        },
        'ESPIRITO SANTO': {
            'codigo': '44',
            'nome': 'BEMAC REPRESENTAÇÕES LTDA',
            'contato': 'Bernardo',
            'email': 'representa.es@gmail.com',
            'celular': '27-99775-0925'
        },
        'DISTRITO FEDERAL': {
            'codigo': '50.01',
            'nome': 'RUMO CERTO REPRESENTACOES LTDA',
            'contato': 'Mirabeau',
            'email': 'mmbastosdf@gmail.com',
            'celular': '61-99364-1111'
        },
        'BAHIA': {
            'codigo': '51',
            'nome': 'A3 CONSULTORIA, REPRES E SERVIÇOS EIRELI',
            'contato': 'Jose Lima',
            'email': 'aconsultoria3@gmail.com',
            'celular': '71-99976-5435 / 71-99239-1242'
        },
        'AMAZONAS': {
            'codigo': '53.02',
            'nome': 'LUGUS REPRESENTACAO LTDA',
            'contato': 'Andre/Pedro',
            'email': 'lugusrep.andre@gmail.com',
            'celular': '92-98127-0831'
        },
        'PIAUI': {
            'codigo': '54.01',
            'nome': 'FERNANDO MURILO REPRESENTAÇÕES LTDA - ME',
            'contato': 'Fernando',
            'email': 'fernandomurilorep@gmail.com',
            'celular': '86-98134-9665'
        },
        'PARA': {
            'codigo': '82.0',
            'nome': 'JUMPER COM. SERVIÇOS E REPRES.LTDA-EPP',
            'contato': 'Edson Pereira',
            'email': 'jumperscltda@gmail.com',
            'celular': '91-98098-9898/91-98427-9972'
        }
    }

def extrair_cidades_por_estado():
    """
    Extrai todas as cidades organizadas por estado usando múltiplas estratégias
    """
    cidades_por_estado = {}
    
    # Estratégia 1: Tentar carregar municipios.json com diferentes codificações
    for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
        try:
            with open('old/municipios.json', 'r', encoding=encoding) as f:
                municipios = json.load(f)
            
            for municipio in municipios['features']:
                uf = municipio['properties']['UF']
                nome_cidade = municipio['properties']['NOME'].upper()
                
                # Normalizar nomes (remover acentos comuns)
                nome_cidade = nome_cidade.replace('Ã', 'A').replace('Õ', 'O').replace('Ç', 'C')
                nome_cidade = nome_cidade.replace('É', 'E').replace('Í', 'I').replace('Ó', 'O')
                nome_cidade = nome_cidade.replace('Ú', 'U').replace('Â', 'A').replace('Ê', 'E')
                nome_cidade = nome_cidade.replace('Ô', 'O').replace('À', 'A')
                
                # Mapear UF para nome completo do estado
                mapa_estados = {
                    'SE': 'SERGIPE', 'RR': 'RORAIMA', 'RN': 'RIO GRANDE DO NORTE',
                    'AL': 'ALAGOAS', 'RO': 'RONDONIA', 'MA': 'MARANHAO',
                    'AP': 'AMAPA', 'AC': 'ACRE', 'PE': 'PERNAMBUCO',
                    'PB': 'PARAIBA', 'GO': 'GOIAS', 'MT': 'MATO GROSSO',
                    'MS': 'MATO GROSSO DO SUL', 'CE': 'CEARA', 'ES': 'ESPIRITO SANTO',
                    'DF': 'DISTRITO FEDERAL', 'BA': 'BAHIA', 'AM': 'AMAZONAS',
                    'PI': 'PIAUI', 'PA': 'PARA'
                }
                
                estado_nome = mapa_estados.get(uf)
                if estado_nome:
                    if estado_nome not in cidades_por_estado:
                        cidades_por_estado[estado_nome] = set()
                    cidades_por_estado[estado_nome].add(nome_cidade)
            
            print(f"✅ Arquivo carregado com codificação {encoding}")
            print(f"✅ Encontrados {len(cidades_por_estado)} estados")
            return cidades_por_estado
            
        except Exception as e:
            print(f"⚠️  Tentativa com {encoding} falhou: {str(e)[:100]}...")
            continue
    
    print("❌ Não foi possível carregar o arquivo de municípios")
    return {}

def corrigir_estados_unico_representante():
    """
    Correção completa: garante que cada estado tenha apenas seu representante único
    atendendo TODAS as cidades do estado
    """
    
    print("=== CORREÇÃO ESTADOS COM ÚNICO REPRESENTANTE ===")
    print(f"Processando em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Obter mapeamento de representantes
    mapeamento_representantes = obter_mapeamento_representantes()
    print(f"📋 Estados com representante único: {len(mapeamento_representantes)}")
    
    # 2. Extrair cidades por estado
    print("🔍 EXTRAINDO CIDADES POR ESTADO...")
    cidades_por_estado = extrair_cidades_por_estado()
    
    if not cidades_por_estado:
        print("❌ Não foi possível extrair cidades por estado")
        return
    
    # 3. Carregar dados dos representantes
    try:
        with open('representantes.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar representantes.json: {e}")
        return
    
    # 4. Backup
    backup_file = f'representantes_backup_estados_unicos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"💾 Backup salvo: {backup_file}")
    
    # 5. Processar cada estado
    print("🔧 PROCESSANDO ESTADOS...")
    estados_processados = 0
    
    for estado_nome, rep_info in mapeamento_representantes.items():
        print(f"\n📍 Processando {estado_nome}...")
        
        # Verificar se o estado existe no arquivo
        if estado_nome not in dados:
            print(f"  ⚠️  Estado {estado_nome} não encontrado no arquivo")
            dados[estado_nome] = {}
        
        # Obter cidades do estado
        cidades_estado = cidades_por_estado.get(estado_nome, set())
        if not cidades_estado:
            print(f"  ⚠️  Nenhuma cidade encontrada para {estado_nome}")
            continue
        
        print(f"  📊 Cidades encontradas: {len(cidades_estado)}")
        
        # Limpar representantes existentes no estado
        dados[estado_nome].clear()
        
        # Adicionar o representante único com todas as cidades
        dados[estado_nome][rep_info['nome']] = {
            'dados_contato': {
                'codigo_representante': rep_info['codigo'],
                'email': rep_info['email'],
                'cell': rep_info['celular'],
                'contato': rep_info['contato']
            },
            'cidades_atendidas': sorted(list(cidades_estado))
        }
        
        print(f"  ✅ {rep_info['nome']} configurado para atender {len(cidades_estado)} cidades")
        estados_processados += 1
    
    # 6. Salvar arquivo corrigido
    with open('representantes.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Arquivo representantes.json atualizado")
    
    # 7. Relatório final
    print("\n📊 RELATÓRIO FINAL:")
    print(f"  • Estados processados: {estados_processados}")
    print(f"  • Estados configurados: {len(mapeamento_representantes)}")
    
    # Mostrar resumo por estado
    print("\n📋 RESUMO POR ESTADO:")
    for estado_nome, rep_info in mapeamento_representantes.items():
        cidades_count = len(cidades_por_estado.get(estado_nome, set()))
        print(f"  • {estado_nome}: {rep_info['nome']} (código {rep_info['codigo']}) - {cidades_count} cidades")
    
    print("\n🎯 CORREÇÃO CONCLUÍDA: Cada estado tem seu representante único atendendo todas as cidades")
    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        corrigir_estados_unico_representante()
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()