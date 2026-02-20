# 📊 Streamlit Dashboard - Guia Completo

## O que foi criado

Um dashboard interativo em Streamlit com **visualizações avançadas, filtros interativos e comparações entre keywords**.

## Funcionalidades Principais

### 1. **📈 Aba de Resumo**
- Estatísticas gerais (total de keywords, com dados, média, erros)
- **Seletor de métrica**: Máximo, Média, Mínimo
- Gráficos comparativos Google Trends vs Wikipedia
- Visualização dos Top 15 keywords

### 2. **📋 Aba de Tabela Completa**
- Tabela com todos os dados
- **Filtros interativos**:
  - 🔍 Buscar por keyword
  - 📊 Filtrar por Google Trends (0-100)
  - 🌍 Filtrar por região
- Download em CSV
- 6 colunas de dados: máximo, média, mínimo (Google + Wiki)

### 3. **🎯 Aba de Comparativos**
- Seleção múltipla de keywords
- **3 gráficos lado a lado**:
  - Máximo (Google vs Wiki)
  - Média (Google vs Wiki)
  - Mínimo (Google vs Wiki)
- Tabela de comparação
- Análise visual de tendências

### 4. **⚠️ Aba de Erros**
- Lista de todos os erros encontrados
- Útil para debug

## Como Usar

### Opção 1: Usando o Script (Recomendado)
```bash
./run_dashboard.sh
```

### Opção 2: Comando Direto
```bash
source venv/bin/activate
streamlit run streamlit_dashboard.py
```

O dashboard abrirá em **http://localhost:8501**

## Fluxo de Uso

1. **Upload de Arquivo ou Exemplo**
   - Selecione modo no sidebar
   - Carregue CSV/Excel com keywords
   - Ou use arquivo de exemplo

2. **Visualize o Preview**
   - Confirme que os dados estão corretos
   - Verifique colunas: keyword, geo, timeframe, language

3. **Processe os Dados**
   - Clique em "Processar"
   - Aguarde o processamento
   - Sistema fará requisições ao Google Trends e Wikipedia

4. **Explore os Resultados**
   - **Resumo**: Visão geral com gráficos
   - **Tabela**: Dados completos com filtros
   - **Comparativos**: Análises avançadas entre keywords
   - **Erros**: Troubleshooting

## Colunas de Dados

| Coluna | Descrição |
|--------|-----------|
| `keyword` | Palavra-chave analisada |
| `geo` | Código de país (ex: BR, US) |
| `timeframe` | Período analisado |
| `language` | Idioma para Wikipedia |
| `google_max` | Valor máximo Google Trends |
| `google_mean` | Valor médio Google Trends |
| `google_min` | Valor mínimo Google Trends |
| `wiki_max` | Máximo de views Wikipedia |
| `wiki_mean` | Média de views Wikipedia |
| `wiki_min` | Mínimo de views Wikipedia |
| `top_region` | Região com maior interesse |

## Filtros Disponíveis

### Tab 2 - Tabela Completa
1. **🔍 Buscar keyword**: Busca textual case-insensitive
2. **📊 Google Trends (mínimo)**: Filtra por valor mínimo de Google
3. **🌍 Região**: Seleciona região específica ou "Todas"

### Tab 3 - Comparativos
1. **Seleção múltipla**: Escolha até X keywords para comparar
2. **Visualização automática**: Gráficos atualizam conforme seleção

## Gráficos

### Tipo: Gráficos de Barras Horizontais
- **Google Trends**: Cor azul
- **Wikipedia**: Cor laranja, vermelha, roxa, etc.

### Interatividade Plotly
- Hover para ver valores exatos
- Zoom com mouse
- Download de imagem
- Pan/Scroll

## Arquivos Criados

```
streamlit_dashboard.py      # Dashboard Streamlit (400+ linhas)
run_dashboard.sh            # Script executável
requirements.txt            # Dependências atualizadas
execution/trends_tool_batch.py  # Método get_results_dataframe() adicionado
```

## Requisitos

- Python 3.7+
- Streamlit >= 1.28.0
- Plotly
- Pandas
- Pytrends

Instale com:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### Erro 429 (Rate Limit)
Espere alguns minutos entre execuções. Google Trends tem limite de requisições.

### Arquivo de exemplo não encontrado
Certifique-se que `input_example.csv` existe no diretório raiz

### Dados zerados
Verifique a conexão com internet e os nomes das colunas

## Próximas Melhorias

- [ ] PDF export
- [ ] Temporal analysis com gráficos de série temporal
- [ ] ML predictions
- [ ] Cache de dados
- [ ] Deployment em Streamlit Cloud

## Arquitetura

```
Input (CSV/Excel)
       ↓
TrendsBatchAnalyzer (process_batch)
       ↓
Get_results_dataframe() (agregação)
       ↓
Streamlit Dashboard (visualização)
       ├─ Tab 1: Resumo
       ├─ Tab 2: Tabela com filtros
       ├─ Tab 3: Comparativos
       └─ Tab 4: Erros
```

---

**Versão**: 1.0  
**Data**: 20 de Fevereiro de 2026  
**Status**: ✅ Pronto para usar
