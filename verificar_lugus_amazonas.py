# Script para verificar representante Lugus
# Análise baseada nos dados encontrados:

print("=== VERIFICAÇÃO DO REPRESENTANTE LUGUS (53.02) ===")
print()
print("DADOS ENCONTRADOS:")
print("- Código: 53.02")
print("- Nome: LUGUS REPRESENTACAO LTDA")
print("- Estados: ['AM   ']")
print("- Cidades: ['MANACAPURU', 'MANAUS', 'PARINTINS', 'PRESIDENTE FIGUEIREDO']")
print("- Total de cidades: 4")
print()
print("ANÁLISE:")
print("✓ Atende apenas o estado do Amazonas (AM)")
print("❌ Cobertura MUITO INSUFICIENTE: apenas 4 de 62 municípios (6.5%)")
print()
print("MUNICÍPIOS DO AMAZONAS (total: 62):")
municipios_am = [
    'Alvarães', 'Amaturá', 'Anamã', 'Anori', 'Apuí', 'Atalaia do Norte',
    'Autazes', 'Barcelos', 'Barreirinha', 'Benjamin Constant', 'Beruri',
    'Boa Vista do Ramos', 'Boca do Acre', 'Borba', 'Caapiranga', 'Canutama',
    'Carauari', 'Careiro', 'Careiro da Várzea', 'Coari', 'Codajás',
    'Eirunepé', 'Envira', 'Fonte Boa', 'Guajará', 'Humaitá', 'Ipixuna',
    'Iranduba', 'Itacoatiara', 'Itamarati', 'Itapiranga', 'Japurá',
    'Juruá', 'Jutaí', 'Lábrea', 'Manacapuru', 'Manaquiri', 'Manaus',
    'Manicoré', 'Maraã', 'Maués', 'Nhamundá', 'Nova Olinda do Norte',
    'Novo Airão', 'Novo Aripuanã', 'Parintins', 'Pauini', 'Presidente Figueiredo',
    'Rio Preto da Eva', 'Santa Isabel do Rio Negro', 'Santo Antônio do Içá',
    'São Gabriel da Cachoeira', 'São Paulo de Olivença', 'São Sebastião do Uatumã',
    'Silves', 'Tabatinga', 'Tapauá', 'Tefé', 'Tonantins', 'Uarini',
    'Urucará', 'Urucurituba'
]
print(f"Total de municípios no AM: {len(municipios_am)}")
print()
print("CONCLUSÃO:")
print("❌ LUGUS NÃO atende todo o estado do Amazonas")
print("❌ Atende apenas 4 municípios de 62 (6.5% de cobertura)")
print("⚠️ NECESSÁRIA CORREÇÃO: Adicionar todos os 62 municípios do Amazonas")
print()
print("AÇÃO RECOMENDADA:")
print("Atualizar o representante Lugus para incluir todos os 62 municípios do Amazonas")