#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover definitivamente as cidades problemáticas da SCHIOPPA
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

# Cidades que devem ser removidas da SCHIOPPA (estados incorretos)
CIDADES_PARA_REMOVER = [
    'barcelona',      # RN, mas aparece como se fosse de outro estado
    'ceara-mirim',    # RN, mas aparece como se fosse do CE
    'cedral',         # SP, SCHIOPPA não atende SP
    'sao vicente',    # SP
    'salto de pirapora',  # SP
    'vargem grande paulista',  # SP
    'palestina',      # SP
    'pacatuba',       # CE (existe no CE e RN, mas mapeamento está incorreto)
    'sao goncalo do amarante',  # CE
    'sao pedro',      # SP
    'santa helena',   # SC
    'sao miguel',     # Pode ser RN (OK) ou outro estado
    'sao tome',       # RN (OK) ou outro estado
    'barueri',        # SP
    'carapicuiba',    # SP
    'cotia',          # SP
    'jandira',        # SP
    'osasco',         # SP
    'pirapora do bom jesus',  # SP
    'santana de parnaiba',    # SP
    'jundia',         # SP
    'campo alegre',   # SC
    'lajes',          # SC
    'maravilha',      # SC
    'tangara',        # SC
    'iracema',        # CE
    'vera cruz',      # BA
    'vicosa',         # MG
]

def remover_cidades_problematicas():
    """Remove cidades problemáticas do mapeamento da SCHIOPPA"""
    try:
        json_path = Path('old/representantes.json')
        
        if not json_path.exists():
            logger.error(f"Arquivo JSON não encontrado: {json_path}")
            return False
        
        # Carregar dados atuais
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'mapeamento_cidades' not in data:
            logger.error("Seção 'mapeamento_cidades' não encontrada")
            return False
        
        mapeamento = data['mapeamento_cidades']
        cidades_removidas = []
        
        # Remover cada cidade problemática
        for cidade in CIDADES_PARA_REMOVER:
            if cidade in mapeamento and mapeamento[cidade] == 'SCHIOPPA':
                logger.info(f"Removendo '{cidade}' da SCHIOPPA")
                del mapeamento[cidade]
                cidades_removidas.append(cidade)
            elif cidade in mapeamento:
                logger.info(f"'{cidade}' encontrada mas não está mapeada para SCHIOPPA (atual: {mapeamento[cidade]})")
            else:
                logger.info(f"'{cidade}' não encontrada no mapeamento")
        
        # Contar cidades restantes da SCHIOPPA
        cidades_schioppa_restantes = [cidade for cidade, rep in mapeamento.items() if rep == 'SCHIOPPA']
        
        # Atualizar metadados
        if 'metadados' in data:
            data['metadados']['data_correcao_final_schioppa'] = '2025-07-29T16:30:00'
            data['metadados']['cidades_removidas_schioppa'] = cidades_removidas
            data['metadados']['total_cidades_schioppa_apos_correcao'] = len(cidades_schioppa_restantes)
        
        # Salvar arquivo atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n✅ Correção final da SCHIOPPA concluída!")
        logger.info(f"\n📊 RESUMO:")
        logger.info(f"   • Cidades removidas: {len(cidades_removidas)}")
        logger.info(f"   • Cidades SCHIOPPA restantes: {len(cidades_schioppa_restantes)}")
        
        if cidades_removidas:
            logger.info(f"\n🗑️ CIDADES REMOVIDAS:")
            for cidade in cidades_removidas:
                logger.info(f"   - {cidade}")
        
        # Mostrar algumas cidades restantes para verificação
        if cidades_schioppa_restantes:
            logger.info(f"\n✅ PRIMEIRAS 10 CIDADES RESTANTES DA SCHIOPPA:")
            for cidade in sorted(cidades_schioppa_restantes)[:10]:
                logger.info(f"   - {cidade}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao remover cidades problemáticas: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🔧 Iniciando remoção final de cidades problemáticas da SCHIOPPA...")
    
    sucesso = remover_cidades_problematicas()
    
    if sucesso:
        logger.info("\n🎉 Correção final concluída com sucesso!")
        logger.info("\n📋 A SCHIOPPA agora deve atender apenas:")
        logger.info("   • SE (Sergipe)")
        logger.info("   • RR (Roraima)")
        logger.info("   • RN (Rio Grande do Norte)")
        logger.info("   • AL (Alagoas)")
        logger.info("   • RO (Rondônia)")
        logger.info("   • MA (Maranhão)")
        logger.info("   • AP (Amapá)")
        logger.info("   • AC (Acre)")
    else:
        logger.error("\n❌ Falha na correção final")

if __name__ == '__main__':
    main()