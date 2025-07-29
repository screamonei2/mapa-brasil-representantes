import json

def corrigir_lugus_amazonas():
    print("=== CORREÇÃO DO REPRESENTANTE LUGUS (53.02) ===")
    print("Adicionando todos os 62 municípios do Amazonas...")
    
    # Lista completa dos 62 municípios do Amazonas
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
        # Carregar dados atuais
        with open('old/representantes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        representantes = data.get('representantes', {})
        
        # Encontrar e atualizar Lugus
        lugus_atualizado = False
        for nome, info in representantes.items():
            if 'lugus' in nome.lower() and info.get('codigo') == '53.02':
                print(f"\n✓ Atualizando representante: {info.get('nome')}")
                print(f"  Código: {info.get('codigo')}")
                print(f"  Cidades antes: {len(info.get('cidades', []))}")
                
                # Atualizar com todos os municípios do Amazonas
                info['cidades'] = municipios_amazonas
                info['total_cidades'] = len(municipios_amazonas)
                info['estados'] = ['AM']
                info['estados_atendidos'] = ['AM']
                
                print(f"  Cidades depois: {len(info['cidades'])}")
                print(f"  Estados: {info['estados']}")
                
                lugus_atualizado = True
                break
        
        if not lugus_atualizado:
            print("❌ Representante Lugus não encontrado para atualização!")
            return
        
        # Atualizar mapeamento de cidades
        mapeamento = data.get('mapeamento_cidades', {})
        
        # Remover mapeamentos antigos do Lugus
        cidades_removidas = 0
        for cidade, representante in list(mapeamento.items()):
            if representante == 'LUGUS REPRESENTACAO LTDA':
                del mapeamento[cidade]
                cidades_removidas += 1
        
        print(f"\n✓ Removidos {cidades_removidas} mapeamentos antigos")
        
        # Adicionar novos mapeamentos
        for cidade in municipios_amazonas:
            mapeamento[cidade.lower()] = 'LUGUS REPRESENTACAO LTDA'
        
        print(f"✓ Adicionados {len(municipios_amazonas)} novos mapeamentos")
        
        # Salvar arquivo atualizado
        with open('old/representantes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ CORREÇÃO CONCLUÍDA!")
        print(f"✓ Lugus agora atende TODO o estado do Amazonas")
        print(f"✓ Total de municípios: {len(municipios_amazonas)}")
        print(f"✓ Estados atendidos: apenas AM")
        print(f"✓ Mapeamento de cidades atualizado")
        
        # Verificar algumas cidades importantes
        cidades_importantes = ['MANAUS', 'PARINTINS', 'ITACOATIARA', 'COARI', 'TABATINGA']
        print(f"\n✓ Cidades importantes incluídas:")
        for cidade in cidades_importantes:
            if cidade in municipios_amazonas:
                print(f"  - {cidade}")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir: {e}")

if __name__ == "__main__":
    corrigir_lugus_amazonas()