#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar especificamente os dados da SCHIOPPA no Excel
"""

import pandas as pd
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def analisar_schioppa_excel():
    """Analisa os dados da SCHIOPPA no Excel"""
    try:
        excel_path = Path('old/rep.xlsx')
        
        if not excel_path.exists():
            logger.error(f"Arquivo Excel não encontrado: {excel_path}")
            return
        
        logger.info(f"Analisando dados da SCHIOPPA em: {excel_path}")
        
        # Ler todas as abas disponíveis
        try:
            excel_file = pd.ExcelFile(excel_path)
            logger.info(f"Abas disponíveis: {excel_file.sheet_names}")
        except Exception as e:
            logger.error(f"Erro ao ler arquivo Excel: {e}")
            return
        
        # Analisar cada aba
        for sheet_name in excel_file.sheet_names:
            try:
                logger.info(f"\n=== ANALISANDO ABA: {sheet_name} ===")
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                
                logger.info(f"Total de linhas: {len(df)}")
                logger.info(f"Colunas: {list(df.columns)}")
                
                # Procurar por SCHIOPPA (case insensitive)
                schioppa_mask = df.astype(str).apply(
                    lambda x: x.str.contains('schioppa', case=False, na=False)
                ).any(axis=1)
                
                schioppa_data = df[schioppa_mask]
                
                if len(schioppa_data) > 0:
                    logger.info(f"\n🔍 ENCONTRADOS {len(schioppa_data)} REGISTROS DA SCHIOPPA:")
                    
                    # Mostrar todos os registros da SCHIOPPA
                    for idx, row in schioppa_data.iterrows():
                        logger.info(f"\n--- Registro {idx + 1} ---")
                        for col in df.columns:
                            value = row[col]
                            if pd.notna(value) and str(value).strip():
                                logger.info(f"  {col}: {value}")
                    
                    # Analisar estados únicos
                    if 'SiglaEstado' in df.columns:
                        estados_schioppa = schioppa_data['SiglaEstado'].dropna().unique()
                        logger.info(f"\n📍 ESTADOS DA SCHIOPPA: {list(estados_schioppa)}")
                    
                    # Analisar cidades únicas
                    if 'Cidade' in df.columns:
                        cidades_schioppa = schioppa_data['Cidade'].dropna().unique()
                        logger.info(f"\n🏙️  CIDADES DA SCHIOPPA ({len(cidades_schioppa)}):")
                        for cidade in sorted(cidades_schioppa):
                            logger.info(f"  - {cidade}")
                    
                    # Verificar se há dados dos estados mencionados pelo usuário
                    estados_esperados = ['SE', 'RR', 'RN', 'AL', 'RO', 'MA', 'AP', 'AC']
                    if 'SiglaEstado' in df.columns:
                        estados_encontrados = schioppa_data['SiglaEstado'].dropna().unique()
                        estados_faltando = set(estados_esperados) - set(estados_encontrados)
                        
                        if estados_faltando:
                            logger.warning(f"\n⚠️  ESTADOS ESPERADOS MAS NÃO ENCONTRADOS: {list(estados_faltando)}")
                        else:
                            logger.info(f"\n✅ TODOS OS ESTADOS ESPERADOS ENCONTRADOS!")
                
                else:
                    logger.info(f"❌ Nenhum registro da SCHIOPPA encontrado na aba {sheet_name}")
                    
            except Exception as e:
                logger.error(f"Erro ao processar aba {sheet_name}: {e}")
                continue
        
        # Verificar se há outras variações do nome
        logger.info(f"\n=== PROCURANDO VARIAÇÕES DO NOME ===")
        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                
                # Procurar variações
                variacoes = ['schioppa', 'schiopa', 'skiopa', 'schyoppa']
                for variacao in variacoes:
                    mask = df.astype(str).apply(
                        lambda x: x.str.contains(variacao, case=False, na=False)
                    ).any(axis=1)
                    
                    if mask.any():
                        logger.info(f"Encontrada variação '{variacao}' na aba {sheet_name}: {mask.sum()} registros")
                        
            except Exception as e:
                continue
                
    except Exception as e:
        logger.error(f"Erro durante a análise: {e}")
        raise

if __name__ == '__main__':
    analisar_schioppa_excel()