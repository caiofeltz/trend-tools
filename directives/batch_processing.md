# Batch Processing with Spreadsheet Input

## Objetivo
Processar múltiplas keywords a partir de uma planilha (Excel ou CSV) e gerar um relatório consolidado em Excel com gráficos e dados de cada keyword.

## Inputs

### Arquivo de Entrada Obrigatório
- **Formato**: `.xlsx` ou `.csv`
- **Coluna Obrigatória**: `keyword`
- **Colunas Opcionais**:
  - `geo`: Código da região (padrão: `BR`)
  - `timeframe`: Período de análise (padrão: `today 12-m`)
  - `language`: Código de linguagem Wikipedia (padrão: `pt`)

### Valores Padrão
Se a coluna não for fornecida ou tiver valor vazio:
- **geo**: `BR` (Brasil)
- **timeframe**: `today 12-m` (últimos 12 meses)
- **language**: `pt` (português)

### Formatos Aceitos

#### Geo (Códigos de Região)
- `BR` - Brasil
- `US` - Estados Unidos
- `MX` - México
- `GB` - Reino Unido
- `DE` - Alemanha
- `FR` - França
- `IT` - Itália
- `ES` - Espanha
- `JP` - Japão
- `CN` - China
- `IN` - Índia
- `AU` - Austrália
- `CA` - Canadá
- `AR` - Argentina
- `PT` - Portugal

#### Timeframe (Períodos)
- `today 1-m` - Último mês
- `today 3-m` - Últimos 3 meses
- `today 12-m` - Últimos 12 meses
- `2024-01-01 2024-12-31` - Período específico (formato YYYY-MM-DD)

#### Language (Códigos Wikipedia)
- `pt` - Português
- `en` - Inglês
- `es` - Espanhol
- `fr` - Francês
- `de` - Alemão
- `it` - Italiano
- `ja` - Japonês
- `zh` - Chinês
- `ru` - Russo
- `ar` - Árabe
- `hi` - Hindi

## Validações Implementadas

1. **Validação de Schema**:
   - Verifica existência de coluna `keyword`
   - Detecta valores vazios em keywords
   - Normaliza nomes de colunas (lowercase, sem espaços)

2. **Valores Padrão**:
   - Aplica defaults automáticos para colunas vazias
   - Remove espaçamento em branco das entradas

3. **Validação de Códigos**:
   - Valida códigos de região (geo)
   - Valida códigos de linguagem
   - Emite avisos para códigos inválidos (não interrompe o processamento)

4. **Tratamento de Erros**:
   - Continua processamento mesmo com falhas em uma keyword
   - Registra erros em lista para relatório final
   - Exibe mensagens descritivas durante a execução

## Outputs

### Arquivo Principal
- **Nome**: `trends_report.xlsx` (personalizável com `-o`)
- **Local**: `output/` directory
- **Formato**: Excel com múltiplas abas

### Estrutura do Excel
Cada keyword tem sua própria aba com:

1. **Header com Parâmetros**:
   - Nome do keyword
   - Data/hora de geração
   - Parâmetros usados (geo, timeframe, language)

2. **Gráfico Dual-Axis**:
   - Google Trends (eixo esquerdo, azul)
   - Wikipedia Pageviews (eixo direito, laranja)
   - Incluído diretamente na planilha

3. **Tabela - Google Trends (Interesse ao Longo do Tempo)**:
   - Data
   - Valor de interesse (0-100)
   - Últimos 10 registros

4. **Tabela - Interesse por Região**:
   - Nome da região/estado
   - Interesse por região
   - Top 10 regiões ordenadas

5. **Tabela - Wikipedia Pageviews**:
   - Data
   - Número de visualizações
   - Últimos 10 registros

### Características do Relatório
- Formatação profissional com cores
- Gráficos de alta qualidade (600x400px)
- Headers com fundo colorido
- Largura de colunas otimizadas
- Dados apenas de keywords processadas com sucesso

## Uso

### Instalação de Dependências
```bash
pip install -r requirements.txt
```

### Uso Básico
```bash
python execution/trends_tool_batch.py input.xlsx
```

### Especificar Output
```bash
python execution/trends_tool_batch.py keywords.csv -o meu_relatorio.xlsx
```

## Exemplos de Arquivos de Entrada

### Exemplo 1: CSV Mínimo
```csv
keyword
Python
Dengue
```
Resultado: Todos com geo=BR, timeframe=today 12-m, language=pt

### Exemplo 2: CSV Completo
```csv
keyword,geo,timeframe,language
Python,BR,today 12-m,pt
Dengue,BR,today 12-m,pt
Machine Learning,US,2024-01-01 2024-12-31,en
```

### Exemplo 3: XLSX com Valores Parciais
| keyword | geo | language |
|---------|-----|----------|
| Python | | en |
| Dengue | BR | |

Resultado:
- Python: geo=BR, language=en, timeframe=today 12-m
- Dengue: geo=BR, language=pt, timeframe=today 12-m

## Tratamento de Erros

### Erros Comuns

**1. Arquivo não encontrado**
```
✗ Erro: Arquivo não encontrado: input.xlsx
```
Solução: Verifique o caminho e nome do arquivo

**2. Coluna 'keyword' ausente**
```
ValueError: Coluna 'keyword' obrigatória
```
Solução: Adicione a coluna 'keyword' ao arquivo

**3. Keyword com valor vazio**
```
ValueError: Coluna 'keyword' contém valores vazios
```
Solução: Remova linhas com keywords vazias

**4. Falha no Google Trends**
```
Google Trends Error: 429 (Too Many Requests)
```
Solução: Aguarde alguns minutos e tente novamente (rate limiting)

**5. Falha no Wikipedia**
```
Wikipedia API Error: 404
```
Solução: Nome do artigo não existe em Wikipedia no idioma especificado

## Resumo de Execução

Ao final do processamento, o script exibe:
```
============================================================
✓ RELATÓRIO CONCLUÍDO
============================================================
Keywords processadas: 4/4

📊 Arquivo de saída: output/trends_report.xlsx
```

Se houver erros:
```
⚠️  2 erros encontrados:
  - Google Trends Error (dengue): 429 Too Many Requests
  - Wikipedia Error (Python): No data found
```

## Performance

- **Tempo por keyword**: 10-30 segundos (depende de APIs)
- **Limite de requisições**: Google Trends tem rate limiting (~100 requisições/hora)
- **Timeout**: 10 segundos por requisição Wikipedia

## Notes

- Script respeita rate limiting das APIs
- Gráficos são gerados em memória e embutidos no Excel
- Execução contínua mesmo com falhas (robustez)
- Todos os erros são registrados para auditoria
