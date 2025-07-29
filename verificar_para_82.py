import json

# Carregar dados dos representantes
print("Procurando representante código 82 ou JUMPER...")
with open('old/representantes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Acessar a seção de representantes
rep_data = data.get('representantes', {})
print(f"Total de representantes no arquivo: {len(rep_data)}")

# Procurar por código 82 ou nome JUMPER
representantes_encontrados = []

for nome_chave, dados in rep_data.items():
    # Verificar se é código 82
    if dados.get('codigo') == '82.0' or dados.get('codigo') == '82':
        representantes_encontrados.append((nome_chave, dados, 'código 82'))
    
    # Verificar se contém JUMPER no nome
    if 'jumper' in nome_chave.lower() or 'jumper' in dados.get('nome', '').lower():
        representantes_encontrados.append((nome_chave, dados, 'nome JUMPER'))

print(f"\nRepresentantes encontrados: {len(representantes_encontrados)}")

for i, (nome_chave, dados, criterio) in enumerate(representantes_encontrados):
    print(f"\n{'='*60}")
    print(f"REPRESENTANTE {i+1} (encontrado por {criterio}):")
    print(f"{'='*60}")
    print(f"Chave no JSON: {nome_chave}")
    print(f"Nome: {dados.get('nome', 'N/A')}")
    print(f"Código: {dados.get('codigo', 'N/A')}")
    print(f"Estados: {dados.get('estados', dados.get('estados_atendidos', 'N/A'))}")
    print(f"Total de cidades: {len(dados.get('cidades', []))}")
    
    if dados.get('cidades'):
        print(f"Primeiras 10 cidades: {dados['cidades'][:10]}")
    
    # Verificar se atende apenas o Pará
    estados = dados.get('estados', dados.get('estados_atendidos', []))
    if isinstance(estados, list):
        estados_limpos = [estado.strip() for estado in estados]
        if len(estados_limpos) == 1 and estados_limpos[0] == 'PA':
            print("✅ Atende apenas o estado do Pará")
            atende_apenas_para = True
        else:
            print(f"❌ Estados atendidos: {estados_limpos}")
            atende_apenas_para = False
    
    # Verificar quantidade de municípios
    total_cidades = len(dados.get('cidades', []))
    if total_cidades >= 140:
        print(f"✅ Quantidade adequada de municípios ({total_cidades}) para cobrir todo o Pará")
        quantidade_adequada = True
    elif total_cidades >= 40:
        print(f"⚠️  Quantidade moderada de municípios ({total_cidades})")
        quantidade_adequada = False
    else:
        print(f"❌ Poucos municípios ({total_cidades})")
        quantidade_adequada = False
    
    # Verificar se há municípios típicos do Pará
    if dados.get('cidades'):
        municipios_tipicos_para = ['BELEM', 'ANANINDEUA', 'SANTAREM', 'MARABA', 'CASTANHAL', 'ALTAMIRA', 'ITAITUBA']
        municipios_encontrados = []
        cidades_upper = [cidade.upper() for cidade in dados['cidades']]
        
        for municipio in municipios_tipicos_para:
            if municipio in cidades_upper:
                municipios_encontrados.append(municipio)
        
        print(f"\nMunicípios típicos do Pará encontrados: {len(municipios_encontrados)}/{len(municipios_tipicos_para)}")
        for municipio in municipios_encontrados:
            print(f"  ✅ {municipio}")
        
        # Conclusão
        print(f"\n{'='*50}")
        print("CONCLUSÃO:")
        print(f"{'='*50}")
        
        if atende_apenas_para and quantidade_adequada and len(municipios_encontrados) >= 5:
            print("🎉 O representante ATENDE TODO E APENAS o estado do Pará!")
        elif atende_apenas_para and len(municipios_encontrados) >= 5:
            print("✅ O representante atende apenas o Pará, mas pode não cobrir todos os municípios")
        else:
            print("⚠️  O representante pode NÃO atender todo e apenas o estado do Pará")
            if not atende_apenas_para:
                print("   - Não atende apenas o Pará")
            if len(municipios_encontrados) < 5:
                print("   - Poucos municípios típicos do Pará encontrados")

if not representantes_encontrados:
    print("\n❌ Nenhum representante encontrado com código 82 ou nome JUMPER")
    print("\nVamos procurar por códigos próximos a 82:")
    
    # Procurar códigos próximos
    codigos_proximos = []
    for nome_chave, dados in rep_data.items():
        codigo = dados.get('codigo', '')
        if codigo and ('8' in codigo or 'PA' in str(dados.get('estados', []))):
            codigos_proximos.append((nome_chave, dados))
    
    print(f"\nEncontrados {len(codigos_proximos)} representantes com código contendo '8' ou atendendo PA:")
    for i, (nome_chave, dados) in enumerate(codigos_proximos[:10]):  # Mostrar apenas os primeiros 10
        print(f"\n{i+1}. {nome_chave}")
        print(f"   Código: {dados.get('codigo', 'N/A')}")
        print(f"   Nome: {dados.get('nome', 'N/A')}")
        print(f"   Estados: {dados.get('estados', 'N/A')}")
        print(f"   Total cidades: {len(dados.get('cidades', []))}")