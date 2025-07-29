#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para corrigir inconsistências do Schioppa na pasta old.
Remove cidades que claramente não pertencem aos estados válidos.
"""

import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def obter_cidades_conhecidas_outros_estados():
    """Retorna cidades conhecidamente de outros estados que não devem estar no Schioppa."""
    
    # Estados válidos para Schioppa: AC, AL, AP, MA, RN, RO, RR, SE
    # Vamos remover cidades que são claramente de outros estados
    
    cidades_outros_estados = {
        # São Paulo
        "salto de pirapora", "vargem grande paulista", "barueri", "carapicuiba", 
        "cotia", "jandira", "osasco", "pirapora do bom jesus", "santana de parnaiba",
        "jundia", "vera cruz", "santa maria", "sao sebastiao", "campo grande",
        "cedral", "palestina", "vicosa",
        
        # Paraíba
        "bom jardim", "santa rita", "sao bento", "viana", "campestre", 
        "nova uniao", "ouro branco", "santa luzia", "sao joao batista",
        "agua branca", "bom jesus", "piranhas", "pacatuba", "sao goncalo do amarante",
        "sao pedro",
        
        # Santa Catarina  
        "campo alegre", "lajes", "maravilha",
        
        # Mato Grosso
        "tangara",
        
        # Pará
        "santa helena", "sao miguel", "sao tome", "sao vicente",
    }
    
    return cidades_outros_estados

def identificar_e_remover_cidades_incorretas(arquivo_path: str):
    """Identifica e remove cidades incorretas do arquivo."""
    
    logger.info(f"Processando arquivo: {arquivo_path}")
    
    try:
        # Carregar dados
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Obter lista de cidades de outros estados
        cidades_outros_estados = obter_cidades_conhecidas_outros_estados()
        
        # Identificar cidades incorretas
        cidades_incorretas = []
        for key, value in data.items():
            if isinstance(value, str) and value == "SCHIOPPA":
                cidade_nome = key.strip().lower()
                if cidade_nome in cidades_outros_estados:
                    cidades_incorretas.append(key)
        
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
    logger.info("Iniciando correção simplificada de inconsistências do Schioppa na pasta old")
    
    # Estados válidos para Schioppa
    logger.info("Estados válidos para Schioppa: AC, AL, AP, MA, RN, RO, RR, SE")
    
    # Arquivos para corrigir
    arquivos = [
        'old/representantes.json',
        'old/representantes_backup.json'
    ]
    
    for arquivo in arquivos:
        try:
            identificar_e_remover_cidades_incorretas(arquivo)
        except FileNotFoundError:
            logger.warning(f"Arquivo não encontrado: {arquivo}")
        except Exception as e:
            logger.error(f"Erro ao processar {arquivo}: {e}")
    
    logger.info("Correção concluída!")

if __name__ == "__main__":
    main() 