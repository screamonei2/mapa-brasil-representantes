import json
import os
from collections import defaultdict
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

def carregar_representantes():
    """Carrega os dados dos representantes do arquivo JSON"""
    with open('old/representantes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_municipios():
    """Carrega os dados geográficos dos municípios"""
    # Tenta diferentes encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open('old/municipios.json', 'r', encoding=encoding) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"Erro com encoding {encoding}: {e}")
            continue
    
    raise Exception("Não foi possível carregar o arquivo municipios.json com nenhum encoding testado")

def normalizar_nome_cidade(nome):
    """Normaliza o nome da cidade para comparação"""
    return nome.upper().strip().replace('Ã', 'A').replace('Õ', 'O')

def criar_mapa_municipios(municipios_geojson):
    """Cria um mapa de nome de município para geometria"""
    mapa_municipios = {}
    
    for feature in municipios_geojson['features']:
        if 'properties' in feature and 'NM_MUN' in feature['properties']:
            nome = normalizar_nome_cidade(feature['properties']['NM_MUN'])
            mapa_municipios[nome] = feature
        elif 'properties' in feature and 'name' in feature['properties']:
            nome = normalizar_nome_cidade(feature['properties']['name'])
            mapa_municipios[nome] = feature
        elif 'properties' in feature:
            # Tenta encontrar qualquer campo que possa ser o nome
            for key, value in feature['properties'].items():
                if isinstance(value, str) and len(value) > 2:
                    nome = normalizar_nome_cidade(value)
                    if nome not in mapa_municipios:
                        mapa_municipios[nome] = feature
                    break
    
    return mapa_municipios

def agrupar_por_representante(dados_representantes):
    """Agrupa cidades por representante"""
    representantes_cidades = {}
    
    for estado, representantes in dados_representantes.items():
        for nome_rep, dados_rep in representantes.items():
            codigo = dados_rep['dados_contato']['codigo_representante']
            cidades = dados_rep['cidades_atendidas']
            
            # Cria uma chave única para o representante
            chave_rep = f"{codigo} - {nome_rep}"
            
            if chave_rep not in representantes_cidades:
                representantes_cidades[chave_rep] = {
                    'dados_contato': dados_rep['dados_contato'],
                    'cidades': []
                }
            
            representantes_cidades[chave_rep]['cidades'].extend(cidades)
    
    return representantes_cidades

def unir_geometrias_municipios(cidades, mapa_municipios):
    """Une as geometrias dos municípios de um representante"""
    geometrias = []
    cidades_encontradas = []
    cidades_nao_encontradas = []
    
    for cidade in cidades:
        nome_normalizado = normalizar_nome_cidade(cidade)
        
        if nome_normalizado in mapa_municipios:
            feature = mapa_municipios[nome_normalizado]
            geometria = shape(feature['geometry'])
            geometrias.append(geometria)
            cidades_encontradas.append(cidade)
        else:
            cidades_nao_encontradas.append(cidade)
    
    if geometrias:
        # Une todas as geometrias em uma só
        geometria_unida = unary_union(geometrias)
        return {
            'geometry': mapping(geometria_unida),
            'cidades_encontradas': cidades_encontradas,
            'cidades_nao_encontradas': cidades_nao_encontradas
        }
    
    return None

def processar_representantes():
    """Função principal que processa os dados"""
    print("Carregando dados dos representantes...")
    dados_representantes = carregar_representantes()
    
    print("Carregando dados dos municípios...")
    municipios_geojson = carregar_municipios()
    
    print("Criando mapa de municípios...")
    mapa_municipios = criar_mapa_municipios(municipios_geojson)
    print(f"Encontrados {len(mapa_municipios)} municípios no arquivo geográfico")
    
    print("Agrupando cidades por representante...")
    representantes_cidades = agrupar_por_representante(dados_representantes)
    print(f"Encontrados {len(representantes_cidades)} representantes")
    
    # Resultado final
    resultado = {
        "type": "FeatureCollection",
        "features": []
    }
    
    estatisticas = {
        'total_representantes': 0,
        'representantes_com_geometria': 0,
        'total_cidades_processadas': 0,
        'total_cidades_encontradas': 0,
        'total_cidades_nao_encontradas': 0
    }
    
    print("\nProcessando representantes...")
    for nome_rep, dados in representantes_cidades.items():
        estatisticas['total_representantes'] += 1
        cidades = list(set(dados['cidades']))  # Remove duplicatas
        estatisticas['total_cidades_processadas'] += len(cidades)
        
        print(f"\nProcessando: {nome_rep}")
        print(f"Cidades: {', '.join(cidades[:5])}{'...' if len(cidades) > 5 else ''}")
        
        resultado_geometria = unir_geometrias_municipios(cidades, mapa_municipios)
        
        if resultado_geometria:
            estatisticas['representantes_com_geometria'] += 1
            estatisticas['total_cidades_encontradas'] += len(resultado_geometria['cidades_encontradas'])
            estatisticas['total_cidades_nao_encontradas'] += len(resultado_geometria['cidades_nao_encontradas'])
            
            feature = {
                "type": "Feature",
                "properties": {
                    "representante": nome_rep,
                    "codigo_representante": dados['dados_contato']['codigo_representante'],
                    "contato": dados['dados_contato']['contato'],
                    "email": dados['dados_contato']['email'],
                    "celular": dados['dados_contato']['celular'],
                    "total_cidades": len(cidades),
                    "cidades_encontradas": resultado_geometria['cidades_encontradas'],
                    "cidades_nao_encontradas": resultado_geometria['cidades_nao_encontradas']
                },
                "geometry": resultado_geometria['geometry']
            }
            
            resultado['features'].append(feature)
            
            print(f"  ✓ Geometria criada: {len(resultado_geometria['cidades_encontradas'])} cidades encontradas")
            if resultado_geometria['cidades_nao_encontradas']:
                print(f"  ⚠ Cidades não encontradas: {', '.join(resultado_geometria['cidades_nao_encontradas'])}")
        else:
            print(f"  ✗ Nenhuma geometria encontrada para as cidades")
    
    # Salva o resultado
    with open('representantes_geometrias.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    # Exibe estatísticas
    print("\n" + "="*60)
    print("ESTATÍSTICAS FINAIS")
    print("="*60)
    print(f"Total de representantes processados: {estatisticas['total_representantes']}")
    print(f"Representantes com geometria criada: {estatisticas['representantes_com_geometria']}")
    print(f"Total de cidades processadas: {estatisticas['total_cidades_processadas']}")
    print(f"Cidades encontradas no mapa: {estatisticas['total_cidades_encontradas']}")
    print(f"Cidades não encontradas: {estatisticas['total_cidades_nao_encontradas']}")
    print(f"\nArquivo salvo como: representantes_geometrias.json")
    print(f"Total de features no arquivo: {len(resultado['features'])}")

if __name__ == "__main__":
    processar_representantes()