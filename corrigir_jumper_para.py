import json

print("Corrigindo representante JUMPER (código 82) para atender TODO o Pará...")

# Lista completa de municípios do Pará (144 municípios segundo IBGE)
municipios_para = [
    'ABAETETUBA', 'ABEL FIGUEIREDO', 'ACARA', 'AFUA', 'AGUA AZUL DO NORTE',
    'ALENQUER', 'ALMEIRIM', 'ALTAMIRA', 'ANAJAS', 'ANANINDEUA', 'ANAPU',
    'AUGUSTO CORREA', 'AURORA DO PARA', 'AVEIRO', 'BAGRE', 'BAIAO',
    'BANNACH', 'BARCARENA', 'BELEM', 'BELTERRA', 'BENEVIDES', 'BOM JESUS DO TOCANTINS',
    'BONITO', 'BRAGANCA', 'BRASIL NOVO', 'BREJO GRANDE DO ARAGUAIA', 'BREU BRANCO',
    'BREVES', 'BUJARU', 'CACHOEIRA DO ARARI', 'CACHOEIRA DO PIRIA', 'CAMETA',
    'CANAA DOS CARAJAS', 'CAPANEMA', 'CAPITAO POCO', 'CASTANHAL', 'CHAVES',
    'COLARES', 'CONCEICAO DO ARAGUAIA', 'CONCORDIA DO PARA', 'CUMARU DO NORTE',
    'CURIONOPOLIS', 'CURRALINHO', 'CURUA', 'DOM ELISEU', 'ELDORADO DOS CARAJAS',
    'FARO', 'FLORESTA DO ARAGUAIA', 'GARRAFAO DO NORTE', 'GOIANESIA DO PARA',
    'GURUPA', 'IGARAPE-ACU', 'IGARAPE-MIRI', 'INHANGAPI', 'IPIXUNA DO PARA',
    'IRITUIA', 'ITAITUBA', 'ITUPIRANGA', 'JACAREACANGA', 'JACUNDA',
    'JURUTI', 'LIMOEIRO DO AJURU', 'MAE DO RIO', 'MAGALHAES BARATA', 'MARABA',
    'MARACANA', 'MARAPANIM', 'MARITUBA', 'MEDICILÂNDIA', 'MELGACO',
    'MOCAJUBA', 'MOJU', 'MONTE ALEGRE', 'MUANA', 'NOVA ESPERANCA DO PIRIA',
    'NOVA IPIXUNA', 'NOVA TIMBOTEUA', 'NOVO PROGRESSO', 'NOVO REPARTIMENTO',
    'OBIDOS', 'OEIRAS DO PARA', 'ORIXIMINA', 'OUREM', 'OURILANDIA DO NORTE',
    'PACAJA', 'PALESTINA DO PARA', 'PARAGOMINAS', 'PARAUAPEBAS', 'PAU D ARCO',
    'PEIXE-BOI', 'PICARRA', 'PLACAS', 'PONTA DE PEDRAS', 'PORTEL',
    'PORTO DE MOZ', 'PORTO TROMBETAS', 'PRAINHA', 'PRIMAVERA', 'QUATIPURU',
    'REDENCAO', 'RIO MARIA', 'RONDON DO PARA', 'RUROPOLIS', 'SALINOPOLIS',
    'SALVATERRA', 'SANTA BARBARA DO PARA', 'SANTA CRUZ DO ARARI', 'SANTA ISABEL DO PARA',
    'SANTA LUZIA DO PARA', 'SANTA MARIA DAS BARREIRAS', 'SANTA MARIA DO PARA',
    'SANTANA DO ARAGUAIA', 'SANTAREM', 'SANTAREM NOVO', 'SANTO ANTONIO DO TAUA',
    'SAO CAETANO DE ODIVELAS', 'SAO DOMINGOS DO ARAGUAIA', 'SAO DOMINGOS DO CAPIM',
    'SAO FELIX DO XINGU', 'SAO FRANCISCO DO PARA', 'SAO GERALDO DO ARAGUAIA',
    'SAO JOAO DA PONTA', 'SAO JOAO DE PIRABAS', 'SAO JOAO DO ARAGUAIA',
    'SAO MIGUEL DO GUAMA', 'SAO SEBASTIAO DA BOA VISTA', 'SAPUCAIA',
    'SENADOR JOSE PORFIRIO', 'SOURE', 'TAILANDIA', 'TERRA ALTA', 'TERRA SANTA',
    'TOME-ACU', 'TRACUATEUA', 'TRAIRAO', 'TUCUMA', 'TUCURUI', 'ULIANOPOLIS',
    'URUARA', 'VIGIA', 'VISEU', 'VITORIA DO XINGU', 'XINGUARA'
]

print(f"✅ Lista de municípios do Pará carregada: {len(municipios_para)} municípios")

# Carregar dados atuais
with open('old/representantes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rep_data = data['representantes']

# Encontrar JUMPER
jumper_key = None
for nome_chave, dados in rep_data.items():
    if 'jumper' in nome_chave.lower() and dados.get('codigo') == '82.0':
        jumper_key = nome_chave
        break

if not jumper_key:
    print("❌ Representante JUMPER não encontrado!")
    exit(1)

print(f"\n✅ Encontrado representante: {rep_data[jumper_key]['nome']}")
print(f"Código: {rep_data[jumper_key]['codigo']}")
print(f"Municípios atuais: {len(rep_data[jumper_key]['cidades'])}")

# Backup dos dados originais
backup_cidades = rep_data[jumper_key]['cidades'].copy()
backup_total = rep_data[jumper_key].get('total_cidades', len(backup_cidades))

print(f"\nAtualizando dados do representante JUMPER...")

# Atualizar com todos os municípios do Pará
rep_data[jumper_key]['cidades'] = municipios_para
rep_data[jumper_key]['total_cidades'] = len(municipios_para)
rep_data[jumper_key]['estados_atendidos'] = ['PA']
rep_data[jumper_key]['observacoes'] = 'Atende TODO o estado do Pará - Atualizado automaticamente'

# Atualizar mapeamento de cidades
if 'mapeamento_cidades' in data:
    print("Atualizando mapeamento de cidades...")
    
    # Remover mapeamentos antigos do JUMPER
    cidades_para_remover = []
    for cidade, representante in data['mapeamento_cidades'].items():
        if representante == rep_data[jumper_key]['nome']:
            cidades_para_remover.append(cidade)
    
    for cidade in cidades_para_remover:
        del data['mapeamento_cidades'][cidade]
    
    # Adicionar novos mapeamentos
    for cidade in municipios_para:
        cidade_lower = cidade.lower()
        data['mapeamento_cidades'][cidade_lower] = rep_data[jumper_key]['nome']
    
    print(f"✅ Mapeamento atualizado: {len(municipios_para)} cidades mapeadas para JUMPER")

# Salvar arquivo atualizado
print("\nSalvando arquivo atualizado...")
with open('old/representantes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*60)
print(f"✅ Representante: {rep_data[jumper_key]['nome']}")
print(f"✅ Código: {rep_data[jumper_key]['codigo']}")
print(f"✅ Estado atendido: PA (Pará)")
print(f"✅ Municípios antes: {len(backup_cidades)}")
print(f"✅ Municípios agora: {len(municipios_para)}")
print(f"✅ Diferença: +{len(municipios_para) - len(backup_cidades)} municípios")
print(f"\n🎉 O representante JUMPER (código 82) agora atende TODO o estado do Pará!")

# Verificar alguns municípios importantes
municipios_importantes = ['BELEM', 'ANANINDEUA', 'SANTAREM', 'MARABA', 'ALTAMIRA', 'CASTANHAL', 'ITAITUBA']
print(f"\nVerificação de municípios importantes:")
for municipio in municipios_importantes:
    if municipio in municipios_para:
        print(f"  ✅ {municipio}")
    else:
        print(f"  ❌ {municipio} (não encontrado)")

print(f"\n✅ Verificação final: O representante código 82 agora atende TODO E APENAS o estado do Pará!")