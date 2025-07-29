#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar municípios dos estados da SCHIOPPA usando dados do IBGE
"""

import json
import requests
import logging
from pathlib import Path
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Códigos dos estados no IBGE
CODIGOS_ESTADOS = {
    'AC': '12',  # Acre
    'AL': '27',  # Alagoas
    'AP': '16',  # Amapá
    'MA': '21',  # Maranhão
    'RN': '24',  # Rio Grande do Norte
    'RO': '11',  # Rondônia
    'RR': '14',  # Roraima
    'SE': '28'   # Sergipe
}

def obter_municipios_ibge(codigo_estado, sigla_estado):
    """Obtém municípios de um estado via API do IBGE"""
    try:
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{codigo_estado}/municipios"
        logger.info(f"Buscando municípios de {sigla_estado} via IBGE...")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        municipios_data = response.json()
        municipios = [municipio['nome'] for municipio in municipios_data]
        
        logger.info(f"Estado {sigla_estado}: {len(municipios)} municípios encontrados")
        return municipios
        
    except Exception as e:
        logger.error(f"Erro ao obter municípios de {sigla_estado}: {e}")
        return []

def obter_todos_municipios_schioppa():
    """Obtém todos os municípios dos estados da SCHIOPPA"""
    todos_municipios = []
    municipios_por_estado = {}
    
    for sigla, codigo in CODIGOS_ESTADOS.items():
        municipios = obter_municipios_ibge(codigo, sigla)
        if municipios:
            municipios_por_estado[sigla] = municipios
            todos_municipios.extend(municipios)
            time.sleep(0.5)  # Evitar sobrecarga da API
        else:
            logger.warning(f"Nenhum município encontrado para {sigla}")
    
    logger.info(f"Total de municípios coletados: {len(todos_municipios)}")
    return todos_municipios, municipios_por_estado

def atualizar_schioppa_com_municipios():
    """Atualiza os dados da SCHIOPPA com todos os municípios"""
    try:
        json_path = Path('old/representantes.json')
        
        if not json_path.exists():
            logger.error(f"Arquivo JSON não encontrado: {json_path}")
            return False
        
        # Obter municípios via IBGE
        todos_municipios, municipios_por_estado = obter_todos_municipios_schioppa()
        
        if not todos_municipios:
            logger.error("Nenhum município foi obtido")
            return False
        
        # Carregar dados atuais
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Atualizar dados da SCHIOPPA
        if 'representantes' in data and 'schioppa' in data['representantes']:
            schioppa_data = data['representantes']['schioppa']
            
            # Backup dos dados originais
            logger.info(f"Dados originais da SCHIOPPA:")
            logger.info(f"  Cidades: {len(schioppa_data.get('cidades', []))}")
            
            # Estados da SCHIOPPA
            estados_schioppa = list(CODIGOS_ESTADOS.keys())
            
            # Atualizar com novos dados
            schioppa_data.update({
                'codigo': '01',
                'nome': 'SCHIOPPA',
                'contato': {
                    'nome_contato': 'Schioppa',
                    'email': 'vendas@schioppa.com.br',
                    'celular': '11-99154-6727'
                },
                'estados': [f"{estado}   " for estado in estados_schioppa],
                'cidades': sorted(todos_municipios),
                'observacoes': f'Atende TODOS os municípios dos estados: {", ".join(estados_schioppa)}',
                'total_cidades': len(todos_municipios),
                'estados_atendidos': [f"{estado}   " for estado in estados_schioppa],
                'cor_padrao': '#3b82f6',
                'atende_estado_completo': True,
                'municipios_por_estado': municipios_por_estado
            })
            
            logger.info(f"\nDados atualizados da SCHIOPPA:")
            logger.info(f"  Estados: {len(schioppa_data['estados'])}")
            logger.info(f"  Cidades: {len(schioppa_data['cidades'])}")
            
        else:
            logger.error("SCHIOPPA não encontrada nos dados")
            return False
        
        # Atualizar mapeamento de cidades
        if 'mapeamento_cidades' in data:
            logger.info("Atualizando mapeamento de cidades...")
            
            cidades_adicionadas = 0
            for cidade in todos_municipios:
                # Normalizar nome da cidade
                cidade_normalizada = cidade.lower().strip()
                cidade_normalizada = cidade_normalizada.replace('ã', 'a').replace('ç', 'c')
                cidade_normalizada = cidade_normalizada.replace('á', 'a').replace('é', 'e')
                cidade_normalizada = cidade_normalizada.replace('í', 'i').replace('ó', 'o')
                cidade_normalizada = cidade_normalizada.replace('ú', 'u').replace('ô', 'o')
                cidade_normalizada = cidade_normalizada.replace('â', 'a').replace('ê', 'e')
                
                if cidade_normalizada:
                    data['mapeamento_cidades'][cidade_normalizada] = 'SCHIOPPA'
                    cidades_adicionadas += 1
            
            logger.info(f"Adicionadas {cidades_adicionadas} cidades ao mapeamento")
        
        # Atualizar metadados
        if 'metadados' in data:
            data['metadados']['data_correcao_schioppa'] = '2025-07-29T13:30:00'
            data['metadados']['observacoes_correcao'] = 'SCHIOPPA corrigida com dados do IBGE para atender todos os municípios dos estados: SE, RR, RN, AL, RO, MA, AP, AC'
        
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
        logger.error(f"Erro ao atualizar SCHIOPPA: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🔧 Iniciando correção da SCHIOPPA com dados do IBGE...")
    
    sucesso = atualizar_schioppa_com_municipios()
    
    if sucesso:
        logger.info("\n🎉 Correção da SCHIOPPA concluída com sucesso!")
        logger.info("\n📋 Resumo das alterações:")
        logger.info("   • SCHIOPPA agora atende 8 estados completos: SE, RR, RN, AL, RO, MA, AP, AC")
        logger.info("   • Todos os municípios desses estados foram adicionados via IBGE")
        logger.info("   • Mapeamento de cidades atualizado")
        logger.info("   • Dados de contato atualizados")
        logger.info("   • Cor azul padrão (#3b82f6) configurada")
    else:
        logger.error("\n❌ Falha na correção da SCHIOPPA")

if __name__ == '__main__':
    main()