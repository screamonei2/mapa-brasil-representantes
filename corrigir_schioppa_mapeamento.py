#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o mapeamento incorreto da SCHIOPPA
Remove cidades de estados que a SCHIOPPA não deveria atender
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

# Estados que a SCHIOPPA DEVE atender
ESTADOS_SCHIOPPA = {'SE', 'RR', 'RN', 'AL', 'RO', 'MA', 'AP', 'AC'}

# Mapeamento de cidades problemáticas encontradas para seus estados corretos
CIDADES_PROBLEMATICAS = {
    # Ceará (CE) - não deveria ter SCHIOPPA
    'ceara-mirim': 'RN',  # Na verdade é do Rio Grande do Norte
    'barcelona': 'RN',    # Na verdade é do Rio Grande do Norte
    
    # São Paulo (SP) - não deveria ter SCHIOPPA
    'cedral': 'SP',
    'sao vicente': 'SP',
    'salto de pirapora': 'SP',
    'vargem grande paulista': 'SP',
    'palestina': 'SP',
    'pacatuba': 'CE',  # Pacatuba existe no CE e RN, mas no mapeamento está como SP
    'sao goncalo do amarante': 'CE',  # Existe no CE e RN
    'sao pedro': 'SP',
    'santa helena': 'SC',
    'sao miguel': 'RN',
    'sao tome': 'RN',
    'barueri': 'SP',
    'carapicuiba': 'SP',
    'cotia': 'SP',
    'jandira': 'SP',
    'osasco': 'SP',
    'pirapora do bom jesus': 'SP',
    'santana de parnaiba': 'SP',
    'jundia': 'SP',
    
    # Santa Catarina (SC) - não deveria ter SCHIOPPA
    'campo alegre': 'SC',
    'lajes': 'SC',
    'maravilha': 'SC',
    'tangara': 'SC',
    
    # Rondônia (RO) - SCHIOPPA DEVE atender, então manter
    'cerejeiras': 'RO',  # OK - RO está na lista
    'iracema': 'CE',     # Iracema do Ceará, não deveria ter SCHIOPPA
    
    # Sergipe (SE) - SCHIOPPA DEVE atender, então manter
    'cedro de sao joao': 'SE',  # OK - SE está na lista
    
    # Alagoas (AL) - SCHIOPPA DEVE atender, então manter
    'agua branca': 'AL',  # OK - AL está na lista
    'bom jesus': 'AL',    # OK - AL está na lista
    'campestre': 'AL',    # OK - AL está na lista
    'campo grande': 'AL', # OK - AL está na lista
    
    # Maranhão (MA) - SCHIOPPA DEVE atender, então manter
    'nova uniao': 'MA',   # OK - MA está na lista
    'ouro branco': 'MA',  # OK - MA está na lista
    'santa luzia': 'MA',  # OK - MA está na lista
    'sao joao batista': 'MA',  # OK - MA está na lista
    'sao sebastiao': 'MA',     # OK - MA está na lista
    'santa maria': 'MA',       # OK - MA está na lista
    'vera cruz': 'BA',         # Vera Cruz da Bahia, não deveria ter SCHIOPPA
    'vicosa': 'MG',           # Viçosa de MG, não deveria ter SCHIOPPA
}

def corrigir_mapeamento_schioppa():
    """Corrige o mapeamento incorreto da SCHIOPPA"""
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
        cidades_mantidas = []
        
        # Verificar cada cidade mapeada para SCHIOPPA
        for cidade, representante in list(mapeamento.items()):
            if representante == 'SCHIOPPA':
                # Verificar se a cidade está na lista de problemáticas
                if cidade in CIDADES_PROBLEMATICAS:
                    estado_real = CIDADES_PROBLEMATICAS[cidade]
                    
                    # Se o estado real NÃO está na lista de estados da SCHIOPPA
                    if estado_real not in ESTADOS_SCHIOPPA:
                        logger.info(f"Removendo '{cidade}' da SCHIOPPA (estado: {estado_real})")
                        del mapeamento[cidade]
                        cidades_removidas.append(f"{cidade} ({estado_real})")
                    else:
                        logger.info(f"Mantendo '{cidade}' na SCHIOPPA (estado: {estado_real} - OK)")
                        cidades_mantidas.append(f"{cidade} ({estado_real})")
                else:
                    # Cidade não está na lista problemática, assumir que está correta
                    cidades_mantidas.append(cidade)
        
        # Atualizar metadados
        if 'metadados' in data:
            data['metadados']['data_correcao_mapeamento_schioppa'] = '2025-07-29T16:00:00'
            data['metadados']['observacoes_mapeamento'] = f'Removidas {len(cidades_removidas)} cidades incorretas da SCHIOPPA'
        
        # Salvar arquivo atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n✅ Correção do mapeamento da SCHIOPPA concluída!")
        logger.info(f"\n📊 RESUMO:")
        logger.info(f"   • Cidades removidas: {len(cidades_removidas)}")
        logger.info(f"   • Cidades mantidas: {len(cidades_mantidas)}")
        
        if cidades_removidas:
            logger.info(f"\n🗑️ CIDADES REMOVIDAS:")
            for cidade in cidades_removidas:
                logger.info(f"   - {cidade}")
        
        if cidades_mantidas:
            logger.info(f"\n✅ CIDADES MANTIDAS (estados corretos):")
            for cidade in cidades_mantidas[:10]:  # Mostrar apenas as primeiras 10
                logger.info(f"   - {cidade}")
            if len(cidades_mantidas) > 10:
                logger.info(f"   ... e mais {len(cidades_mantidas) - 10} cidades")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao corrigir mapeamento da SCHIOPPA: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🔧 Iniciando correção do mapeamento da SCHIOPPA...")
    logger.info(f"Estados que a SCHIOPPA DEVE atender: {', '.join(sorted(ESTADOS_SCHIOPPA))}")
    
    sucesso = corrigir_mapeamento_schioppa()
    
    if sucesso:
        logger.info("\n🎉 Correção concluída com sucesso!")
        logger.info("\n📋 O que foi feito:")
        logger.info("   • Removidas cidades de estados incorretos")
        logger.info("   • Mantidas cidades dos estados corretos (SE, RR, RN, AL, RO, MA, AP, AC)")
        logger.info("   • Metadados atualizados")
    else:
        logger.error("\n❌ Falha na correção do mapeamento")

if __name__ == '__main__':
    main()