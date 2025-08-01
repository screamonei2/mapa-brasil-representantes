#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir duplicações de representantes em São Paulo

PROBLEMA IDENTIFICADO:
- 11 representantes duplicados (32 total vs 21 esperado)
- Códigos ligeiramente diferentes (ex: 30 vs 30.0)
- Mesmo nome, chaves diferentes

SOLUÇÃO:
- Consolidar duplicatas mantendo a versão mais completa
- Manter código mais específico (ex: 30.0 > 30)
- Mesclar cidades se necessário

Autor: Assistente AI
Data: $(date +%Y-%m-%d)
"""

import json
import shutil
from datetime import datetime
from collections import defaultdict

def fazer_backup(arquivo):
    """
    Faz backup do arquivo original
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{arquivo.replace('.json', '')}_backup_correcao_duplicatas_{timestamp}.json"
    shutil.copy2(arquivo, backup_name)
    print(f"✅ Backup criado: {backup_name}")
    return backup_name

def normalizar_codigo(codigo):
    """
    Normaliza código para comparação (remove .0 se não for necessário)
    """
    if isinstance(codigo, str):
        codigo = codigo.strip()
        # Se termina com .0 e não é um código decimal real, remove
        if codigo.endswith('.0') and not codigo.replace('.0', '').isdigit():
            return codigo[:-2]
        return codigo
    return str(codigo)

def escolher_melhor_versao(duplicatas):
    """
    Escolhe a melhor versão entre duplicatas baseado em critérios
    """
    if len(duplicatas) == 1:
        return duplicatas[0]
    
    # Critérios de prioridade:
    # 1. Código mais específico (ex: 30.0 > 30)
    # 2. Mais cidades
    # 3. Chave mais limpa
    
    # Ordenar por especificidade do código
    duplicatas_ordenadas = sorted(duplicatas, key=lambda x: (
        # Priorizar códigos com .0 (mais específicos)
        not x['codigo'].endswith('.0') if isinstance(x['codigo'], str) else True,
        # Depois por número de cidades (mais é melhor)
        -x['cidades'],
        # Por fim, chave mais limpa
        len(x['key'])
    ))
    
    return duplicatas_ordenadas[0]

def mesclar_cidades(representantes):
    """
    Mescla cidades de representantes duplicados
    """
    todas_cidades = set()
    for rep in representantes:
        if 'SP' in rep.get('estados', {}):
            todas_cidades.update(rep['estados']['SP']['cidades'])
    return sorted(list(todas_cidades))

def corrigir_duplicatas_sp():
    """
    Função principal para corrigir duplicatas em SP
    """
    arquivo_sistema = 'old/representantes_por_estado.json'
    
    print("🔧 CORREÇÃO DE DUPLICAÇÕES EM SÃO PAULO")
    print("=" * 60)
    print()
    
    # 1. Fazer backup
    backup_file = fazer_backup(arquivo_sistema)
    
    # 2. Carregar dados
    print("📂 Carregando dados...")
    with open(arquivo_sistema, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 3. Identificar representantes de SP
    representantes_sp = []
    for key, rep in data['representantes'].items():
        if 'SP' in rep.get('estados', {}):
            representantes_sp.append({
                'key': key,
                'rep': rep,
                'codigo': rep.get('codigo', ''),
                'nome': rep.get('nome', ''),
                'cidades': len(rep['estados']['SP']['cidades'])
            })
    
    print(f"📊 Total de representantes SP encontrados: {len(representantes_sp)}")
    
    # 4. Agrupar por nome normalizado
    grupos_por_nome = defaultdict(list)
    for rep_info in representantes_sp:
        nome_normalizado = rep_info['nome'].strip().upper()
        grupos_por_nome[nome_normalizado].append(rep_info)
    
    # 5. Identificar duplicatas
    duplicatas_encontradas = []
    representantes_para_manter = []
    representantes_para_remover = []
    
    print()
    print("🔍 ANÁLISE DE DUPLICAÇÕES:")
    print("-" * 40)
    
    for nome, grupo in grupos_por_nome.items():
        if len(grupo) > 1:
            print(f"❌ DUPLICATA: {nome} ({len(grupo)} versões)")
            for i, rep in enumerate(grupo, 1):
                print(f"   {i}. Código: {rep['codigo']} | Cidades: {rep['cidades']} | Chave: {rep['key']}")
            
            # Escolher melhor versão
            melhor_versao = escolher_melhor_versao(grupo)
            representantes_para_manter.append(melhor_versao)
            
            # Marcar outros para remoção
            for rep in grupo:
                if rep['key'] != melhor_versao['key']:
                    representantes_para_remover.append(rep['key'])
            
            duplicatas_encontradas.append({
                'nome': nome,
                'grupo': grupo,
                'melhor': melhor_versao
            })
            
            print(f"   ✅ MANTENDO: {melhor_versao['codigo']} ({melhor_versao['cidades']} cidades)")
            print()
        else:
            # Representante único, manter
            representantes_para_manter.append(grupo[0])
    
    print(f"📊 RESUMO:")
    print(f"   Duplicatas encontradas: {len(duplicatas_encontradas)}")
    print(f"   Representantes para manter: {len(representantes_para_manter)}")
    print(f"   Representantes para remover: {len(representantes_para_remover)}")
    print()
    
    # 6. Mesclar cidades de duplicatas se necessário
    print("🔄 MESCLANDO CIDADES DE DUPLICATAS...")
    
    for duplicata in duplicatas_encontradas:
        nome = duplicata['nome']
        grupo = duplicata['grupo']
        melhor = duplicata['melhor']
        
        # Verificar se há cidades diferentes entre as versões
        todas_cidades = set()
        for rep in grupo:
            if 'SP' in rep['rep'].get('estados', {}):
                todas_cidades.update(rep['rep']['estados']['SP']['cidades'])
        
        cidades_melhor = set(melhor['rep']['estados']['SP']['cidades'])
        
        if todas_cidades != cidades_melhor:
            print(f"   📥 Mesclando cidades para {nome}")
            print(f"      Antes: {len(cidades_melhor)} cidades")
            print(f"      Depois: {len(todas_cidades)} cidades")
            
            # Atualizar melhor versão com todas as cidades
            melhor['rep']['estados']['SP']['cidades'] = sorted(list(todas_cidades))
            melhor['rep']['estados']['SP']['total_cidades'] = len(todas_cidades)
            
            # Atualizar total geral se só atende SP
            if len(melhor['rep']['estados']) == 1:
                melhor['rep']['total_cidades'] = len(todas_cidades)
    
    # 7. Remover representantes duplicados
    print()
    print("🗑️  REMOVENDO DUPLICATAS...")
    
    for key in representantes_para_remover:
        if key in data['representantes']:
            nome_removido = data['representantes'][key]['nome']
            print(f"   ❌ Removendo: {nome_removido} (chave: {key})")
            del data['representantes'][key]
    
    # 8. Salvar arquivo corrigido
    print()
    print("💾 Salvando sistema corrigido...")
    with open(arquivo_sistema, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 9. Verificar resultado
    print("🔍 Verificando resultado...")
    
    representantes_finais = []
    for key, rep in data['representantes'].items():
        if 'SP' in rep.get('estados', {}):
            representantes_finais.append({
                'nome': rep['nome'],
                'codigo': rep['codigo'],
                'cidades': len(rep['estados']['SP']['cidades'])
            })
    
    # 10. Relatório final
    print("=" * 60)
    print("🎉 RELATÓRIO DE CORREÇÃO:")
    print(f"📊 Representantes antes: {len(representantes_sp)}")
    print(f"📊 Representantes depois: {len(representantes_finais)}")
    print(f"🗑️  Duplicatas removidas: {len(representantes_para_remover)}")
    print(f"💾 Backup: {backup_file}")
    print()
    
    print("📋 REPRESENTANTES FINAIS SP:")
    for i, rep in enumerate(sorted(representantes_finais, key=lambda x: x['codigo']), 1):
        print(f"{i:2d}. {rep['nome']} (código {rep['codigo']}) - {rep['cidades']} cidades")
    
    print()
    print("✅ CORREÇÃO CONCLUÍDA!")
    print("🎯 SP agora tem representantes únicos e organizados!")
    
    return True

if __name__ == "__main__":
    try:
        sucesso = corrigir_duplicatas_sp()
        if sucesso:
            print("✅ Correção de duplicatas concluída!")
        else:
            print("❌ Problemas na correção.")
    except Exception as e:
        print(f"❌ ERRO durante correção: {e}")
        print("Verifique os arquivos e tente novamente.") 