import json
from collections import defaultdict, Counter
import re

def carregar_dados():
    """Carrega os dados processados dos representantes"""
    with open('representantes_geometrias.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_municipios():
    """Carrega os dados dos municípios para análise"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open('old/municipios.json', 'r', encoding=encoding) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    
    raise Exception("Não foi possível carregar o arquivo municipios.json")

def extrair_nomes_municipios(municipios_geojson):
    """Extrai todos os nomes de municípios do arquivo geográfico"""
    nomes_encontrados = set()
    
    for feature in municipios_geojson['features']:
        if 'properties' in feature:
            props = feature['properties']
            
            # Tenta diferentes campos que podem conter o nome
            campos_nome = ['NM_MUN', 'name', 'nome', 'municipio', 'cidade']
            
            for campo in campos_nome:
                if campo in props and isinstance(props[campo], str):
                    nome = props[campo].upper().strip()
                    nomes_encontrados.add(nome)
                    break
    
    return nomes_encontrados

def normalizar_nome(nome):
    """Normaliza o nome para comparação"""
    # Remove acentos e caracteres especiais
    nome = nome.upper().strip()
    
    # Substituições comuns
    substituicoes = {
        'Ã': 'A', 'Á': 'A', 'À': 'A', 'Â': 'A',
        'É': 'E', 'Ê': 'E', 'È': 'E',
        'Í': 'I', 'Î': 'I', 'Ì': 'I',
        'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ò': 'O',
        'Ú': 'U', 'Û': 'U', 'Ù': 'U',
        'Ç': 'C',
        'Ñ': 'N'
    }
    
    for original, substituto in substituicoes.items():
        nome = nome.replace(original, substituto)
    
    return nome

def encontrar_similares(cidade_nao_encontrada, nomes_municipios):
    """Encontra nomes similares no arquivo de municípios"""
    cidade_norm = normalizar_nome(cidade_nao_encontrada)
    similares = []
    
    for nome_mun in nomes_municipios:
        nome_mun_norm = normalizar_nome(nome_mun)
        
        # Verifica se é uma substring
        if cidade_norm in nome_mun_norm or nome_mun_norm in cidade_norm:
            similares.append(nome_mun)
        
        # Verifica similaridade por palavras
        palavras_cidade = set(cidade_norm.split())
        palavras_municipio = set(nome_mun_norm.split())
        
        if palavras_cidade & palavras_municipio:  # Interseção não vazia
            if nome_mun not in similares:
                similares.append(nome_mun)
    
    return similares[:5]  # Retorna até 5 similares

def categorizar_motivos(cidade, similares):
    """Categoriza o motivo pelo qual a cidade não foi encontrada"""
    cidade_norm = normalizar_nome(cidade)
    
    # Verifica se é um nome muito genérico
    nomes_genericos = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'GO', 'MT', 'MS', 'BA']
    if cidade_norm in nomes_genericos:
        return "Nome muito genérico (sigla de estado)"
    
    # Verifica se pode ser um bairro ou distrito
    indicadores_bairro = ['CENTRO', 'VILA', 'JARDIM', 'PARQUE', 'CONJUNTO']
    for indicador in indicadores_bairro:
        if indicador in cidade_norm:
            return "Possível bairro ou distrito"
    
    # Verifica se tem similares
    if similares:
        return f"Nome similar encontrado: {similares[0]}"
    
    # Verifica se pode ser grafia antiga ou alternativa
    if len(cidade_norm) > 3:
        return "Possível grafia alternativa ou nome antigo"
    
    return "Município não identificado no arquivo geográfico"

def analisar_cidades_nao_encontradas():
    """Análise principal das cidades não encontradas"""
    print("Carregando dados...")
    dados_representantes = carregar_dados()
    municipios_geojson = carregar_municipios()
    
    print("Extraindo nomes de municípios do arquivo geográfico...")
    nomes_municipios = extrair_nomes_municipios(municipios_geojson)
    print(f"Encontrados {len(nomes_municipios)} nomes únicos no arquivo geográfico")
    
    # Coleta todas as cidades não encontradas
    todas_cidades_nao_encontradas = []
    cidades_por_representante = {}
    
    for feature in dados_representantes['features']:
        props = feature['properties']
        representante = props['representante']
        cidades_nao_encontradas = props['cidades_nao_encontradas']
        
        if cidades_nao_encontradas:
            cidades_por_representante[representante] = cidades_nao_encontradas
            todas_cidades_nao_encontradas.extend(cidades_nao_encontradas)
    
    # Conta frequência das cidades não encontradas
    contador_cidades = Counter(todas_cidades_nao_encontradas)
    
    print(f"\nTotal de cidades não encontradas: {len(todas_cidades_nao_encontradas)}")
    print(f"Cidades únicas não encontradas: {len(contador_cidades)}")
    
    # Análise detalhada
    analise_detalhada = []
    motivos_counter = Counter()
    
    print("\nAnalisando cada cidade não encontrada...")
    
    for cidade, frequencia in contador_cidades.most_common():
        similares = encontrar_similares(cidade, nomes_municipios)
        motivo = categorizar_motivos(cidade, similares)
        
        analise_detalhada.append({
            'cidade': cidade,
            'frequencia': frequencia,
            'similares': similares,
            'motivo': motivo
        })
        
        motivos_counter[motivo] += 1
    
    # Relatório final
    print("\n" + "="*80)
    print("RELATÓRIO DE CIDADES NÃO ENCONTRADAS")
    print("="*80)
    
    print(f"\nESTATÍSTICAS GERAIS:")
    print(f"- Total de ocorrências: {len(todas_cidades_nao_encontradas)}")
    print(f"- Cidades únicas: {len(contador_cidades)}")
    print(f"- Representantes afetados: {len(cidades_por_representante)}")
    
    print(f"\nMOTIVOS MAIS COMUNS:")
    for motivo, count in motivos_counter.most_common():
        print(f"- {motivo}: {count} cidades")
    
    print(f"\nCIDADES MAIS PROBLEMÁTICAS (por frequência):")
    for i, item in enumerate(analise_detalhada[:20], 1):
        print(f"{i:2d}. {item['cidade']} (aparece {item['frequencia']}x)")
        print(f"    Motivo: {item['motivo']}")
        if item['similares']:
            print(f"    Similares: {', '.join(item['similares'][:3])}")
        print()
    
    print(f"\nREPRESENTANTES MAIS AFETADOS:")
    representantes_ordenados = sorted(cidades_por_representante.items(), 
                                    key=lambda x: len(x[1]), reverse=True)
    
    for i, (rep, cidades) in enumerate(representantes_ordenados[:10], 1):
        print(f"{i:2d}. {rep}")
        print(f"    Cidades não encontradas: {len(cidades)}")
        print(f"    Exemplos: {', '.join(cidades[:5])}{'...' if len(cidades) > 5 else ''}")
        print()
    
    # Salva relatório detalhado
    relatorio = {
        'estatisticas': {
            'total_ocorrencias': len(todas_cidades_nao_encontradas),
            'cidades_unicas': len(contador_cidades),
            'representantes_afetados': len(cidades_por_representante)
        },
        'motivos': dict(motivos_counter),
        'cidades_detalhadas': analise_detalhada,
        'representantes_afetados': cidades_por_representante
    }
    
    with open('relatorio_cidades_nao_encontradas.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\nRelatório detalhado salvo em: relatorio_cidades_nao_encontradas.json")
    
    # Sugestões de correção
    print(f"\nSUGESTÕES DE CORREÇÃO:")
    print("1. Verificar se os nomes estão com grafia correta")
    print("2. Alguns podem ser bairros ou distritos, não municípios")
    print("3. Verificar se são nomes antigos de municípios")
    print("4. Alguns podem ser siglas que precisam ser expandidas")
    print("5. Verificar encoding do arquivo original de representantes")

if __name__ == "__main__":
    analisar_cidades_nao_encontradas()