# 📊 Trends Tool - Batch Processing com Entrada de Planilha

## ✨ Novo Recurso: Processamento em Lote

O script foi adaptado para receber uma planilha como input e gerar um relatório consolidado em Excel com todas as análises.

## 🚀 Instalação e Setup

### 1. Criar Ambiente Virtual
```bash
cd trends_tool_full
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

## 📋 Como Usar

### Comando Básico
```bash
python3 execution/trends_tool_batch.py input.xlsx
```

### Especificar Arquivo de Saída
```bash
python3 execution/trends_tool_batch.py keywords.csv -o meu_relatorio.xlsx
```

## 📁 Formato do Arquivo de Entrada

### Estrutura Obrigatória
**Coluna obrigatória:**
- `keyword` - Palavra-chave para análise

**Colunas opcionais:**
- `geo` - Código da região (padrão: BR)
- `timeframe` - Período de análise (padrão: today 12-m)
- `language` - Código de idioma Wikipedia (padrão: pt)

### Valores Padrão Automáticos
Se a coluna não existir ou tiver célula vazia:
- **geo**: `BR` (Brasil)
- **timeframe**: `today 12-m` (últimos 12 meses)
- **language**: `pt` (português)

### Exemplos de Entrada

#### ✅ Exemplo 1: CSV Mínimo (apenas keyword)
```csv
keyword
Python
Dengue
Machine Learning
```
✓ Todos processados com padrões: BR, 12 meses, português

#### ✅ Exemplo 2: CSV com Alguns Valores
```csv
keyword,geo,language
Python,US,en
Dengue,BR,pt
IA,BR,
```
✓ IA usa defaults: geo=BR (já tem), timeframe=today 12-m, language=pt

#### ✅ Exemplo 3: Arquivo Excel Completo
| keyword | geo | timeframe | language |
|---------|-----|-----------|----------|
| Python | BR | today 12-m | pt |
| Dengue | US | today 6-m | en |
| Trends | | 2024-01-01 2024-12-31 | pt |

## 🌍 Códigos Disponíveis

### Regiões (geo)
```
BR - Brasil
US - Estados Unidos
MX - México
GB - Reino Unido
DE - Alemanha
FR - França
IT - Itália
ES - Espanha
JP - Japão
CN - China
IN - Índia
AU - Austrália
CA - Canadá
AR - Argentina
PT - Portugal
```

### Períodos (timeframe)
```
today 1-m     - Último mês
today 3-m     - Últimos 3 meses
today 12-m    - Últimos 12 meses
today 5-y     - Últimos 5 anos
2024-01-01 2024-12-31  - Data específica
```

### Idiomas Wikipedia (language)
```
pt - Português
en - Inglês
es - Espanhol
fr - Francês
de - Alemão
it - Italiano
ja - Japonês
zh - Chinês
ru - Russo
ar - Árabe
hi - Hindi
```

## 📊 Formato do Relatório de Saída

### Estrutura Excel
Cada keyword tem sua própria **aba** contendo:

1. **📝 Cabeçalho com Parâmetros**
   - Nome do keyword
   - Data e hora de geração
   - Parâmetros usados (região, período, idioma)

2. **📈 Gráfico Dual-Axis**
   - Google Trends (em azul, eixo esquerdo)
   - Wikipedia Pageviews (em laranja, eixo direito)
   - Incluído diretamente na planilha

3. **📋 Tabela - Google Trends (Interesse ao Longo do Tempo)**
   - Data
   - Valor de interesse (0-100)
   - Últimos 10 registros

4. **🗺️ Tabela - Interesse por Região**
   - Região/estado
   - Interesse relativo
   - Top 10 regiões ordenadas

5. **📚 Tabela - Wikipedia Pageviews**
   - Data
   - Número de visualizações
   - Últimos 10 registros

## ✅ Validações Implementadas

### 1. Validação de Entrada
- ✓ Coluna `keyword` é obrigatória
- ✓ Keywords vazias são rejeitadas
- ✓ Nomes de colunas normalizados (lowercase)
- ✓ Espaços em branco removidos

### 2. Valores Padrão
- ✓ Colunas faltantes preenchidas com defaults
- ✓ Células vazias substituídas por padrões
- ✓ Continuidade no processamento

### 3. Validação de Códigos
- ✓ Aviso se geo code inválido (não interrompe)
- ✓ Aviso se language code inválido (não interrompe)
- ✓ Processamento robusto

### 4. Tratamento de Erros
- ✓ Falhas isoladas por keyword
- ✓ Processamento continua mesmo com erros
- ✓ Relatório final com resumo de erros

## 🎯 Exemplos de Uso Prático

### Cenário 1: Análise Simples
```bash
# Arquivo: keywords_simples.csv
keyword
Python
JavaScript
Go

# Comando
python3 execution/trends_tool_batch.py keywords_simples.csv

# Resultado
# - Todas com: BR, 12 meses, português
# - Arquivo: output/trends_report.xlsx
```

### Cenário 2: Análise com Customização
```bash
# Arquivo: keywords_customizado.csv
keyword,geo,timeframe
Python,US,today 6-m
Dengue,BR,today 12-m
Machine Learning,GB,2023-01-01 2023-12-31

# Comando
python3 execution/trends_tool_batch.py keywords_customizado.csv -o analise_2024.xlsx

# Resultado
# - 3 keywords com parâmetros personalizados
# - Arquivo: output/analise_2024.xlsx
```

### Cenário 3: Análise Global
```bash
# Arquivo: keywords_global.xlsx
keyword,geo,language
Python,US,en
Python,BR,pt
Python,DE,de
Dengue,BR,pt

# Comando
python3 execution/trends_tool_batch.py keywords_global.xlsx -o trends_global.xlsx

# Resultado
# - 4 abas diferentes para cada combinação
# - Arquivo: output/trends_global.xlsx
```

## ⚠️ Mensagens Comuns

### Erro: Arquivo não encontrado
```
✗ Erro: Arquivo não encontrado: input.xlsx
```
**Solução**: Verifique o caminho e nome do arquivo

### Erro: Coluna obrigatória ausente
```
ValueError: Coluna 'keyword' obrigatória
```
**Solução**: Adicione a coluna `keyword` ao arquivo

### Erro: Keyword vazio
```
ValueError: Coluna 'keyword' contém valores vazios
```
**Solução**: Remova linhas com keywords vazias

### Aviso: Código inválido
```
⚠️  Aviso: Código geo 'XX' pode não ser válido
⚠️  Aviso: Código de linguagem 'xx' pode não ser válido
```
**Ação**: Processamento continua, verifique o código

### Erro: Rate Limiting do Google
```
Google Trends Error: 429 (Too Many Requests)
```
**Solução**: Aguarde 15-30 minutos antes de tentar novamente

### Erro: Wikipedia não encontrado
```
⚠️  Wikipedia API Error: 404
```
**Causa**: Artigo não existe nesse idioma
**Ação**: Tente outro keyword ou verifique o nome

## 📊 Resumo da Execução

Ao final, o script exibe:
```
============================================================
✓ RELATÓRIO CONCLUÍDO
============================================================
Keywords processadas: 3/4

⚠️  1 erros encontrados:
  - Google Trends Error (dengue): 429 Too Many Requests

📊 Arquivo de saída: output/trends_report.xlsx
```

## 🔧 Performance

- **Tempo por keyword**: 10-30 segundos (depende das APIs)
- **Limite de requisições**: ~100 requisições/hora (Google Trends rate limit)
- **Timeout de requisição**: 10 segundos
- **Tamanho do Excel**: ~50-150 KB por keyword

## 📌 Dicas Importantes

1. **Rate Limiting**: Google Trends tem limite de requisições. Se processar muitos keywords de uma vez, aguarde entre execuções.

2. **Nome de Abas**: Excel limita nome de abas a 31 caracteres. Keywords muito longos são truncados automaticamente.

3. **Gráficos**: Todos os gráficos estão embutidos no Excel (não são links externos).

4. **Idiomas**: Wikipedia usa códigos de dois dígitos. Nem todo keyword existe em todos os idiomas.

5. **Sem Dados**: Se Google Trends retornar dados insuficientes, as tabelas ficarão vazias (não é erro).

## 🆘 Troubleshooting

### Script não encontra venv
```bash
source venv/bin/activate
```

### Permissão negada ao salvar
```bash
chmod +x execution/trends_tool_batch.py
```

### Excel corrompido
- Tente novamente com menos keywords
- Verifique se há espaço em disco

### Imagens não aparecem no Excel
- Verifique se a pasta `output/` tem permissão de escrita
- Reinicie o Excel se já estiver aberto

## 📚 Próximas Etapas

- Adicionar filtros e agregações no Excel
- Suporte a múltiplas planilhas de saída
- Export em outros formatos (PDF, HTML)
- Dashboard interativo

---

**Versão**: 1.0  
**Data**: Fevereiro 2026  
**Status**: ✅ Testado e funcionando
