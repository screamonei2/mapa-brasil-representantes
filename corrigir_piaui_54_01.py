#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o representante 54.01 (FERNANDO MURILO REPRESENTAÇÕES LTDA - ME)
para atender TODOS os 224 municípios do estado do Piauí
"""

import json
import time
from pathlib import Path

def obter_municipios_piaui():
    """Retorna todos os 224 municípios do Piauí"""
    print("Carregando lista completa dos municípios do Piauí...")
    
    # Lista completa dos 224 municípios do Piauí
    municipios_piaui = [
        'ACAUÃ', 'AGRICOLÂNDIA', 'ÁGUA BRANCA', 'ALAGOINHA DO PIAUÍ', 'ALEGRETE DO PIAUÍ',
        'ALTO LONGÁ', 'ALTOS', 'ALVORADA DO GURGUÉIA', 'AMARANTE', 'ANGICAL DO PIAUÍ',
        'ANÍSIO DE ABREU', 'ANTÔNIO ALMEIDA', 'AROAZES', 'AROEIRAS DO ITAIM', 'ARRAIAL',
        'ASSUNÇÃO DO PIAUÍ', 'AVELINO LOPES', 'BAIXA GRANDE DO RIBEIRO', 'BARRA D\'ALCÂNTARA',
        'BARRAS', 'BARREIRAS DO PIAUÍ', 'BARRO DURO', 'BATALHA', 'BELA VISTA DO PIAUÍ',
        'BELÉM DO PIAUÍ', 'BENEDITINOS', 'BERTOLÍNIA', 'BETÂNIA DO PIAUÍ', 'BOA HORA',
        'BOCAINA', 'BOM JESUS', 'BOM PRINCÍPIO DO PIAUÍ', 'BONFIM DO PIAUÍ', 'BOQUEIRÃO DO PIAUÍ',
        'BRASILEIRA', 'BREJO DO PIAUÍ', 'BURITI DOS LOPES', 'BURITI DOS MONTES', 'CABECEIRAS DO PIAUÍ',
        'CAJAZEIRAS DO PIAUÍ', 'CAJUEIRO DA PRAIA', 'CALDEIRÃO GRANDE DO PIAUÍ', 'CAMPINAS DO PIAUÍ',
        'CAMPO ALEGRE DO FIDALGO', 'CAMPO GRANDE DO PIAUÍ', 'CAMPO LARGO DO PIAUÍ', 'CAMPO MAIOR',
        'CANAVIEIRA', 'CANTO DO BURITI', 'CAPITÃO DE CAMPOS', 'CAPITÃO GERVÁSIO OLIVEIRA',
        'CARACOL', 'CARAÚBAS DO PIAUÍ', 'CARIDADE DO PIAUÍ', 'CASTELO DO PIAUÍ', 'CAXINGÓ',
        'COCAL', 'COCAL DE TELHA', 'COCAL DOS ALVES', 'COIVARAS', 'COLÔNIA DO GURGUÉIA',
        'COLÔNIA DO PIAUÍ', 'CONCEIÇÃO DO CANINDÉ', 'CORONEL JOSÉ DIAS', 'CORRENTE',
        'CRISTALÂNDIA DO PIAUÍ', 'CRISTINO CASTRO', 'CURIMATÁ', 'CURRAIS', 'CURRAL NOVO DO PIAUÍ',
        'CURRALINHOS', 'DEMERVAL LOBÃO', 'DIRCEU ARCOVERDE', 'DOM EXPEDITO LOPES', 'DOM INOCÊNCIO',
        'DOMINGOS MOURÃO', 'ELESBÃO VELOSO', 'ELISEU MARTINS', 'ESPERANTINA', 'FARTURA DO PIAUÍ',
        'FLORES DO PIAUÍ', 'FLORESTA DO PIAUÍ', 'FLORIANO', 'FRANCINÓPOLIS', 'FRANCISCO AYRES',
        'FRANCISCO MACEDO', 'FRANCISCO SANTOS', 'FRONTEIRAS', 'GEMINIANO', 'GILBUÉS',
        'GUADALUPE', 'GUARIBAS', 'HUGO NAPOLEÃO', 'ILHA GRANDE', 'INHUMA', 'IPIRANGA DO PIAUÍ',
        'ISAÍAS COELHO', 'ITAINÓPOLIS', 'ITAUEIRA', 'JACOBINA DO PIAUÍ', 'JAICÓS',
        'JARDIM DO MULATO', 'JATOBÁ DO PIAUÍ', 'JERUMENHA', 'JOÃO COSTA', 'JOAQUIM PIRES',
        'JOCA MARQUES', 'JOSÉ DE FREITAS', 'JUAZEIRO DO PIAUÍ', 'JÚLIO BORGES', 'JUREMA',
        'LAGOINHA DO PIAUÍ', 'LAGOA ALEGRE', 'LAGOA DE SÃO FRANCISCO', 'LAGOA DO BARRO DO PIAUÍ',
        'LAGOA DO PIAUÍ', 'LAGOA DO SÍTIO', 'LANDRI SALES', 'LUÍS CORREIA', 'LUZILÂNDIA',
        'MADEIRO', 'MANOEL EMÍDIO', 'MARCOLÂNDIA', 'MARCOS PARENTE', 'MASSAPÊ DO PIAUÍ',
        'MATIAS OLÍMPIO', 'MIGUEL ALVES', 'MIGUEL LEÃO', 'MILTON BRANDÃO', 'MONSENHOR GIL',
        'MONSENHOR HIPÓLITO', 'MONTE ALEGRE DO PIAUÍ', 'MORRO CABEÇA NO TEMPO', 'MORRO DO CHAPÉU DO PIAUÍ',
        'MURICI DOS PORTELAS', 'NAZARÉ DO PIAUÍ', 'NAZÁRIA', 'NOSSA SENHORA DE NAZARÉ',
        'NOSSA SENHORA DOS REMÉDIOS', 'NOVO ORIENTE DO PIAUÍ', 'NOVO SANTO ANTÔNIO', 'OEIRAS',
        'OLHO D\'ÁGUA DO PIAUÍ', 'PADRE MARCOS', 'PAES LANDIM', 'PAJEÚ DO PIAUÍ', 'PALMEIRA DO PIAUÍ',
        'PALMEIRAIS', 'PAQUETÁ', 'PARNAGUÁ', 'PARNAÍBA', 'PASSAGEM FRANCA DO PIAUÍ',
        'PATOS DO PIAUÍ', 'PAU D\'ARCO DO PIAUÍ', 'PAULISTANA', 'PAVUSSU', 'PEDRO II',
        'PEDRO LAURENTINO', 'PICOS', 'PIMENTEIRAS', 'PIO IX', 'PIRACURUCA', 'PIRIPIRI',
        'PORTO', 'PORTO ALEGRE DO PIAUÍ', 'PRATA DO PIAUÍ', 'QUEIMADA NOVA', 'QUIXELÔ',
        'REDENÇAO DO GURGUÉIA', 'REGENERAÇÃO', 'RIACHO FRIO', 'RIBEIRA DO PIAUÍ', 'RIBEIRO GONÇALVES',
        'RIO GRANDE DO PIAUÍ', 'SANTA CRUZ DO PIAUÍ', 'SANTA CRUZ DOS MILAGRES', 'SANTA FILOMENA',
        'SANTA LUZ', 'SANTA ROSA DO PIAUÍ', 'SANTANA DO PIAUÍ', 'SANTO ANTÔNIO DE LISBOA',
        'SANTO ANTÔNIO DOS MILAGRES', 'SANTO INÁCIO DO PIAUÍ', 'SÃO BRAZ DO PIAUÍ', 'SÃO FÉLIX DO PIAUÍ',
        'SÃO FRANCISCO DE ASSIS DO PIAUÍ', 'SÃO FRANCISCO DO PIAUÍ', 'SÃO GONÇALO DO GURGUÉIA',
        'SÃO GONÇALO DO PIAUÍ', 'SÃO JOÃO DA CANABRAVA', 'SÃO JOÃO DA FRONTEIRA', 'SÃO JOÃO DA SERRA',
        'SÃO JOÃO DA VARJOTA', 'SÃO JOÃO DO ARRAIAL', 'SÃO JOÃO DO PIAUÍ', 'SÃO JOSÉ DO DIVINO',
        'SÃO JOSÉ DO PEIXE', 'SÃO JOSÉ DO PIAUÍ', 'SÃO JULIÃO', 'SÃO LOURENÇO DO PIAUÍ',
        'SÃO LUÍS DO PIAUÍ', 'SÃO MIGUEL DA BAIXA GRANDE', 'SÃO MIGUEL DO FIDALGO', 'SÃO MIGUEL DO TAPUIO',
        'SÃO PEDRO DO PIAUÍ', 'SÃO RAIMUNDO NONATO', 'SEBASTIÃO BARROS', 'SEBASTIÃO LEAL',
        'SIGEFREDO PACHECO', 'SIMÕES', 'SIMPLÍCIO MENDES', 'SOCORRO DO PIAUÍ', 'SUSSUAPARA',
        'TAMBORIL DO PIAUÍ', 'TANQUE DO PIAUÍ', 'TERESINA', 'UNIÃO', 'URUÇUÍ',
        'VALENÇA DO PIAUÍ', 'VÁRZEA BRANCA', 'VÁRZEA GRANDE', 'VERA MENDES', 'VILA NOVA DO PIAUÍ',
        'WALL FERRAZ'
    ]
    
    print(f"✅ Lista carregada: {len(municipios_piaui)} municípios do Piauí")
    return sorted(municipios_piaui)

def corrigir_representante_piaui():
    """Corrige o representante 54.01 para atender todo o Piauí"""
    print("=== CORREÇÃO DO REPRESENTANTE 54.01 (FERNANDO MURILO) ===")
    print("Atualizando para atender TODOS os municípios do Piauí...")
    
    try:
        # Obter lista completa de municípios
        municipios_piaui = obter_municipios_piaui()
        
        if not municipios_piaui:
            print("❌ Erro: Não foi possível obter a lista de municípios")
            return False
        
        # Carregar dados atuais
        json_path = Path('old/representantes.json')
        
        if not json_path.exists():
            print(f"❌ Arquivo JSON não encontrado: {json_path}")
            return False
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Encontrar o representante 54.01
        representantes = data.get('representantes', {})
        fernando_key = None
        
        for nome_chave, dados in representantes.items():
            if dados.get('codigo') == '54.01':
                fernando_key = nome_chave
                break
        
        if not fernando_key:
            print("❌ Representante 54.01 (FERNANDO MURILO) não encontrado")
            return False
        
        # Dados atuais
        fernando_data = representantes[fernando_key]
        cidades_atuais = fernando_data.get('cidades', [])
        
        print(f"\n📊 SITUAÇÃO ATUAL:")
        print(f"   Representante: {fernando_data.get('nome', 'N/A')}")
        print(f"   Código: {fernando_data.get('codigo', 'N/A')}")
        print(f"   Cidades atuais: {len(cidades_atuais)}")
        print(f"   Estados: {fernando_data.get('estados', [])}")
        
        # Atualizar com todos os municípios do Piauí
        fernando_data.update({
            'cidades': municipios_piaui,
            'total_cidades': len(municipios_piaui),
            'estados': ['PI   '],
            'estados_atendidos': ['PI   '],
            'observacoes': 'Corrigido para atender TODOS os 224 municípios do Piauí'
        })
        
        # Atualizar metadados
        if 'metadados' not in data:
            data['metadados'] = {}
        
        data['metadados'].update({
            'data_correcao_piaui_54_01': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'observacoes_correcao_piaui': f'Representante 54.01 corrigido para atender todos os {len(municipios_piaui)} municípios do Piauí'
        })
        
        # Salvar arquivo atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ CORREÇÃO CONCLUÍDA:")
        print(f"   Municípios anteriores: {len(cidades_atuais)}")
        print(f"   Municípios atualizados: {len(municipios_piaui)}")
        print(f"   Diferença: +{len(municipios_piaui) - len(cidades_atuais)} municípios")
        print(f"   Arquivo salvo: {json_path}")
        
        # Mostrar alguns municípios adicionados
        novos_municipios = set(municipios_piaui) - set([cidade.upper() for cidade in cidades_atuais])
        if novos_municipios:
            print(f"\n📍 Exemplos de municípios adicionados:")
            for i, municipio in enumerate(sorted(novos_municipios)[:10]):
                print(f"   • {municipio}")
            if len(novos_municipios) > 10:
                print(f"   ... e mais {len(novos_municipios) - 10} municípios")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a correção: {e}")
        return False

if __name__ == '__main__':
    sucesso = corrigir_representante_piaui()
    
    if sucesso:
        print("\n🎉 Representante 54.01 agora atende TODO o estado do Piauí!")
    else:
        print("\n💥 Falha na correção. Verifique os erros acima.")