import json

# Estados que a SCHIOPPA deve atender
estados_schioppa = ['SE', 'RR', 'RN', 'AL', 'RO', 'MA', 'AP', 'AC']

def extrair_municipios_do_geojson():
    """Extrai municípios do arquivo GeoJSON existente"""
    try:
        with open('old/geojs-100-mun-v2.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        municipios_por_estado = {}
        
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            
            # Extrair UF do campo uf_municipio (formato: "UF - Município")
            uf_municipio = props.get('uf_municipio', '')
            if ' - ' in uf_municipio:
                uf, municipio = uf_municipio.split(' - ', 1)
                uf = uf.strip()
                municipio = municipio.strip().upper()
                
                if uf in estados_schioppa:
                    if uf not in municipios_por_estado:
                        municipios_por_estado[uf] = []
                    municipios_por_estado[uf].append(municipio)
        
        return municipios_por_estado
    
    except Exception as e:
        print(f"Erro ao ler arquivo GeoJSON: {e}")
        return {}

def main():
    print("Extraindo municípios do arquivo GeoJSON...")
    
    municipios_por_estado = extrair_municipios_do_geojson()
    
    todas_cidades = []
    
    for estado in estados_schioppa:
        municipios = municipios_por_estado.get(estado, [])
        todas_cidades.extend(municipios)
        print(f"Estado {estado}: {len(municipios)} municípios")
    
    # Remover duplicatas e ordenar
    todas_cidades = sorted(list(set(todas_cidades)))
    
    print(f"\nTotal de cidades únicas encontradas: {len(todas_cidades)}")
    
    # Salvar em arquivo
    resultado = {
        'estados': estados_schioppa,
        'total_cidades': len(todas_cidades),
        'cidades': todas_cidades,
        'municipios_por_estado': {k: sorted(list(set(v))) for k, v in municipios_por_estado.items()}
    }
    
    with open('cidades_schioppa.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print("Arquivo 'cidades_schioppa.json' criado com sucesso!")
    
    # Mostrar algumas cidades como exemplo
    print("\nPrimeiras 10 cidades:")
    for cidade in todas_cidades[:10]:
        print(f"  - {cidade}")
    
    return todas_cidades

if __name__ == "__main__":
    main()