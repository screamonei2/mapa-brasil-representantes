import json

# Lista de cidades da 3L (com duplicatas)
cidades_3l = [
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "CHAVANTES", "GARCA", "GARCA", "JAU", "JAU", "JAU", "JUNQUEIROPOLIS", "LINS", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO",
    "MIRANTE DO PARANAPANEMA", "ORIENTE", "OURINHOS", "OURINHOS", "OURINHOS", "OURINHOS", "OURINHOS",
    "PEDRINHAS PAULISTA", "POMPEIA", "PRATANIA", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "TAQUARITUBA", "ADAMANTINA", "AGUDOS", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "AREIOPOLIS", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "CANDIDO MOTA",
    "CANDIDO MOTA", "HERCULANDIA", "IACRI", "ITAPUI", "JAU", "JAU", "LINS", "LINS", "LINS",
    "LINS", "LUCELIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MINEIROS DO TIETE", "PIRAJUI",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "RANCHARIA", "TUPA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ASSIS", "ASSIS", "AVAI", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "ITATINGA", "JAU", "LENCOIS PAULISTA", "LENCOIS PAULISTA", "LENCOIS PAULISTA", "LINS",
    "LINS", "LINS", "LINS", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "OURINHOS",
    "OURINHOS", "PARAPUA", "PIRAJU", "PIRAPOZINHO", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "TUPA", "TUPA", "ADAMANTINA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ASSIS", "ASSIS", "ASSIS", "BARIRI",
    "BASTOS", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BORACEIA", "CAFELANDIA", "GAVIAO PEIXOTO", "ITATINGA", "JAU",
    "LENCOIS PAULISTA", "LINS", "LINS", "LINS", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO",
    "OURINHOS", "OURINHOS", "OURINHOS", "OURINHOS", "OURINHOS", "PARAGUACU PAULISTA",
    "PEDERNEIRAS", "PIRAJUI", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "REGENTE FEIJO", "TUPA", "TUPA", "TUPA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "AREALVA", "ASSIS", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BOCAINA",
    "CHAVANTES", "ITAPUI", "JAU", "JAU", "JAU", "JAU", "JAU", "LINS", "MACATUBA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MATAO", "MATAO",
    "MATAO", "MATAO", "OSVALDO CRUZ", "OURINHOS", "OURINHOS", "POMPEIA", "PRESIDENTE EPITACIO",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "RINOPOLIS", "TUPA", "TUPA", "ALVARES MACHADO", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ASSIS",
    "ASSIS", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "DRACENA",
    "JAU", "JAU", "JAU", "LINS", "LINS", "LINS", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO", "MATAO",
    "OURINHOS", "PACAEMBU", "PALMITAL", "PARANAPANEMA", "PEDERNEIRAS", "PINHALZINHO",
    "POMPEIA", "POMPEIA", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "TARUMA", "TUPA", "TUPA", "TUPA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ASSIS", "ASSIS", "ASSIS", "BAURU", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ARARAQUARA",
    "ARARAQUARA", "ARARAQUARA", "ARARAQUARA", "ASSIS", "ASSIS", "BARIRI", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "GUATAPARA", "INUBIA PAULISTA", "JAU", "JAU", "JAU", "JAU", "JAU", "JAU", "LINS", "LINS",
    "LINS", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU", "BAURU",
    "BAURU", "BAURU", "BOCAINA", "CAFELANDIA", "CONCHAS", "GARCA", "GUARANTA", "GUARANTA",
    "IACANGA", "IGARACU DO TIETE", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MATAO", "OURINHOS", "OURINHOS", "OURINHOS", "OURINHOS",
    "OURINHOS", "PARAGUACU PAULISTA", "PARAGUACU PAULISTA", "POMPEIA", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PROMISSAO", "QUATA", "RIBEIRAO DOS INDIOS", "JAU", "JAU", "JAU",
    "JUNQUEIROPOLIS", "LINS", "LINS", "LINS", "LINS", "LINS", "MARILIA", "MARILIA", "MARILIA",
    "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MARILIA", "MATAO", "MATAO",
    "MATAO", "MATAO", "PEDERNEIRAS", "PEDERNEIRAS", "PEREIRAS", "PIRAJUI", "PIRATININGA",
    "TARUMA", "TUPA", "TUPA", "TUPA", "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE",
    "PRESIDENTE PRUDENTE", "PRESIDENTE PRUDENTE", "PRESIDENTE VENCESLAU", "QUEIROZ", "QUINTANA",
    "TUPA", "TUPA"
]

# Remover duplicatas e ordenar
cidades_unicas = sorted(list(set(cidades_3l)))

print(f"Total de cidades únicas: {len(cidades_unicas)}")
print("Cidades únicas:")
for cidade in cidades_unicas:
    print(f"  - {cidade}")

# Organizar em regiões lógicas
regioes = {
    "bauru": {
        "nome": "Região de Bauru",
        "cidades": []
    },
    "araraquara": {
        "nome": "Região de Araraquara",
        "cidades": []
    },
    "marilia": {
        "nome": "Região de Marília",
        "cidades": []
    },
    "presidente_prudente": {
        "nome": "Região de Presidente Prudente",
        "cidades": []
    },
    "outras": {
        "nome": "Outras Regiões",
        "cidades": []
    }
}

# Distribuir cidades por região
for cidade in cidades_unicas:
    if cidade in ["BAURU", "LENCOIS PAULISTA", "AGUDOS", "PIRAJU", "PIRAJUI", "PIRAPOZINHO", 
                   "PIRATININGA", "PROMISSAO", "QUADRA", "QUATA", "QUEIROZ", "QUINTANA", 
                   "RANCHARIA", "REGENTE FEIJO", "RIBEIRAO DOS INDIOS", "RINCAO", "RINOPOLIS", 
                   "SABINO", "BOCAINA", "CAFELANDIA", "CONCHAS", "GARCA", "GUARANTA", 
                   "IACANGA", "IGARACU DO TIETE", "MACATUBA", "PEDERNEIRAS", "PEREIRAS", 
                   "PIRAJUI", "PIRATININGA", "TARUMA", "CANDIDO MOTA", "HERCULANDIA", 
                   "IACRI", "ITAPUI", "LUCELIA", "MINEIROS DO TIETE", "PIRAJUI", 
                   "BARIRI", "BASTOS", "BORACEIA", "GAVIAO PEIXOTO", "ITATINGA", 
                   "GUATAPARA", "INUBIA PAULISTA", "OSVALDO CRUZ", "PACAEMBU", 
                   "PALMITAL", "PARANAPANEMA", "PINHALZINHO", "POMPEIA", "PRATANIA", 
                   "TARUMA", "ALVARES MACHADO", "DRACENA", "PEDERNEIRAS", "PEREIRAS", 
                   "PIRAJUI", "PIRATININGA", "TARUMA"]:
        regioes["bauru"]["cidades"].append(cidade)
    elif cidade in ["ARARAQUARA", "AREALVA", "ASSIS", "AVAI", "AREIOPOLIS"]:
        regioes["araraquara"]["cidades"].append(cidade)
    elif cidade in ["MARILIA", "MATAO", "JAU", "LINS", "OURINHOS", "TUPA"]:
        regioes["marilia"]["cidades"].append(cidade)
    elif cidade in ["PRESIDENTE PRUDENTE", "PRESIDENTE EPITACIO", "PRESIDENTE VENCESLAU", 
                    "MIRANTE DO PARANAPANEMA", "ORIENTE", "PEDRINHAS PAULISTA", 
                    "PARAPUA", "PARAGUACU PAULISTA"]:
        regioes["presidente_prudente"]["cidades"].append(cidade)
    else:
        regioes["outras"]["cidades"].append(cidade)

# Criar estrutura JSON da 3L
estrutura_3l = {
    "representantes": {
        "3l representacoes comerciais ltda me": {
            "codigo": "30.0",
            "nome": "3L REPRESENTACOES COMERCIAIS LTDA ME",
            "contato": {
                "nome_contato": "Cristian",
                "email": "vendasgentil@hotmail.com",
                "celular": "14-99712-4471"
            },
            "observacoes": "Será enviado para pesquisa no mapa",
            "total_cidades": len(cidades_unicas),
            "estados_atendidos": ["SP"],
            "resumo_atividades": "",
            "performance": {},
            "estados": {
                "SP": {
                    "regioes": regioes
                }
            }
        }
    }
}

# Salvar arquivo JSON
with open("3l_nova_estrutura.json", "w", encoding="utf-8") as f:
    json.dump(estrutura_3l, f, indent=2, ensure_ascii=False)

print(f"\nArquivo '3l_nova_estrutura.json' criado com sucesso!")
print(f"Total de cidades únicas: {len(cidades_unicas)}")

# Mostrar distribuição por região
for regiao_key, regiao_data in regioes.items():
    print(f"\n{regiao_data['nome']}: {len(regiao_data['cidades'])} cidades")
    for cidade in sorted(regiao_data['cidades']):
        print(f"  - {cidade}") 