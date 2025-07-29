import json
import os
from collections import defaultdict
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import unicodedata
import re
from difflib import SequenceMatcher

def carregar_representantes():
    """Carrega os dados dos representantes do arquivo JSON"""
    with open('old/representantes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_municipios():
    """Carrega os dados geográficos dos municípios"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open('old/municipios.json', 'r', encoding=encoding) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"Erro com encoding {encoding}: {e}")
            continue
    
    raise Exception("Não foi possível carregar o arquivo municipios.json com nenhum encoding testado")

def normalizar_nome_avancado(nome):
    """Normalização avançada de nomes com correção de caracteres corrompidos"""
    if not nome or not isinstance(nome, str):
        return ""
    
    # Remove espaços extras e converte para maiúsculo
    nome = nome.strip().upper()
    
    # Mapeamento de caracteres corrompidos comuns
    correcoes_encoding = {
        # Caracteres corrompidos -> caracteres corretos
        'Ã': 'A',
        'Á': 'A', 'À': 'A', 'Â': 'A', 'Ä': 'A',
        'É': 'E', 'Ê': 'E', 'È': 'E', 'Ë': 'E',
        'Í': 'I', 'Î': 'I', 'Ì': 'I', 'Ï': 'I',
        'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ò': 'O', 'Ö': 'O',
        'Ú': 'U', 'Û': 'U', 'Ù': 'U', 'Ü': 'U',
        'Ç': 'C',
        'Ñ': 'N',
        # Caracteres corrompidos específicos
        '�': '',  # Remove caracteres de substituição
        'Ã\x83': 'A',
        'Ã\x95': 'O',
        'Ã\x87': 'C',
    }
    
    # Aplica correções de encoding
    for corrupto, correto in correcoes_encoding.items():
        nome = nome.replace(corrupto, correto)
    
    # Remove acentos usando unicodedata (fallback)
    nome = unicodedata.normalize('NFD', nome)
    nome = ''.join(char for char in nome if unicodedata.category(char) != 'Mn')
    
    # Normaliza espaços e hífens
    nome = re.sub(r'\s+', ' ', nome)  # Múltiplos espaços -> um espaço
    nome = re.sub(r'-+', '-', nome)   # Múltiplos hífens -> um hífen
    
    # Remove caracteres especiais exceto espaços, hífens e apóstrofes
    nome = re.sub(r'[^A-Z0-9\s\-\']+', '', nome)
    
    return nome.strip()

def calcular_similaridade(str1, str2):
    """Calcula similaridade entre duas strings usando SequenceMatcher"""
    return SequenceMatcher(None, str1, str2).ratio()

def encontrar_melhor_match(cidade_procurada, lista_municipios, threshold=0.8):
    """Encontra o melhor match para uma cidade na lista de municípios"""
    cidade_norm = normalizar_nome_avancado(cidade_procurada)
    
    melhor_match = None
    melhor_score = 0
    
    for municipio in lista_municipios:
        municipio_norm = normalizar_nome_avancado(municipio)
        
        # Verifica match exato primeiro
        if cidade_norm == municipio_norm:
            return municipio, 1.0
        
        # Calcula similaridade
        score = calcular_similaridade(cidade_norm, municipio_norm)
        
        if score > melhor_score and score >= threshold:
            melhor_score = score
            melhor_match = municipio
    
    return melhor_match, melhor_score if melhor_match else 0

def criar_mapa_municipios_melhorado(municipios_geojson):
    """Cria um mapa melhorado de nome de município para geometria"""
    mapa_municipios = {}
    nomes_originais = []
    
    for feature in municipios_geojson['features']:
        if 'properties' in feature:
            props = feature['properties']
            
            # Tenta diferentes campos que podem conter o nome
            nome_original = None
            campos_nome = ['NOME', 'NM_MUN', 'name', 'nome', 'municipio', 'cidade']
            
            for campo in campos_nome:
                if campo in props and isinstance(props[campo], str):
                    nome_original = props[campo]
                    break
            
            if nome_original:
                nome_normalizado = normalizar_nome_avancado(nome_original)
                if nome_normalizado:
                    mapa_municipios[nome_normalizado] = feature
                    nomes_originais.append(nome_original)
    
    return mapa_municipios, nomes_originais

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

def unir_geometrias_municipios_melhorado(cidades, mapa_municipios, nomes_originais):
    """Une as geometrias dos municípios com busca por similaridade"""
    geometrias = []
    cidades_encontradas = []
    cidades_nao_encontradas = []
    matches_por_similaridade = []
    
    for cidade in cidades:
        nome_normalizado = normalizar_nome_avancado(cidade)
        
        # Primeiro tenta match exato
        if nome_normalizado in mapa_municipios:
            feature = mapa_municipios[nome_normalizado]
            geometria = shape(feature['geometry'])
            geometrias.append(geometria)
            cidades_encontradas.append(cidade)
        else:
            # Tenta encontrar por similaridade
            melhor_match, score = encontrar_melhor_match(cidade, nomes_originais, threshold=0.75)
            
            if melhor_match and score >= 0.75:
                nome_match_normalizado = normalizar_nome_avancado(melhor_match)
                if nome_match_normalizado in mapa_municipios:
                    feature = mapa_municipios[nome_match_normalizado]
                    geometria = shape(feature['geometry'])
                    geometrias.append(geometria)
                    cidades_encontradas.append(cidade)
                    matches_por_similaridade.append({
                        'cidade_original': cidade,
                        'cidade_encontrada': melhor_match,
                        'score': score
                    })
                else:
                    cidades_nao_encontradas.append(cidade)
            else:
                cidades_nao_encontradas.append(cidade)
    
    if geometrias:
        # Une todas as geometrias em uma só
        geometria_unida = unary_union(geometrias)
        return {
            'geometry': mapping(geometria_unida),
            'cidades_encontradas': cidades_encontradas,
            'cidades_nao_encontradas': cidades_nao_encontradas,
            'matches_por_similaridade': matches_por_similaridade
        }
    
    return None

def processar_representantes_melhorado():
    """Função principal melhorada que processa os dados"""
    print("Carregando dados dos representantes...")
    dados_representantes = carregar_representantes()
    
    print("Carregando dados dos municípios...")
    municipios_geojson = carregar_municipios()
    
    print("Criando mapa melhorado de municípios...")
    mapa_municipios, nomes_originais = criar_mapa_municipios_melhorado(municipios_geojson)
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
        'total_cidades_nao_encontradas': 0,
        'total_matches_por_similaridade': 0
    }
    
    todos_matches_similaridade = []
    
    print("\nProcessando representantes com algoritmo melhorado...")
    for nome_rep, dados in representantes_cidades.items():
        estatisticas['total_representantes'] += 1
        cidades = list(set(dados['cidades']))  # Remove duplicatas
        estatisticas['total_cidades_processadas'] += len(cidades)
        
        print(f"\nProcessando: {nome_rep}")
        print(f"Cidades: {', '.join(cidades[:5])}{'...' if len(cidades) > 5 else ''}")
        
        resultado_geometria = unir_geometrias_municipios_melhorado(cidades, mapa_municipios, nomes_originais)
        
        if resultado_geometria:
            estatisticas['representantes_com_geometria'] += 1
            estatisticas['total_cidades_encontradas'] += len(resultado_geometria['cidades_encontradas'])
            estatisticas['total_cidades_nao_encontradas'] += len(resultado_geometria['cidades_nao_encontradas'])
            estatisticas['total_matches_por_similaridade'] += len(resultado_geometria['matches_por_similaridade'])
            
            todos_matches_similaridade.extend(resultado_geometria['matches_por_similaridade'])
            
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
                    "cidades_nao_encontradas": resultado_geometria['cidades_nao_encontradas'],
                    "matches_por_similaridade": resultado_geometria['matches_por_similaridade']
                },
                "geometry": resultado_geometria['geometry']
            }
            
            resultado['features'].append(feature)
            
            print(f"  ✓ Geometria criada: {len(resultado_geometria['cidades_encontradas'])} cidades encontradas")
            if resultado_geometria['matches_por_similaridade']:
                print(f"  🔍 Matches por similaridade: {len(resultado_geometria['matches_por_similaridade'])}")
                for match in resultado_geometria['matches_por_similaridade'][:3]:  # Mostra apenas os 3 primeiros
                    print(f"    '{match['cidade_original']}' → '{match['cidade_encontrada']}' (score: {match['score']:.2f})")
            if resultado_geometria['cidades_nao_encontradas']:
                print(f"  ⚠ Cidades ainda não encontradas: {len(resultado_geometria['cidades_nao_encontradas'])}")
                if len(resultado_geometria['cidades_nao_encontradas']) <= 5:
                    print(f"    {', '.join(resultado_geometria['cidades_nao_encontradas'])}")
        else:
            print(f"  ✗ Nenhuma geometria encontrada para as cidades")
    
    # Salva o resultado melhorado
    with open('representantes_geometrias_melhorado.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    # Salva relatório de matches por similaridade
    relatorio_matches = {
        'total_matches': len(todos_matches_similaridade),
        'matches': sorted(todos_matches_similaridade, key=lambda x: x['score'], reverse=True)
    }
    
    with open('relatorio_matches_similaridade.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio_matches, f, ensure_ascii=False, indent=2)
    
    # Exibe estatísticas melhoradas
    print("\n" + "="*70)
    print("ESTATÍSTICAS FINAIS - VERSÃO MELHORADA")
    print("="*70)
    print(f"Total de representantes processados: {estatisticas['total_representantes']}")
    print(f"Representantes com geometria criada: {estatisticas['representantes_com_geometria']}")
    print(f"Total de cidades processadas: {estatisticas['total_cidades_processadas']}")
    print(f"Cidades encontradas (match exato): {estatisticas['total_cidades_encontradas'] - estatisticas['total_matches_por_similaridade']}")
    print(f"Cidades encontradas (por similaridade): {estatisticas['total_matches_por_similaridade']}")
    print(f"Total de cidades mapeadas: {estatisticas['total_cidades_encontradas']}")
    print(f"Cidades ainda não encontradas: {estatisticas['total_cidades_nao_encontradas']}")
    
    taxa_sucesso = (estatisticas['total_cidades_encontradas'] / estatisticas['total_cidades_processadas']) * 100
    melhoria = estatisticas['total_matches_por_similaridade']
    
    print(f"\nTaxa de sucesso: {taxa_sucesso:.1f}%")
    print(f"Melhoria com algoritmo de similaridade: +{melhoria} cidades")
    
    print(f"\nArquivos salvos:")
    print(f"- representantes_geometrias_melhorado.json ({len(resultado['features'])} features)")
    print(f"- relatorio_matches_similaridade.json ({len(todos_matches_similaridade)} matches)")
    
    if todos_matches_similaridade:
        print(f"\nExemplos de matches por similaridade:")
        for match in sorted(todos_matches_similaridade, key=lambda x: x['score'], reverse=True)[:10]:
            print(f"  '{match['cidade_original']}' → '{match['cidade_encontrada']}' (score: {match['score']:.3f})")

if __name__ == "__main__":
    processar_representantes_melhorado()