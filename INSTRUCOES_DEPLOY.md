# 🚀 Instruções para Deploy na Vercel

## ✅ Arquivos Preparados

O diretório `vercel-deploy/` foi criado com todos os arquivos necessários:

### 📁 Estrutura do Projeto
```
vercel-deploy/
├── index.html                    # Aplicação principal (76KB)
├── representantes_por_estado.json # Dados dos representantes (312KB)
├── geojs-100-mun-v2.json        # Dados dos municípios (55MB)
├── uf.json                       # Dados dos estados (2.5MB)
├── vercel.json                   # Configuração Vercel
├── deploy.sh                     # Script de deploy
├── README.md                     # Documentação
└── .gitignore                    # Arquivos ignorados
```

### 📊 Tamanho Total: ~58MB

## 🎯 Opções de Deploy

### 1. **Via GitHub (Recomendado)**

```bash
# 1. Crie um novo repositório no GitHub
# 2. Faça push do diretório vercel-deploy
cd vercel-deploy
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main

# 3. Conecte na Vercel
# - Acesse vercel.com
# - Importe o repositório
# - Deploy automático
```

### 2. **Via Vercel CLI**

```bash
cd vercel-deploy
./deploy.sh
```

### 3. **Via Interface Web**

1. Acesse [vercel.com](https://vercel.com)
2. Faça login/cadastro
3. Clique em "New Project"
4. Faça upload do diretório `vercel-deploy`
5. Clique em "Deploy"

## 🔧 Configurações

### Arquivo `vercel.json`
- Configurado para servir arquivos estáticos
- Headers CORS configurados
- Rotas configuradas para todos os arquivos

### Funcionalidades da Aplicação
- ✅ Mapa interativo do Brasil
- ✅ Busca por estado/município
- ✅ Visualização de representantes
- ✅ Interface responsiva
- ✅ Destaque de áreas atendidas

## 🌐 Após o Deploy

1. A Vercel fornecerá uma URL (ex: `https://seu-projeto.vercel.app`)
2. A aplicação estará disponível imediatamente
3. Qualquer push para o GitHub atualizará automaticamente

## 📝 Notas Importantes

- **Tamanho dos arquivos**: O arquivo `geojs-100-mun-v2.json` (55MB) pode demorar um pouco para carregar na primeira vez
- **CDN**: A Vercel usa CDN global, então o carregamento será rápido
- **HTTPS**: Automático e obrigatório na Vercel
- **Domínio customizado**: Pode ser configurado nas configurações do projeto

## 🐛 Troubleshooting

Se houver problemas:

1. **Erro de CORS**: Verifique se o `vercel.json` está correto
2. **Arquivos não encontrados**: Verifique se todos os arquivos estão no diretório
3. **Erro de build**: A aplicação é estática, não deve ter problemas de build

## 📞 Suporte

- [Documentação Vercel](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions) 