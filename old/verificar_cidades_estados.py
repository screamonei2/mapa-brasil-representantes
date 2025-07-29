#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e remover cidades que não pertencem aos estados
atendidos pelos representantes.

Exemplo: Se Schioppa está listando cidades no Ceará, mas não atende o estado CE,
essas cidades devem ser removidas.
"""

import json
import logging
from typing import Dict, Set, List, Tuple
from collections import defaultdict
import unicodedata
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('verificacao_cidades_estados.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def normalizar_nome(nome: str) -> str:
    """Normaliza nome removendo acentos, espaços extras e convertendo para maiúsculo."""
    if not nome:
        return ""
    
    # Remove acentos
    nome = unicodedata.normalize('NFD', nome)
    nome = ''.join(char for char in nome if unicodedata.category(char) != 'Mn')
    
    # Converte para maiúsculo e remove espaços extras
    nome = nome.upper().strip()
    
    # Remove caracteres especiais, mantendo apenas letras, números e espaços
    nome = re.sub(r'[^A-Z0-9\s]', '', nome)
    
    # Remove espaços múltiplos
    nome = re.sub(r'\s+', ' ', nome)
    
    return nome

def carregar_mapeamento_municipios_estados() -> Dict[str, str]:
    """Carrega o mapeamento de municípios para estados do arquivo geojs."""
    try:
        with open('geojs-100-mun-v2.json', 'r', encoding='utf-8') as f:
            geojs_data = json.load(f)
        
        municipio_para_estado = {}
        
        for feature in geojs_data.get('features', []):
            properties = feature.get('properties', {})
            nome_municipio = properties.get('name', '').strip()
            
            # Tentar extrair UF de diferentes campos
            uf = None
            if 'uf' in properties:
                uf = properties['uf']
            elif 'sigla_uf' in properties:
                uf = properties['sigla_uf']
            elif 'estado' in properties:
                uf = properties['estado']
            elif 'uf_municipio' in properties:
                # Formato: "UF - Município"
                uf_municipio = properties['uf_municipio']
                if ' - ' in uf_municipio:
                    uf = uf_municipio.split(' - ')[0].strip()
            
            if nome_municipio and uf:
                nome_normalizado = normalizar_nome(nome_municipio)
                municipio_para_estado[nome_normalizado] = uf.strip().upper()
        
        logger.info(f"Carregados {len(municipio_para_estado)} municípios do arquivo geojs")
        return municipio_para_estado
        
    except Exception as e:
        logger.error(f"Erro ao carregar geojs-100-mun-v2.json: {e}")
        return {}

def carregar_representantes() -> dict:
    """Carrega dados dos representantes."""
    try:
        with open('representantes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar representantes.json: {e}")
        return {}

def normalizar_estado(estado: str) -> str:
    """Normaliza código do estado removendo espaços extras."""
    return estado.strip().upper()

def verificar_cidades_representante(representante_data: dict, municipio_para_estado: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """Verifica quais cidades de um representante não pertencem aos estados atendidos.
    
    Returns:
        Tuple[List[str], List[str]]: (cidades_validas, cidades_invalidas)
    """
    estados_atendidos = set()
    for estado in representante_data.get('estados', []):
        estados_atendidos.add(normalizar_estado(estado))
    
    cidades = representante_data.get('cidades', [])
    cidades_validas = []
    cidades_invalidas = []
    
    for cidade in cidades:
        nome_normalizado = normalizar_nome(cidade)
        
        # Verificar se a cidade existe no mapeamento
        if nome_normalizado in municipio_para_estado:
            estado_da_cidade = municipio_para_estado[nome_normalizado]
            
            # Verificar se o estado da cidade está nos estados atendidos
            if estado_da_cidade in estados_atendidos:
                cidades_validas.append(cidade)
            else:
                cidades_invalidas.append(cidade)
                logger.warning(
                    f"Cidade '{cidade}' (estado: {estado_da_cidade}) não está nos estados atendidos: {estados_atendidos}"
                )
        else:
            # Cidade não encontrada no mapeamento - manter por enquanto
            cidades_validas.append(cidade)
            logger.info(f"Cidade '{cidade}' não encontrada no mapeamento geográfico - mantendo")
    
    return cidades_validas, cidades_invalidas

def gerar_relatorio_inconsistencias(dados_representantes: dict, municipio_para_estado: Dict[str, str]) -> dict:
    """Gera relatório detalhado das inconsistências encontradas."""
    relatorio = {
        'total_representantes': 0,
        'representantes_com_problemas': 0,
        'total_cidades_removidas': 0,
        'detalhes': []
    }
    
    representantes = dados_representantes.get('representantes', {})
    relatorio['total_representantes'] = len(representantes)
    
    for nome_representante, dados in representantes.items():
        cidades_validas, cidades_invalidas = verificar_cidades_representante(dados, municipio_para_estado)
        
        if cidades_invalidas:
            relatorio['representantes_com_problemas'] += 1
            relatorio['total_cidades_removidas'] += len(cidades_invalidas)
            
            # Agrupar cidades inválidas por estado
            cidades_por_estado = defaultdict(list)
            for cidade in cidades_invalidas:
                nome_normalizado = normalizar_nome(cidade)
                if nome_normalizado in municipio_para_estado:
                    estado = municipio_para_estado[nome_normalizado]
                    cidades_por_estado[estado].append(cidade)
                else:
                    cidades_por_estado['DESCONHECIDO'].append(cidade)
            
            relatorio['detalhes'].append({
                'representante': nome_representante,
                'codigo': dados.get('codigo', 'N/A'),
                'estados_atendidos': dados.get('estados', []),
                'total_cidades_original': len(dados.get('cidades', [])),
                'total_cidades_validas': len(cidades_validas),
                'total_cidades_removidas': len(cidades_invalidas),
                'cidades_removidas_por_estado': dict(cidades_por_estado)
            })
    
    return relatorio

def corrigir_representantes(dados_representantes: dict, municipio_para_estado: Dict[str, str], salvar_backup: bool = True) -> dict:
    """Corrige os dados dos representantes removendo cidades inconsistentes."""
    if salvar_backup:
        # Salvar backup
        with open('representantes_backup_antes_correcao.json', 'w', encoding='utf-8') as f:
            json.dump(dados_representantes, f, ensure_ascii=False, indent=2)
        logger.info("Backup salvo em representantes_backup_antes_correcao.json")
    
    dados_corrigidos = dados_representantes.copy()
    representantes = dados_corrigidos.get('representantes', {})
    
    total_cidades_removidas = 0
    
    for nome_representante, dados in representantes.items():
        cidades_validas, cidades_invalidas = verificar_cidades_representante(dados, municipio_para_estado)
        
        if cidades_invalidas:
            logger.info(f"Corrigindo {nome_representante}: removendo {len(cidades_invalidas)} cidades")
            
            # Atualizar dados do representante
            dados['cidades'] = cidades_validas
            dados['total_cidades'] = len(cidades_validas)
            
            # Adicionar observação sobre a correção
            observacao_correcao = f"Removidas {len(cidades_invalidas)} cidades que não pertencem aos estados atendidos"
            if 'observacoes' in dados:
                dados['observacoes'] += f" | {observacao_correcao}"
            else:
                dados['observacoes'] = observacao_correcao
            
            total_cidades_removidas += len(cidades_invalidas)
    
    # Atualizar metadados
    if 'metadados' not in dados_corrigidos:
        dados_corrigidos['metadados'] = {}
    
    dados_corrigidos['metadados']['data_correcao_estados'] = "2025-01-27"
    dados_corrigidos['metadados']['total_cidades_removidas'] = total_cidades_removidas
    dados_corrigidos['metadados']['observacoes_correcao_estados'] = "Removidas cidades que não pertencem aos estados atendidos pelos representantes"
    
    logger.info(f"Correção concluída: {total_cidades_removidas} cidades removidas no total")
    
    return dados_corrigidos

def main():
    """Função principal."""
    logger.info("Iniciando verificação de cidades vs estados atendidos")
    
    # Carregar dados
    logger.info("Carregando mapeamento de municípios para estados...")
    municipio_para_estado = carregar_mapeamento_municipios_estados()
    
    if not municipio_para_estado:
        logger.error("Não foi possível carregar o mapeamento de municípios. Abortando.")
        return
    
    logger.info("Carregando dados dos representantes...")
    dados_representantes = carregar_representantes()
    
    if not dados_representantes:
        logger.error("Não foi possível carregar os dados dos representantes. Abortando.")
        return
    
    # Gerar relatório de inconsistências
    logger.info("Gerando relatório de inconsistências...")
    relatorio = gerar_relatorio_inconsistencias(dados_representantes, municipio_para_estado)
    
    # Salvar relatório
    with open('relatorio_inconsistencias_estados.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Relatório salvo em relatorio_inconsistencias_estados.json")
    logger.info(f"Resumo: {relatorio['representantes_com_problemas']} representantes com problemas, {relatorio['total_cidades_removidas']} cidades a serem removidas")
    
    # Mostrar detalhes dos problemas encontrados
    if relatorio['detalhes']:
        print("\n" + "="*80)
        print("PROBLEMAS ENCONTRADOS:")
        print("="*80)
        
        for detalhe in relatorio['detalhes']:
            print(f"\n🏢 {detalhe['representante']} (Código: {detalhe['codigo']})")
            print(f"   Estados atendidos: {', '.join(detalhe['estados_atendidos'])}")
            print(f"   Cidades: {detalhe['total_cidades_original']} → {detalhe['total_cidades_validas']} (removidas: {detalhe['total_cidades_removidas']})")
            
            for estado, cidades in detalhe['cidades_removidas_por_estado'].items():
                print(f"   ❌ Estado {estado}: {len(cidades)} cidades")
                for cidade in cidades[:5]:  # Mostrar apenas as primeiras 5
                    print(f"      - {cidade}")
                if len(cidades) > 5:
                    print(f"      ... e mais {len(cidades) - 5} cidades")
    
    # Perguntar se deve corrigir
    if relatorio['total_cidades_removidas'] > 0:
        resposta = input(f"\nDeseja corrigir os dados removendo {relatorio['total_cidades_removidas']} cidades inconsistentes? (s/N): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            logger.info("Iniciando correção dos dados...")
            dados_corrigidos = corrigir_representantes(dados_representantes, municipio_para_estado)
            
            # Salvar dados corrigidos
            with open('representantes_corrigidos.json', 'w', encoding='utf-8') as f:
                json.dump(dados_corrigidos, f, ensure_ascii=False, indent=2)
            
            logger.info("Dados corrigidos salvos em representantes_corrigidos.json")
            print("\n✅ Correção concluída!")
            print("📁 Arquivos gerados:")
            print("   - representantes_backup_antes_correcao.json (backup original)")
            print("   - representantes_corrigidos.json (dados corrigidos)")
            print("   - relatorio_inconsistencias_estados.json (relatório detalhado)")
        else:
            print("\n❌ Correção cancelada. Apenas o relatório foi gerado.")
    else:
        print("\n✅ Nenhuma inconsistência encontrada! Todos os representantes têm cidades consistentes com seus estados atendidos.")

if __name__ == "__main__":
    main()