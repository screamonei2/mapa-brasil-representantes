#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o representante 43.0 (ROD LON REPRESENTAÇÕES LTDA)
para atender TODOS os 184 municípios do estado do Ceará
"""

import json
import time
from pathlib import Path

def obter_municipios_ceara():
    """Retorna todos os 184 municípios do Ceará"""
    print("Carregando lista completa dos municípios do Ceará...")
    
    # Lista completa dos 184 municípios do Ceará
    municipios_ceara = [
        'ABAIARA', 'ACARAPE', 'ACARAÚ', 'ACOPIARA', 'AIUABA', 'ALCÂNTARAS', 'ALTANEIRA',
        'ALTO SANTO', 'AMONTADA', 'ANTONINA DO NORTE', 'APUIARÉS', 'AQUIRAZ', 'ARACATI',
        'ARACOIABA', 'ARARENDÁ', 'ARARIPE', 'ARATUBA', 'ARNEIROZ', 'ASSARÉ', 'AURORA',
        'BAIXIO', 'BANABUIÚ', 'BARBALHA', 'BARREIRA', 'BARRO', 'BARROQUINHA', 'BATURITÉ',
        'BEBERIBE', 'BELA CRUZ', 'BOA VIAGEM', 'BREJO SANTO', 'CAMOCIM', 'CAMPOS SALES',
        'CANINDÉ', 'CAPISTRANO', 'CARIDADE', 'CARIRÉ', 'CARIRIAÇU', 'CARIÚS', 'CARNAUBAL',
        'CASCAVEL', 'CATARINA', 'CATUNDA', 'CAUCAIA', 'CEDRO', 'CHAVAL', 'CHORÓ',
        'CHOROZINHO', 'COREAÚ', 'CRATEÚS', 'CRATO', 'CROATÁ', 'CRUZ', 'DEPUTADO IRAPUAN PINHEIRO',
        'ERERÊ', 'EUSÉBIO', 'FARIAS BRITO', 'FORQUILHA', 'FORTALEZA', 'FORTIM', 'FRECHEIRINHA',
        'GENERAL SAMPAIO', 'GRAÇA', 'GRANJA', 'GRANJEIRO', 'GROAÍRAS', 'GUAIÚBA', 'GUARACIABA DO NORTE',
        'GUARAMIRANGA', 'HIDROLÂNDIA', 'HORIZONTE', 'IBARETAMA', 'IBIAPINA', 'IBICUITINGA',
        'ICAPUÍ', 'ICÓ', 'IGUATU', 'INDEPENDÊNCIA', 'IPAPORANGA', 'IPAUMIRIM', 'IPU',
        'IPUEIRAS', 'IRACEMA', 'IRAUÇUBA', 'ITAIÇABA', 'ITAITINGA', 'ITAPAJÉ', 'ITAPIPOCA',
        'ITAPIÚNA', 'ITAREMA', 'ITATIRA', 'JAGUARETAMA', 'JAGUARIBARA', 'JAGUARIBE', 'JAGUARUANA',
        'JARDIM', 'JATI', 'JIJOCA DE JERICOACOARA', 'JUAZEIRO DO NORTE', 'JUCÁS', 'LAVRAS DA MANGABEIRA',
        'LIMOEIRO DO NORTE', 'MADALENA', 'MARACANAÚ', 'MARANGUAPE', 'MARCO', 'MARTINÓPOLE',
        'MASSAPÊ', 'MAURITI', 'MERUOCA', 'MILAGRES', 'MILHÃ', 'MIRAÍMA', 'MISSÃO VELHA',
        'MOMBAÇA', 'MONSENHOR TABOSA', 'MORADA NOVA', 'MORAÚJO', 'MORRINHOS', 'MUCAMBO',
        'MULUNGU', 'NOVA OLINDA', 'NOVA RUSSAS', 'NOVO ORIENTE', 'OCARA', 'ORÓS',
        'PACAJUS', 'PACATUBA', 'PACOTI', 'PACUJÁ', 'PALHANO', 'PALMÁCIA', 'PARACURU',
        'PARAIPABA', 'PARAMBU', 'PARAMOTI', 'PEDRA BRANCA', 'PENAFORTE', 'PENTECOSTE',
        'PEREIRO', 'PINDORETAMA', 'PIQUET CARNEIRO', 'PIRES FERREIRA', 'PORANGA', 'PORTEIRAS',
        'POTENGI', 'POTIRETAMA', 'QUITERIANÓPOLIS', 'QUIXADÁ', 'QUIXELÔ', 'QUIXERAMOBIM',
        'QUIXERÉ', 'REDENÇÃO', 'RERIUTABA', 'RUSSAS', 'SABOEIRO', 'SALITRE', 'SANTA QUITÉRIA',
        'SANTANA DO ACARAÚ', 'SANTANA DO CARIRI', 'SÃO BENEDITO', 'SÃO GONÇALO DO AMARANTE',
        'SÃO JOÃO DO JAGUARIBE', 'SÃO LUÍS DO CURU', 'SENADOR POMPEU', 'SENADOR SÁ',
        'SOBRAL', 'SOLONÓPOLE', 'TABULEIRO DO NORTE', 'TAMBORIL', 'TARRAFAS', 'TAUÁ',
        'TEJUÇUOCA', 'TIANGUÁ', 'TRAIRI', 'TURURU', 'UBAJARA', 'UMARI', 'UMIRIM',
        'URUBURETAMA', 'URUOCA', 'VARJOTA', 'VÁRZEA ALEGRE', 'VIÇOSA DO CEARÁ'
    ]
    
    print(f"✅ Lista carregada: {len(municipios_ceara)} municípios do Ceará")
    return sorted(municipios_ceara)

def corrigir_representante_ceara():
    """Corrige o representante 43.0 para atender todo o Ceará"""
    print("=== CORREÇÃO DO REPRESENTANTE 43.0 (ROD LON REPRESENTAÇÕES LTDA) ===")
    print("Atualizando para atender TODOS os municípios do Ceará...")
    
    try:
        # Obter lista completa de municípios
        municipios_ceara = obter_municipios_ceara()
        
        if not municipios_ceara:
            print("❌ Erro: Não foi possível obter a lista de municípios")
            return False
        
        # Carregar dados atuais
        json_path = Path('old/representantes.json')
        
        if not json_path.exists():
            print(f"❌ Arquivo JSON não encontrado: {json_path}")
            return False
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Encontrar o representante 43.0
        representantes = data.get('representantes', {})
        rod_lon_key = None
        
        for nome_chave, dados in representantes.items():
            if dados.get('codigo') == '43.0':
                rod_lon_key = nome_chave
                break
        
        if not rod_lon_key:
            print("❌ Representante 43.0 (ROD LON REPRESENTAÇÕES LTDA) não encontrado")
            return False
        
        # Dados atuais
        rod_lon_data = representantes[rod_lon_key]
        cidades_atuais = rod_lon_data.get('cidades', [])
        
        print(f"\n📊 SITUAÇÃO ATUAL:")
        print(f"   Representante: {rod_lon_data.get('nome', 'N/A')}")
        print(f"   Código: {rod_lon_data.get('codigo', 'N/A')}")
        print(f"   Cidades atuais: {len(cidades_atuais)}")
        print(f"   Estados: {rod_lon_data.get('estados', [])}")
        
        # Atualizar com todos os municípios do Ceará
        rod_lon_data.update({
            'cidades': municipios_ceara,
            'total_cidades': len(municipios_ceara),
            'estados': ['CE   '],
            'estados_atendidos': ['CE   '],
            'observacoes': 'Corrigido para atender TODOS os 184 municípios do Ceará'
        })
        
        # Atualizar metadados
        if 'metadados' not in data:
            data['metadados'] = {}
        
        data['metadados'].update({
            'data_correcao_ceara_43_0': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'observacoes_correcao_ceara': f'Representante 43.0 corrigido para atender todos os {len(municipios_ceara)} municípios do Ceará'
        })
        
        # Salvar arquivo atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ CORREÇÃO CONCLUÍDA:")
        print(f"   Municípios anteriores: {len(cidades_atuais)}")
        print(f"   Municípios atualizados: {len(municipios_ceara)}")
        print(f"   Diferença: +{len(municipios_ceara) - len(cidades_atuais)} municípios")
        print(f"   Arquivo salvo: {json_path}")
        
        # Mostrar alguns municípios adicionados
        novos_municipios = set(municipios_ceara) - set([cidade.upper() for cidade in cidades_atuais])
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
    sucesso = corrigir_representante_ceara()
    
    if sucesso:
        print("\n🎉 Representante 43.0 agora atende TODO o estado do Ceará!")
    else:
        print("\n💥 Falha na correção. Verifique os erros acima.")