#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reorganizar o JSON de representantes, fazendo com que as cidades sejam filhas dos estados.
Isso resolve o problema de cidades com nomes iguais em diferentes estados.
"""

import json
import os
from collections import defaultdict

def reorganizar_representantes():
    """Reorganiza o JSON de representantes para que as cidades sejam filhas dos estados."""
    
    # Caminho do arquivo original
    arquivo_original = "old/representantes.json"
    arquivo_novo = "old/representantes_por_estado.json"
    
    print("Carregando arquivo original...")
    with open(arquivo_original, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print("Reorganizando dados...")
    representantes_reorganizados = {}
    
    for codigo_representante, dados_representante in dados["representantes"].items():
        # Criar nova estrutura para o representante
        novo_representante = {
            "codigo": dados_representante["codigo"],
            "nome": dados_representante["nome"],
            "contato": dados_representante["contato"],
            "observacoes": dados_representante.get("observacoes", ""),
            "total_cidades": dados_representante.get("total_cidades", 0),
            "estados_atendidos": dados_representante.get("estados_atendidos", []),
            "resumo_atividades": dados_representante.get("resumo_atividades", ""),
            "performance": dados_representante.get("performance", {}),
            "estados": {}
        }
        
        # Organizar cidades por estado
        estados_cidades = defaultdict(list)
        
        # Se já existe estrutura de estados, usar ela
        if "estados" in dados_representante and isinstance(dados_representante["estados"], list):
            estados = dados_representante["estados"]
            cidades = dados_representante.get("cidades", [])
            
            # Se temos a mesma quantidade de estados e cidades, assumir que estão relacionados
            if len(estados) == 1 and len(cidades) > 0:
                # Um estado, múltiplas cidades
                estado = estados[0].strip()
                for cidade in cidades:
                    estados_cidades[estado].append(cidade.strip())
            else:
                # Múltiplos estados - distribuir cidades (assumindo que todas as cidades pertencem a todos os estados)
                for estado in estados:
                    estado_limpo = estado.strip()
                    for cidade in cidades:
                        estados_cidades[estado_limpo].append(cidade.strip())
        else:
            # Estrutura antiga - todas as cidades pertencem a todos os estados
            estados = dados_representante.get("estados_atendidos", [])
            cidades = dados_representante.get("cidades", [])
            
            for estado in estados:
                estado_limpo = estado.strip()
                for cidade in cidades:
                    estados_cidades[estado_limpo].append(cidade.strip())
        
        # Adicionar estados e suas cidades ao representante
        for estado, cidades_estado in estados_cidades.items():
            novo_representante["estados"][estado] = {
                "cidades": sorted(list(set(cidades_estado))),  # Remove duplicatas e ordena
                "total_cidades": len(set(cidades_estado))
            }
        
        representantes_reorganizados[codigo_representante] = novo_representante
    
    # Criar estrutura final
    dados_finais = {
        "representantes": representantes_reorganizados
    }
    
    print("Salvando arquivo reorganizado...")
    with open(arquivo_novo, 'w', encoding='utf-8') as f:
        json.dump(dados_finais, f, ensure_ascii=False, indent=2)
    
    print(f"Arquivo reorganizado salvo como: {arquivo_novo}")
    
    # Estatísticas
    total_representantes = len(representantes_reorganizados)
    total_estados = 0
    total_cidades = 0
    
    for representante in representantes_reorganizados.values():
        total_estados += len(representante["estados"])
        for estado_data in representante["estados"].values():
            total_cidades += estado_data["total_cidades"]
    
    print(f"\nEstatísticas:")
    print(f"Total de representantes: {total_representantes}")
    print(f"Total de estados: {total_estados}")
    print(f"Total de cidades: {total_cidades}")
    
    return arquivo_novo

def criar_exemplo_html():
    """Cria um exemplo de HTML que mostra como usar a nova estrutura."""
    
    html_exemplo = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Representantes por Estado - Exemplo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .representante {
            border: 1px solid #ddd;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            background: #fafafa;
        }
        .representante h3 {
            color: #333;
            margin-top: 0;
        }
        .estado {
            margin: 10px 0;
            padding: 10px;
            background: #e8f4fd;
            border-left: 4px solid #2196F3;
            border-radius: 3px;
        }
        .estado h4 {
            margin: 0 0 10px 0;
            color: #1976D2;
        }
        .cidades {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .cidade {
            background: #fff;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            border: 1px solid #ddd;
        }
        .contato {
            background: #f0f8ff;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .info {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Representantes por Estado</h1>
        <p>Esta é uma visualização da nova estrutura onde as cidades são filhas dos estados.</p>
        
        <div id="representantes"></div>
    </div>

    <script>
        // Função para carregar e exibir os dados
        async function carregarRepresentantes() {
            try {
                const response = await fetch('representantes_por_estado.json');
                const data = await response.json();
                
                const container = document.getElementById('representantes');
                
                for (const [codigo, representante] of Object.entries(data.representantes)) {
                    const div = document.createElement('div');
                    div.className = 'representante';
                    
                    let html = `
                        <h3>${representante.nome}</h3>
                        <div class="info">
                            <strong>Código:</strong> ${representante.codigo}<br>
                            <strong>Total de cidades:</strong> ${representante.total_cidades}
                        </div>
                    `;
                    
                    // Informações de contato
                    if (representante.contato) {
                        html += `
                            <div class="contato">
                                <strong>Contato:</strong> ${representante.contato.nome_contato}<br>
                                <strong>Email:</strong> ${representante.contato.email}<br>
                                <strong>Celular:</strong> ${representante.contato.celular}
                            </div>
                        `;
                    }
                    
                    // Estados e suas cidades
                    for (const [estado, dadosEstado] of Object.entries(representante.estados)) {
                        html += `
                            <div class="estado">
                                <h4>${estado} (${dadosEstado.total_cidades} cidades)</h4>
                                <div class="cidades">
                        `;
                        
                        for (const cidade of dadosEstado.cidades) {
                            html += `<span class="cidade">${cidade}</span>`;
                        }
                        
                        html += `
                                </div>
                            </div>
                        `;
                    }
                    
                    div.innerHTML = html;
                    container.appendChild(div);
                }
                
            } catch (error) {
                console.error('Erro ao carregar dados:', error);
                document.getElementById('representantes').innerHTML = 
                    '<p style="color: red;">Erro ao carregar os dados. Verifique se o arquivo representantes_por_estado.json está disponível.</p>';
            }
        }
        
        // Carregar dados quando a página carregar
        document.addEventListener('DOMContentLoaded', carregarRepresentantes);
    </script>
</body>
</html>"""
    
    with open("exemplo_representantes_por_estado.html", "w", encoding="utf-8") as f:
        f.write(html_exemplo)
    
    print("Exemplo HTML criado: exemplo_representantes_por_estado.html")

if __name__ == "__main__":
    print("=== Reorganização de Representantes por Estado ===")
    print()
    
    # Reorganizar o JSON
    arquivo_novo = reorganizar_representantes()
    
    print()
    print("=== Criando exemplo HTML ===")
    criar_exemplo_html()
    
    print()
    print("=== Concluído ===")
    print(f"1. JSON reorganizado: {arquivo_novo}")
    print("2. Exemplo HTML: exemplo_representantes_por_estado.html")
    print()
    print("Agora você pode:")
    print("- Acessar http://localhost:8000/exemplo_representantes_por_estado.html para ver o exemplo")
    print("- Usar a nova estrutura no seu HTML principal")
    print("- As cidades agora são filhas dos estados, evitando conflitos de nomes iguais") 