#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir inconsistências do Schioppa na pasta old.
Remove cidades que não pertencem aos estados corretos.
"""

import json
import logging
from typing import Dict, Set, List

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_municipios_por_estado() -> Dict[str, Set[str]]:
    """Carrega o mapeamento de municípios por estado do arquivo geojs."""
    try:
        with open('old/geojs-100-mun-v2.json', 'r', encoding='utf-8') as f:
            geojs_data = json.load(f)
        
        municipios_por_estado = {}
        
        # O arquivo geojs tem uma estrutura com features
        for feature in geojs_data.get('features', []):
            properties = feature.get('properties', {})
            nome = properties.get('name', '').strip().lower()
            estado_sigla = properties.get('sigla_uf', '').strip()
            
            if estado_sigla and nome:
                if estado_sigla not in municipios_por_estado:
                    municipios_por_estado[estado_sigla] = set()
                municipios_por_estado[estado_sigla].add(nome)
        
        logger.info(f"Carregados municípios de {len(municipios_por_estado)} estados do arquivo geojs")
        return municipios_por_estado
        
    except Exception as e:
        logger.error(f"Erro ao carregar geojs-100-mun-v2.json: {e}")
        return {}

def normalizar_nome_cidade(nome: str) -> str:
    """Normaliza nome da cidade para comparação."""
    return nome.strip().lower().replace('_', ' ')

def identificar_cidades_incorretas(representantes_data: Dict, municipios_por_estado: Dict[str, Set[str]]) -> List[str]:
    """Identifica cidades incorretamente atribuídas ao Schioppa."""
    
    # Estados válidos para Schioppa
    estados_schioppa = {'AC', 'AL', 'AP', 'MA', 'RN', 'RO', 'RR', 'SE'}
    
    # Obter todas as cidades válidas dos estados do Schioppa
    cidades_validas = set()
    for estado in estados_schioppa:
        if estado in municipios_por_estado:
            cidades_validas.update(municipios_por_estado[estado])
    
    logger.info(f"Estados válidos para Schioppa: {estados_schioppa}")
    logger.info(f"Total de cidades válidas: {len(cidades_validas)}")
    
    # Identificar mapeamento de cidades
    mapeamento_cidades = {}
    cidades_incorretas = []
    
    # Procurar na seção de mapeamento direto de cidades
    for key, value in representantes_data.items():
        if isinstance(value, str) and value == "SCHIOPPA":
            cidade_nome = normalizar_nome_cidade(key)
            
            # Verificar se a cidade pertence aos estados válidos
            if cidade_nome not in cidades_validas:
                # Verificar se a cidade existe em outros estados
                cidade_encontrada_em = []
                for estado, cidades in municipios_por_estado.items():
                    if cidade_nome in cidades and estado not in estados_schioppa:
                        cidade_encontrada_em.append(estado)
                
                if cidade_encontrada_em:
                    logger.warning(f"Cidade '{key}' está atribuída ao Schioppa mas pertence ao(s) estado(s): {cidade_encontrada_em}")
                    cidades_incorretas.append(key)
                else:
                    logger.warning(f"Cidade '{key}' não encontrada em nenhum estado válido")
    
    return cidades_incorretas

def corrigir_arquivo_representantes(arquivo_path: str, municipios_por_estado: Dict[str, Set[str]]):
    """Corrige as inconsistências no arquivo de representantes."""
    
    logger.info(f"Processando arquivo: {arquivo_path}")
    
    try:
        # Carregar dados
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Identificar cidades incorretas
        cidades_incorretas = identificar_cidades_incorretas(data, municipios_por_estado)
        
        if not cidades_incorretas:
            logger.info("Nenhuma inconsistência encontrada!")
            return
        
        logger.info(f"Encontradas {len(cidades_incorretas)} cidades incorretas:")
        for cidade in cidades_incorretas:
            logger.info(f"  - {cidade}")
        
        # Fazer backup
        backup_path = arquivo_path.replace('.json', '_backup_antes_correcao.json')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Backup criado: {backup_path}")
        
        # Remover cidades incorretas
        removidas = 0
        for cidade in cidades_incorretas:
            if cidade in data and data[cidade] == "SCHIOPPA":
                del data[cidade]
                removidas += 1
                logger.info(f"Removida: {cidade}")
        
        # Salvar arquivo corrigido
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Arquivo corrigido! Removidas {removidas} cidades incorretas.")
        
    except Exception as e:
        logger.error(f"Erro ao processar arquivo {arquivo_path}: {e}")

def main():
    """Função principal."""
    logger.info("Iniciando correção de inconsistências do Schioppa na pasta old")
    
    # Carregar referência de municípios
    municipios_por_estado = carregar_municipios_por_estado()
    
    if not municipios_por_estado:
        logger.error("Não foi possível carregar dados de municípios")
        return
    
    # Arquivos para corrigir
    arquivos = [
        'old/representantes.json',
        'old/representantes_backup.json'
    ]
    
    for arquivo in arquivos:
        try:
            corrigir_arquivo_representantes(arquivo, municipios_por_estado)
        except FileNotFoundError:
            logger.warning(f"Arquivo não encontrado: {arquivo}")
        except Exception as e:
            logger.error(f"Erro ao processar {arquivo}: {e}")
    
    logger.info("Correção concluída!")

if __name__ == "__main__":
    main() 