# Script para corrigir representante Lugus - versão sem dependências externas
import json

def corrigir_lugus():
    print("=== CORREÇÃO DO REPRESENTANTE LUGUS (53.02) ===")
    
    # Lista completa dos 62 municípios do Amazonas (em maiúsculas)
    municipios_amazonas = [
        'ALVARÃES', 'AMATURÁ', 'ANAMÃ', 'ANORI', 'APUÍ', 'ATALAIA DO NORTE',
        'AUTAZES', 'BARCELOS', 'BARREIRINHA', 'BENJAMIN CONSTANT', 'BERURI',
        'BOA VISTA DO RAMOS', 'BOCA DO ACRE', 'BORBA', 'CAAPIRANGA', 'CANUTAMA',
        'CARAUARI', 'CAREIRO', 'CAREIRO DA VÁRZEA', 'COARI', 'CODAJÁS',
        'EIRUNEPÉ', 'ENVIRA', 'FONTE BOA', 'GUAJARÁ', 'HUMAITÁ', 'IPIXUNA',
        'IRANDUBA', 'ITACOATIARA', 'ITAMARATI', 'ITAPIRANGA', 'JAPURÁ',
        'JURUÁ', 'JUTAÍ', 'LÁBREA', 'MANACAPURU', 'MANAQUIRI', 'MANAUS',
        'MANICORÉ', 'MARAÃ', 'MAUÉS', 'NHAMUNDÁ', 'NOVA OLINDA DO NORTE',
        'NOVO AIRÃO', 'NOVO ARIPUANÃ', 'PARINTINS', 'PAUINI', 'PRESIDENTE FIGUEIREDO',
        'RIO PRETO DA EVA', 'SANTA ISABEL DO RIO NEGRO', 'SANTO ANTÔNIO DO IÇÁ',
        'SÃO GABRIEL DA CACHOEIRA', 'SÃO PAULO DE OLIVENÇA', 'SÃO SEBASTIÃO DO UATUMÃ',
        'SILVES', 'TABATINGA', 'TAPAUÁ', 'TEFÉ', 'TONANTINS', 'UARINI',
        'URUCARÁ', 'URUCURITUBA'
    ]
    
    try:
        # Ler arquivo atual
        with open('old/representantes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Encontrar e atualizar Lugus
        representantes = data['representantes']
        lugus_key = None
        
        for key, rep in representantes.items():
            if 'lugus' in key.lower() or rep.get('codigo') == '53.02':
                lugus_key = key
                break
        
        if lugus_key:
            print(f"✓ Encontrado representante: {representantes[lugus_key]['nome']}")
            print(f"  Código: {representantes[lugus_key]['codigo']}")
            print(f"  Cidades antes: {len(representantes[lugus_key].get('cidades', []))}")
            
            # Atualizar dados
            representantes[lugus_key]['cidades'] = municipios_amazonas
            representantes[lugus_key]['total_cidades'] = len(municipios_amazonas)
            representantes[lugus_key]['estados'] = ['AM']
            representantes[lugus_key]['estados_atendidos'] = ['AM']
            
            print(f"  Cidades depois: {len(municipios_amazonas)}")
            
            # Atualizar mapeamento
            mapeamento = data['mapeamento_cidades']
            
            # Remover mapeamentos antigos
            cidades_removidas = 0
            for cidade in list(mapeamento.keys()):
                if mapeamento[cidade] == 'LUGUS REPRESENTACAO LTDA':
                    del mapeamento[cidade]
                    cidades_removidas += 1
            
            # Adicionar novos mapeamentos
            for cidade in municipios_amazonas:
                mapeamento[cidade.lower()] = 'LUGUS REPRESENTACAO LTDA'
            
            print(f"✓ Removidos {cidades_removidas} mapeamentos antigos")
            print(f"✓ Adicionados {len(municipios_amazonas)} novos mapeamentos")
            
            # Salvar arquivo
            with open('old/representantes.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ LUGUS CORRIGIDO COM SUCESSO!")
            print(f"✓ Agora atende TODO o estado do Amazonas (AM)")
            print(f"✓ Total de municípios: {len(municipios_amazonas)}")
            print(f"✓ Estados: apenas AM")
            print(f"✓ Inclui cidades importantes: MANAUS, PARINTINS, ITACOATIARA, COARI, TABATINGA")
            
        else:
            print("❌ Representante Lugus não encontrado!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

corrigir_lugus()