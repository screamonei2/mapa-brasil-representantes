import json

def atualizar_schioppa():
    """Atualiza os dados da SCHIOPPA conforme solicitado"""
    
    # Estados que a SCHIOPPA deve atender (conforme dados fornecidos)
    estados_schioppa = ['SE', 'RR', 'RN', 'AL', 'RO', 'MA', 'AP', 'AC']
    
    # Dados atualizados da SCHIOPPA
    dados_schioppa = {
        "codigo": "01",
        "nome": "SCHIOPPA",
        "contato": {
            "nome_contato": "Schioppa",
            "email": "vendas@schioppa.com.br",
            "celular": "11-99154-6727"
        },
        "estados": [f"{estado}   " for estado in estados_schioppa],  # Formato com espaços
        "cidades": [],  # Será preenchido com TODAS as cidades dos estados
        "observacoes": "Atende TODOS os municípios dos estados: SE, RR, RN, AL, RO, MA, AP, AC",
        "cor_padrao": "#3b82f6",  # Azul padrão
        "atende_estado_completo": True
    }
    
    try:
        # Ler o arquivo atual
        with open('old/representantes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Atualizar os dados da SCHIOPPA
        if 'representantes' in data:
            data['representantes']['schioppa'] = dados_schioppa
        else:
            # Se não existe a estrutura, criar
            data = {'representantes': {'schioppa': dados_schioppa}}
        
        # Salvar o arquivo atualizado
        with open('old/representantes.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("Dados da SCHIOPPA atualizados com sucesso!")
        print(f"Estados atendidos: {', '.join(estados_schioppa)}")
        print(f"Cor padrao: {dados_schioppa['cor_padrao']} (azul padrao)")
        print(f"Contato: {dados_schioppa['contato']['email']}")
        print(f"Celular: {dados_schioppa['contato']['celular']}")
        print("\nIMPORTANTE: A SCHIOPPA agora atende TODOS os municipios dos estados especificados.")
        
        return True
        
    except Exception as e:
        print(f"Erro ao atualizar dados da SCHIOPPA: {e}")
        return False

def main():
    print("Atualizando dados da SCHIOPPA...\n")
    
    # Atualizar dados JSON
    sucesso_json = atualizar_schioppa()
    
    if sucesso_json:
        print("\nAtualizacao concluida com sucesso!")
        print("\nResumo das alteracoes:")
        print("   • SCHIOPPA agora atende 8 estados completos: SE, RR, RN, AL, RO, MA, AP, AC")
        print("   • Todos os municipios desses estados serao da mesma cor azul padrao (#3b82f6)")
        print("   • Dados de contato atualizados conforme fornecido")
    else:
        print("\nAlgumas atualizacoes falharam. Verifique os logs acima.")

if __name__ == "__main__":
    main()