#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir completamente os dados da SCHIOPPA
Adicionando todos os municípios dos estados: SE, RR, RN, AL, RO, MA, AP, AC
"""

import json
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def obter_municipios_por_estado():
    """Obtém todos os municípios dos estados da SCHIOPPA do arquivo GeoJSON"""
    try:
        geojson_path = Path('old/geojs-100-mun-v2.json')
        
        if not geojson_path.exists():
            logger.error(f"Arquivo GeoJSON não encontrado: {geojson_path}")
            return {}
        
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        estados_schioppa = ['SE', 'RR', 'RN', 'AL', 'RO', 'MA', 'AP', 'AC']
        municipios_por_estado = {estado: [] for estado in estados_schioppa}
        
        logger.info(f"Processando {len(geojson_data.get('features', []))} municípios do GeoJSON...")
        
        for feature in geojson_data.get('features', []):
            props = feature.get('properties', {})
            
            # Extrair UF e nome do município
            uf_municipio = props.get('uf_municipio', '')
            if ' - ' in uf_municipio:
                uf, municipio = uf_municipio.split(' - ', 1)
                uf = uf.strip()
                municipio = municipio.strip()
                
                if uf in estados_schioppa:
                    municipios_por_estado[uf].append(municipio)
        
        # Remover duplicatas e ordenar
        for estado in estados_schioppa:
            municipios_por_estado[estado] = sorted(list(set(municipios_por_estado[estado])))
            logger.info(f"Estado {estado}: {len(municipios_por_estado[estado])} municípios")
        
        return municipios_por_estado
        
    except Exception as e:
        logger.error(f"Erro ao obter municípios: {e}")
        return {}

def corrigir_schioppa():
    """Corrige os dados da SCHIOPPA no arquivo JSON"""
    try:
        json_path = Path('old/representantes.json')
        
        if not json_path.exists():
            logger.error(f"Arquivo JSON não encontrado: {json_path}")
            return False
        
        # Carregar dados atuais
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Obter municípios dos estados
        municipios_por_estado = obter_municipios_por_estado()
        
        if not municipios_por_estado:
            logger.error("Não foi possível obter municípios dos estados")
            return False
        
        # Coletar todas as cidades dos estados da SCHIOPPA
        todas_cidades_schioppa = []
        for estado, municipios in municipios_por_estado.items():
            todas_cidades_schioppa.extend(municipios)
        
        logger.info(f"Total de cidades para SCHIOPPA: {len(todas_cidades_schioppa)}")
        
        # Atualizar dados da SCHIOPPA
        if 'representantes' in data and 'schioppa' in data['representantes']:
            schioppa_data = data['representantes']['schioppa']
            
            # Backup dos dados originais
            logger.info(f"Dados originais da SCHIOPPA:")
            logger.info(f"  Estados: {schioppa_data.get('estados', [])}")
            logger.info(f"  Cidades: {len(schioppa_data.get('cidades', []))}")
            logger.info(f"  Estados atendidos: {schioppa_data.get('estados_atendidos', [])}")
            
            # Atualizar com novos dados
            estados_completos = ['SE', 'RR', 'RN', 'AL', 'RO', 'MA', 'AP', 'AC']
            
            schioppa_data.update({
                'codigo': '01',
                'nome': 'SCHIOPPA',
                'contato': {
                    'nome_contato': 'Schioppa',
                    'email': 'vendas@schioppa.com.br',
                    'celular': '11-99154-6727'
                },
                'estados': [f"{estado}   " for estado in estados_completos],
                'cidades': todas_cidades_schioppa,
                'observacoes': f'Atende TODOS os municípios dos estados: {", ".join(estados_completos)}',
                'total_cidades': len(todas_cidades_schioppa),
                'estados_atendidos': [f"{estado}   " for estado in estados_completos],
                'cor_padrao': '#3b82f6',
                'atende_estado_completo': True
            })
            
            logger.info(f"\nDados atualizados da SCHIOPPA:")
            logger.info(f"  Estados: {len(schioppa_data['estados'])}")
            logger.info(f"  Cidades: {len(schioppa_data['cidades'])}")
            logger.info(f"  Estados atendidos: {len(schioppa_data['estados_atendidos'])}")
            
        else:
            logger.error("SCHIOPPA não encontrada nos dados")
            return False
        
        # Atualizar mapeamento de cidades
        if 'mapeamento_cidades' in data:
            logger.info("Atualizando mapeamento de cidades...")
            
            # Adicionar todas as cidades da SCHIOPPA ao mapeamento
            cidades_adicionadas = 0
            for cidade in todas_cidades_schioppa:
                cidade_normalizada = cidade.lower().strip()
                if cidade_normalizada:
                    data['mapeamento_cidades'][cidade_normalizada] = 'SCHIOPPA'
                    cidades_adicionadas += 1
            
            logger.info(f"Adicionadas {cidades_adicionadas} cidades ao mapeamento")
        
        # Atualizar metadados
        if 'metadados' in data:
            data['metadados']['data_correcao_schioppa'] = '2025-07-29T13:30:00'
            data['metadados']['observacoes_correcao'] = 'SCHIOPPA corrigida para atender todos os municípios dos estados: SE, RR, RN, AL, RO, MA, AP, AC'
        
        # Salvar arquivo atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n✅ Arquivo {json_path} atualizado com sucesso!")
        
        # Mostrar resumo por estado
        logger.info("\n📊 RESUMO POR ESTADO:")
        for estado, municipios in municipios_por_estado.items():
            logger.info(f"  {estado}: {len(municipios)} municípios")
            if municipios:
                logger.info(f"    Exemplos: {', '.join(municipios[:3])}{'...' if len(municipios) > 3 else ''}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao corrigir SCHIOPPA: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🔧 Iniciando correção completa da SCHIOPPA...")
    
    sucesso = corrigir_schioppa()
    
    if sucesso:
        logger.info("\n🎉 Correção da SCHIOPPA concluída com sucesso!")
        logger.info("\n📋 Resumo das alterações:")
        logger.info("   • SCHIOPPA agora atende 8 estados completos: SE, RR, RN, AL, RO, MA, AP, AC")
        logger.info("   • Todos os municípios desses estados foram adicionados")
        logger.info("   • Mapeamento de cidades atualizado")
        logger.info("   • Dados de contato atualizados")
        logger.info("   • Cor azul padrão (#3b82f6) configurada")
    else:
        logger.error("\n❌ Falha na correção da SCHIOPPA")

if __name__ == '__main__':
    main()