#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para processar arquivo Excel com representantes e atualizar representantes.json
Processa as abas 'Listagem' e 'Resumo' do arquivo rep.xlsx
"""

import pandas as pd
import json
import os
from pathlib import Path
import logging
from typing import Dict, List, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def normalizar_string(texto: str) -> str:
    """Normaliza string removendo acentos e convertendo para minúsculas"""
    if not isinstance(texto, str):
        return str(texto).strip()
    
    import unicodedata
    # Remove acentos
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sem_acentos = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
    return texto_sem_acentos.lower().strip()

def processar_aba_listagem(df_listagem: pd.DataFrame) -> Dict[str, Any]:
    """Processa a aba Listagem do Excel"""
    logger.info(f"Processando aba Listagem com {len(df_listagem)} registros")
    
    # Mostrar colunas disponíveis
    logger.info(f"Colunas na aba Listagem: {list(df_listagem.columns)}")
    
    representantes_listagem = {}
    
    # Agrupar por representante
    for nome_rep, grupo in df_listagem.groupby('NomeRepresentante'):
        try:
            # Pegar primeira linha do grupo para dados do representante
            primeira_linha = grupo.iloc[0]
            
            representante = {
                'codigo': str(primeira_linha.get('CodigoRepresentante', '')).strip(),
                'nome': str(nome_rep).strip(),
                'contato': {
                    'nome_contato': str(primeira_linha.get('Contato', '')).strip(),
                    'email': str(primeira_linha.get('email', '')).strip(),
                    'celular': str(primeira_linha.get('celular', '')).strip()
                },
                'estados': list(grupo['SiglaEstado'].dropna().unique()),
                'cidades': [],
                'observacoes': str(primeira_linha.get('obs', '')).strip()
            }
            
            # Coletar todas as cidades do representante
            cidades_unicas = set()
            for _, row in grupo.iterrows():
                cidade = str(row.get('Cidade', '')).strip()
                if cidade and cidade != 'nan':
                    cidades_unicas.add(cidade)
            
            representante['cidades'] = sorted(list(cidades_unicas))
            representante['total_cidades'] = len(representante['cidades'])
            
            # Usar nome como chave
            chave = normalizar_string(representante['nome'])
            if chave and representante['nome']:
                representantes_listagem[chave] = representante
                
        except Exception as e:
            logger.warning(f"Erro ao processar representante {nome_rep}: {e}")
            continue
    
    logger.info(f"Processados {len(representantes_listagem)} representantes da aba Listagem")
    return representantes_listagem

def processar_aba_resumo(df_resumo: pd.DataFrame) -> Dict[str, Any]:
    """Processa a aba Resumo do Excel"""
    logger.info(f"Processando aba Resumo com {len(df_resumo)} registros")
    
    # Mostrar colunas disponíveis
    logger.info(f"Colunas na aba Resumo: {list(df_resumo.columns)}")
    
    representantes_resumo = {}
    
    # Agrupar por representante
    for nome_rep, grupo in df_resumo.groupby('NomeRepresentante'):
        try:
            # Pegar primeira linha do grupo para dados do representante
            primeira_linha = grupo.iloc[0]
            
            representante = {
                'codigo': str(primeira_linha.get('CodigoRepresentante', '')).strip(),
                'nome': str(nome_rep).strip(),
                'contato': {
                    'nome_contato': str(primeira_linha.get('Contato', '')).strip(),
                    'email': str(primeira_linha.get('email', '')).strip(),
                    'celular': str(primeira_linha.get('celular', '')).strip()
                },
                'estados_atendidos': list(grupo['SiglaEstado'].dropna().unique()),
                'total_estados': len(list(grupo['SiglaEstado'].dropna().unique())),
                'resumo': 'Dados do resumo de representantes'
            }
            
            # Usar nome como chave
            chave = normalizar_string(representante['nome'])
            if chave and representante['nome']:
                representantes_resumo[chave] = representante
                
        except Exception as e:
            logger.warning(f"Erro ao processar representante {nome_rep}: {e}")
            continue
    
    logger.info(f"Processados {len(representantes_resumo)} representantes da aba Resumo")
    return representantes_resumo

def mesclar_dados(listagem: Dict, resumo: Dict) -> Dict[str, Any]:
    """Mescla os dados das duas abas"""
    logger.info("Mesclando dados das abas Listagem e Resumo")
    
    representantes_final = {}
    
    # Começar com dados da listagem (mais detalhados)
    for chave, dados_listagem in listagem.items():
        representante_final = dados_listagem.copy()
        
        # Adicionar dados do resumo se existir
        if chave in resumo:
            dados_resumo = resumo[chave]
            representante_final.update({
                'total_cidades': dados_resumo.get('total_cidades', len(dados_listagem.get('cidades', []))),
                'estados_atendidos': dados_resumo.get('estados_atendidos', []),
                'resumo_atividades': dados_resumo.get('resumo_atividades', ''),
                'performance': dados_resumo.get('performance', {})
            })
        
        representantes_final[chave] = representante_final
    
    # Adicionar representantes que só existem no resumo
    for chave, dados_resumo in resumo.items():
        if chave not in representantes_final:
            representantes_final[chave] = dados_resumo
    
    logger.info(f"Total de representantes após mesclagem: {len(representantes_final)}")
    return representantes_final

def criar_mapeamento_cidades(representantes: Dict) -> Dict[str, str]:
    """Cria mapeamento cidade -> representante para compatibilidade"""
    mapeamento = {}
    
    for nome_rep, dados in representantes.items():
        nome_original = dados.get('nome', nome_rep)
        cidades = dados.get('cidades', [])
        
        for cidade in cidades:
            cidade_normalizada = normalizar_string(cidade)
            if cidade_normalizada:
                mapeamento[cidade_normalizada] = nome_original
    
    logger.info(f"Criado mapeamento para {len(mapeamento)} cidades")
    return mapeamento

def main():
    """Função principal"""
    try:
        # Caminhos dos arquivos
        excel_path = Path('old/rep.xlsx')
        json_path = Path('old/representantes.json')
        
        if not excel_path.exists():
            logger.error(f"Arquivo Excel não encontrado: {excel_path}")
            return
        
        logger.info(f"Processando arquivo: {excel_path}")
        
        # Ler as abas do Excel
        try:
            df_listagem = pd.read_excel(excel_path, sheet_name='Listagem')
            logger.info(f"Aba 'Listagem' carregada com {len(df_listagem)} linhas")
        except Exception as e:
            logger.warning(f"Erro ao carregar aba 'Listagem': {e}")
            df_listagem = pd.DataFrame()
        
        try:
            df_resumo = pd.read_excel(excel_path, sheet_name='Resumo')
            logger.info(f"Aba 'Resumo' carregada com {len(df_resumo)} linhas")
        except Exception as e:
            logger.warning(f"Erro ao carregar aba 'Resumo': {e}")
            df_resumo = pd.DataFrame()
        
        if df_listagem.empty and df_resumo.empty:
            logger.error("Nenhuma aba foi carregada com sucesso")
            return
        
        # Processar cada aba
        representantes_listagem = processar_aba_listagem(df_listagem) if not df_listagem.empty else {}
        representantes_resumo = processar_aba_resumo(df_resumo) if not df_resumo.empty else {}
        
        # Mesclar dados
        representantes_final = mesclar_dados(representantes_listagem, representantes_resumo)
        
        # Criar mapeamento de cidades
        mapeamento_cidades = criar_mapeamento_cidades(representantes_final)
        
        # Estrutura final do JSON
        dados_finais = {
            'representantes': representantes_final,
            'mapeamento_cidades': mapeamento_cidades,
            'metadados': {
                'total_representantes': len(representantes_final),
                'total_cidades_mapeadas': len(mapeamento_cidades),
                'fonte': 'rep.xlsx',
                'abas_processadas': {
                    'listagem': len(representantes_listagem),
                    'resumo': len(representantes_resumo)
                },
                'data_processamento': pd.Timestamp.now().isoformat()
            }
        }
        
        # Salvar JSON atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Arquivo {json_path} atualizado com sucesso!")
        logger.info(f"Total de representantes: {len(representantes_final)}")
        logger.info(f"Total de cidades mapeadas: {len(mapeamento_cidades)}")
        
        # Mostrar alguns exemplos
        logger.info("\n=== EXEMPLOS DE REPRESENTANTES ===")
        for i, (chave, dados) in enumerate(list(representantes_final.items())[:3]):
            logger.info(f"\n{i+1}. {dados.get('nome', chave)}")
            logger.info(f"   Região: {dados.get('regiao', 'N/A')}")
            logger.info(f"   Estado: {dados.get('estado', 'N/A')}")
            logger.info(f"   Cidades: {len(dados.get('cidades', []))}")
            if dados.get('cidades'):
                logger.info(f"   Primeiras cidades: {', '.join(dados['cidades'][:3])}")
        
    except Exception as e:
        logger.error(f"Erro durante o processamento: {e}")
        raise

if __name__ == '__main__':
    main()