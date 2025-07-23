class BrazilMap {
    constructor() {
        this.map = null;
        this.statesLayer = null;
        this.municipalitiesLayer = null;
        this.representativesData = null;
        this.statesData = null;
        this.municipalitiesData = null;
        this.showingMunicipalities = false;
        this.currentStateFilter = null;
        
        this.init();
    }
    
    async init() {
        try {
            this.showLoading();
            await this.loadData();
            this.initMap();
            this.setupEventListeners();
            this.hideLoading();
        } catch (error) {
            this.showError('Erro ao carregar o mapa: ' + error.message);
        }
    }
    
    async loadData() {
        try {
            const [representativesResponse, statesResponse, municipalitiesResponse] = await Promise.all([
                fetch('./representantes.json'),
                fetch('https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/uf/geojson/uf.json'),
                fetch('https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/municipio/geojson/municipio.json')
            ]);
            
            if (!representativesResponse.ok || !statesResponse.ok || !municipalitiesResponse.ok) {
                throw new Error('Erro ao carregar dados');
            }
            
            this.representativesData = await representativesResponse.json();
            this.statesData = await statesResponse.json();
            this.municipalitiesData = await municipalitiesResponse.json();
            
            console.log('Dados carregados:', {
                representatives: Object.keys(this.representativesData).length,
                states: this.statesData.features.length,
                municipalities: this.municipalitiesData.features.length
            });
            
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            throw error;
        }
    }
    
    initMap() {
        // Inicializar mapa Leaflet centrado no Brasil
        this.map = L.map('map', {
            center: [-14.2350, -51.9253], // Centro do Brasil
            zoom: 4,
            minZoom: 3,
            maxZoom: 12,
            zoomControl: true
        });
        
        // Adicionar tile layer (OpenStreetMap)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(this.map);
        
        // Adicionar camada de estados
        this.addStatesLayer();
        
        // Adicionar controles customizados
        this.addCustomControls();
    }
    
    addStatesLayer() {
        this.statesLayer = L.geoJSON(this.statesData, {
            style: (feature) => this.getStateStyle(feature),
            onEachFeature: (feature, layer) => this.onEachState(feature, layer)
        }).addTo(this.map);
    }
    
    getStateStyle(feature) {
        const stateName = this.getStateNameFromProperties(feature.properties);
        const hasRepresentatives = stateName && this.representativesData[stateName];
        
        return {
            fillColor: hasRepresentatives ? '#27ae60' : '#3498db',
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
        };
    }
    
    onEachState(feature, layer) {
        const stateName = this.getStateNameFromProperties(feature.properties);
        const displayName = feature.properties.name || feature.properties.nome || stateName;
        const hasRepresentatives = stateName && this.representativesData[stateName];
        
        // Popup
        const popupContent = `
            <h4>${displayName}</h4>
            <p><strong>Status:</strong> ${hasRepresentatives ? 'Com representantes' : 'Sem representantes'}</p>
            ${hasRepresentatives ? '<p>Clique para ver detalhes e fazer zoom</p>' : ''}
        `;
        layer.bindPopup(popupContent);
        
        // Eventos
        layer.on({
            mouseover: (e) => this.highlightFeature(e),
            mouseout: (e) => this.resetHighlight(e),
            click: (e) => this.selectState(stateName, layer)
        });
    }
    
    highlightFeature(e) {
        const layer = e.target;
        layer.setStyle({
            weight: 5,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.9
        });
        layer.bringToFront();
    }
    
    resetHighlight(e) {
        this.statesLayer.resetStyle(e.target);
    }
    
    selectState(stateName, layer) {
        if (!stateName || !this.representativesData[stateName]) {
            this.showError('Estado não possui representantes cadastrados.');
            return;
        }
        
        // Fazer zoom no estado
        this.map.fitBounds(layer.getBounds(), {
            padding: [20, 20],
            maxZoom: 8
        });
        
        // Filtrar municípios do estado
        this.currentStateFilter = stateName;
        
        // Mostrar municípios se não estiverem visíveis
        if (!this.showingMunicipalities) {
            this.toggleMunicipalityDisplay();
        } else {
            this.updateMunicipalitiesLayer();
        }
        
        // Mostrar informações do estado
        this.displayStateInfo(stateName);
    }
    
    addMunicipalitiesLayer() {
        if (this.municipalitiesLayer) {
            this.map.removeLayer(this.municipalitiesLayer);
        }
        
        // Filtrar municípios por estado se houver filtro ativo
        let filteredFeatures = this.municipalitiesData.features;
        if (this.currentStateFilter) {
            filteredFeatures = this.municipalitiesData.features.filter(feature => {
                const municipalityState = this.getMunicipalityState(feature.properties);
                return municipalityState === this.currentStateFilter;
            });
        }
        
        const filteredGeoJSON = {
            type: 'FeatureCollection',
            features: filteredFeatures
        };
        
        this.municipalitiesLayer = L.geoJSON(filteredGeoJSON, {
            style: (feature) => this.getMunicipalityStyle(feature),
            onEachFeature: (feature, layer) => this.onEachMunicipality(feature, layer)
        }).addTo(this.map);
    }
    
    getMunicipalityStyle(feature) {
        const municipalityName = feature.properties.name || feature.properties.nome;
        const municipalityState = this.getMunicipalityState(feature.properties);
        
        // Verificar se algum representante atende esta cidade
        let hasRepresentative = false;
        if (municipalityState && this.representativesData[municipalityState]) {
            const representatives = this.representativesData[municipalityState];
            hasRepresentative = Object.values(representatives).some(rep => 
                rep.cidades && rep.cidades.some(cidade => 
                    cidade.toLowerCase().includes(municipalityName.toLowerCase())
                )
            );
        }
        
        return {
            fillColor: hasRepresentative ? '#27ae60' : '#95a5a6',
            weight: 1,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.6
        };
    }
    
    onEachMunicipality(feature, layer) {
        const municipalityName = feature.properties.name || feature.properties.nome;
        const municipalityState = this.getMunicipalityState(feature.properties);
        
        // Popup
        const popupContent = `
            <h4>${municipalityName}</h4>
            <p><strong>Estado:</strong> ${municipalityState}</p>
            <p>Clique para ver representantes</p>
        `;
        layer.bindPopup(popupContent);
        
        // Eventos
        layer.on({
            mouseover: (e) => this.highlightMunicipality(e),
            mouseout: (e) => this.resetMunicipalityHighlight(e),
            click: (e) => this.selectMunicipality(municipalityName, municipalityState)
        });
    }
    
    highlightMunicipality(e) {
        const layer = e.target;
        layer.setStyle({
            weight: 3,
            color: '#666',
            fillOpacity: 0.9
        });
        layer.bringToFront();
    }
    
    resetMunicipalityHighlight(e) {
        this.municipalitiesLayer.resetStyle(e.target);
    }
    
    selectMunicipality(municipalityName, municipalityState) {
        this.displayMunicipalityInfo(municipalityName, municipalityState);
        this.findRepresentativesForCity(municipalityName, municipalityState);
    }
    
    updateMunicipalitiesLayer() {
        if (this.showingMunicipalities) {
            this.addMunicipalitiesLayer();
        }
    }
    
    toggleMunicipalityDisplay() {
        const button = document.getElementById('toggleMunicipalities');
        
        if (this.showingMunicipalities) {
            // Esconder municípios
            if (this.municipalitiesLayer) {
                this.map.removeLayer(this.municipalitiesLayer);
                this.municipalitiesLayer = null;
            }
            this.showingMunicipalities = false;
            button.textContent = 'Mostrar Municípios';
            button.classList.remove('active');
        } else {
            // Mostrar municípios
            this.addMunicipalitiesLayer();
            this.showingMunicipalities = true;
            button.textContent = 'Esconder Municípios';
            button.classList.add('active');
        }
    }
    
    resetView() {
        this.map.setView([-14.2350, -51.9253], 4);
        this.currentStateFilter = null;
        
        if (this.showingMunicipalities) {
            this.updateMunicipalitiesLayer();
        }
        
        this.clearResults();
    }
    
    addCustomControls() {
        // Controle para resetar visualização
        const resetControl = L.control({position: 'topright'});
        resetControl.onAdd = () => {
            const div = L.DomUtil.create('div', 'leaflet-control-custom');
            div.innerHTML = '🏠 Início';
            div.onclick = () => this.resetView();
            return div;
        };
        resetControl.addTo(this.map);
    }
    
    getStateNameFromProperties(properties) {
        if (!properties) {
            console.warn('Properties object is undefined');
            return null;
        }
        
        // Mapear nomes dos estados do GeoJSON para os nomes no representantes.json
        const stateMapping = {
            'Acre': 'ACRE',
            'Alagoas': 'ALAGOAS',
            'Amapá': 'AMAPA',
            'Amazonas': 'AMAZONAS',
            'Bahia': 'BAHIA',
            'Ceará': 'CEARA',
            'Distrito Federal': 'DISTRITO FEDERAL',
            'Espírito Santo': 'ESPIRITO SANTO',
            'Goiás': 'GOIAS',
            'Maranhão': 'MARANHAO',
            'Mato Grosso': 'MATO GROSSO',
            'Mato Grosso do Sul': 'MATO GROSSO DO SUL',
            'Minas Gerais': 'MINAS GERAIS',
            'Pará': 'PARA',
            'Paraíba': 'PARAIBA',
            'Paraná': 'PARANA',
            'Pernambuco': 'PERNAMBUCO',
            'Piauí': 'PIAUI',
            'Rio de Janeiro': 'RIO DE JANEIRO',
            'Rio Grande do Norte': 'RIO GRANDE DO NORTE',
            'Rio Grande do Sul': 'RIO GRANDE DO SUL',
            'Rondônia': 'RONDONIA',
            'Roraima': 'RORAIMA',
            'Santa Catarina': 'SANTA CATARINA',
            'São Paulo': 'SAO PAULO',
            'Sergipe': 'SERGIPE',
            'Tocantins': 'TOCANTINS'
        };
        
        const stateName = properties.name || properties.nome || properties.NOME || properties.nm_estado;
        
        if (!stateName) {
            console.warn('No state name found in properties:', properties);
            return null;
        }
        
        return stateMapping[stateName] || stateName.toUpperCase();
    }
    
    getMunicipalityState(properties) {
        // Tentar diferentes propriedades para o estado do município
        const stateCode = properties.uf || properties.state || properties.estado;
        const stateName = properties.state_name || properties.nome_estado;
        
        if (stateName) {
            return this.getStateNameFromProperties({name: stateName});
        }
        
        // Mapear códigos de UF para nomes completos
        const ufMapping = {
            'AC': 'ACRE', 'AL': 'ALAGOAS', 'AP': 'AMAPA', 'AM': 'AMAZONAS',
            'BA': 'BAHIA', 'CE': 'CEARA', 'DF': 'DISTRITO FEDERAL', 'ES': 'ESPIRITO SANTO',
            'GO': 'GOIAS', 'MA': 'MARANHAO', 'MT': 'MATO GROSSO', 'MS': 'MATO GROSSO DO SUL',
            'MG': 'MINAS GERAIS', 'PA': 'PARA', 'PB': 'PARAIBA', 'PR': 'PARANA',
            'PE': 'PERNAMBUCO', 'PI': 'PIAUI', 'RJ': 'RIO DE JANEIRO', 'RN': 'RIO GRANDE DO NORTE',
            'RS': 'RIO GRANDE DO SUL', 'RO': 'RONDONIA', 'RR': 'RORAIMA', 'SC': 'SANTA CATARINA',
            'SP': 'SAO PAULO', 'SE': 'SERGIPE', 'TO': 'TOCANTINS'
        };
        
        return ufMapping[stateCode] || stateCode;
    }
    
    displayStateInfo(stateName) {
        const representatives = this.representativesData[stateName];
        if (!representatives) {
            this.showError('Nenhum representante encontrado para este estado.');
            return;
        }
        
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = `
            <h3>Estado: ${stateName}</h3>
            <div id="representativesList"></div>
        `;
        
        const representativesList = document.getElementById('representativesList');
        
        Object.entries(representatives).forEach(([name, data]) => {
            const card = this.createRepresentativeCard(name, data);
            representativesList.appendChild(card);
        });
    }
    
    displayMunicipalityInfo(municipalityName, municipalityState) {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = `
            <h3>Município: ${municipalityName}</h3>
            <p><strong>Estado:</strong> ${municipalityState}</p>
            <div id="representativesList"></div>
        `;
        
        this.findRepresentativesForCity(municipalityName, municipalityState);
    }
    
    findRepresentativesForCity(cityName, stateName) {
        const representatives = this.representativesData[stateName];
        if (!representatives) {
            this.showError('Nenhum representante encontrado para este estado.');
            return;
        }
        
        const representativesList = document.getElementById('representativesList');
        const matchingRepresentatives = [];
        
        Object.entries(representatives).forEach(([name, data]) => {
            if (data.cidades && data.cidades.some(cidade => 
                cidade.toLowerCase().includes(cityName.toLowerCase())
            )) {
                matchingRepresentatives.push([name, data]);
            }
        });
        
        if (matchingRepresentatives.length === 0) {
            representativesList.innerHTML = '<p>Nenhum representante atende esta cidade especificamente.</p>';
            return;
        }
        
        matchingRepresentatives.forEach(([name, data]) => {
            const card = this.createRepresentativeCard(name, data);
            representativesList.appendChild(card);
        });
    }
    
    createRepresentativeCard(name, data) {
        const card = document.createElement('div');
        card.className = 'representative-card';
        
        const citiesHtml = data.cidades ? `
            <div class="cities-list">
                <h5>Cidades atendidas:</h5>
                <ul>
                    ${data.cidades.map(cidade => `<li>${cidade}</li>`).join('')}
                </ul>
            </div>
        ` : '';
        
        card.innerHTML = `
            <h4>${name}</h4>
            <p><strong>Telefone:</strong> ${data.telefone || 'Não informado'}</p>
            <p><strong>Email:</strong> ${data.email || 'Não informado'}</p>
            <p><strong>Endereço:</strong> ${data.endereco || 'Não informado'}</p>
            ${citiesHtml}
        `;
        
        return card;
    }
    
    performSearch() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
        if (!searchTerm) {
            this.clearResults();
            return;
        }
        
        const results = this.searchRepresentatives(searchTerm);
        this.displaySearchResults(results, searchTerm);
    }
    
    searchRepresentatives(searchTerm) {
        const results = [];
        
        Object.entries(this.representativesData).forEach(([stateName, representatives]) => {
            Object.entries(representatives).forEach(([repName, repData]) => {
                // Buscar por nome do representante
                if (repName.toLowerCase().includes(searchTerm)) {
                    results.push({
                        type: 'representative',
                        name: repName,
                        data: repData,
                        state: stateName,
                        matchType: 'nome'
                    });
                }
                
                // Buscar por cidades
                if (repData.cidades) {
                    repData.cidades.forEach(cidade => {
                        if (cidade.toLowerCase().includes(searchTerm)) {
                            results.push({
                                type: 'city',
                                name: repName,
                                data: repData,
                                state: stateName,
                                city: cidade,
                                matchType: 'cidade'
                            });
                        }
                    });
                }
            });
            
            // Buscar por estado
            if (stateName.toLowerCase().includes(searchTerm)) {
                Object.entries(representatives).forEach(([repName, repData]) => {
                    results.push({
                        type: 'state',
                        name: repName,
                        data: repData,
                        state: stateName,
                        matchType: 'estado'
                    });
                });
            }
        });
        
        return results;
    }
    
    displaySearchResults(results, searchTerm) {
        const resultsContainer = document.getElementById('results');
        
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <h3>Resultados da busca</h3>
                <p>Nenhum resultado encontrado para "${searchTerm}".</p>
            `;
            return;
        }
        
        resultsContainer.innerHTML = `
            <h3>Resultados da busca (${results.length})</h3>
            <div id="searchResults"></div>
        `;
        
        const searchResults = document.getElementById('searchResults');
        
        results.forEach(result => {
            const card = this.createRepresentativeCard(result.name, result.data);
            
            // Adicionar informação sobre o tipo de match
            const matchInfo = document.createElement('p');
            matchInfo.style.fontStyle = 'italic';
            matchInfo.style.color = '#7f8c8d';
            matchInfo.style.fontSize = '0.85rem';
            
            switch (result.matchType) {
                case 'nome':
                    matchInfo.textContent = `Encontrado por nome do representante`;
                    break;
                case 'cidade':
                    matchInfo.textContent = `Encontrado por cidade: ${result.city}`;
                    break;
                case 'estado':
                    matchInfo.textContent = `Encontrado por estado: ${result.state}`;
                    break;
            }
            
            card.insertBefore(matchInfo, card.firstChild.nextSibling);
            searchResults.appendChild(card);
        });
    }
    
    clearResults() {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = `
            <h3>Informações</h3>
            <p>Clique em um estado ou município para ver os representantes.</p>
        `;
    }
    
    setupEventListeners() {
        // Busca
        const searchButton = document.getElementById('searchButton');
        const searchInput = document.getElementById('searchInput');
        
        searchButton.addEventListener('click', () => this.performSearch());
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
        
        // Controles do mapa
        const toggleMunicipalitiesBtn = document.getElementById('toggleMunicipalities');
        const resetViewBtn = document.getElementById('resetView');
        
        toggleMunicipalitiesBtn.addEventListener('click', () => this.toggleMunicipalityDisplay());
        resetViewBtn.addEventListener('click', () => this.resetView());
    }
    
    showLoading() {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = '<div class="loading">Carregando dados...</div>';
    }
    
    hideLoading() {
        this.clearResults();
    }
    
    showError(message) {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = `
            <div class="error-message">
                <strong>Erro:</strong> ${message}
            </div>
        `;
    }
}

// Inicializar o mapa quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    new BrazilMap();
});