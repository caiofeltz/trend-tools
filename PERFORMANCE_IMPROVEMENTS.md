# 🚀 Melhorias de Performance - Rate Limiting 429

## Problema Original

Estava recebendo erros **429 (Too Many Requests)** do Google Trends durante processamento em batch.

---

## Soluções Implementadas

### 1. **Retry com Backoff Exponencial**

```
Tentativa 1: 3-6 segundos
Tentativa 2: 6-10 segundos (2^1 × base)
Tentativa 3: 12-14 segundos (2^2 × base)
```

**Código:**
```python
delay = base_delay * (2 ** attempt) + random.uniform(0, 2)
```

### 2. **Delays Adaptativos Entre Keywords**

Cada keyword recebe delay baseado em sua posição na fila:

```
Keyword 1: 2-5 segundos
Keyword 2: 2.5-5.5 segundos
Keyword 3: 3-6 segundos
Keyword 4: 3.5-6.5 segundos
...
```

**Código:**
```python
base_delay = 2 + (keyword_index * 0.5)
total_delay = base_delay + random.uniform(1, 3)
```

### 3. **Delays Entre Requisições Internas**

Google Trends é chamado 2 vezes por keyword:
- `interest_over_time()` 
- `interest_by_region()`

Agora há **1-2 segundos** de delay entre elas.

### 4. **HTTP Session com Retry Strategy**

Configurado HTTP adapter com retry automático:

```python
retry_strategy = Retry(
    total=2,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
```

### 5. **Timeouts Realistas**

- Google Trends: **15 segundos**
- Wikipedia: **15 segundos**
- Evita erros de timeout

### 6. **User-Agent Realista**

Mudado de `TrendTool/1.0` para navegador real:

```python
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```

### 7. **Detecção Inteligente de Erros**

Diferencia entre:
- **Rate limit (429)** → Retry com delay exponencial
- **Timeout** → Retry simples
- **Arquivo não encontrado (404)** → Skip silencioso
- **Outros erros** → Log e continua

---

## Fluxo Otimizado

```
Início: 5 keywords

Keyword 1 (índice 0)
├─ Nenhum delay (primeiro)
├─ Google Trends: retry automático + 1-2s entre chamadas
└─ Wikipedia: retry automático

[Delay adaptativo: 2-5s]

Keyword 2 (índice 1)
├─ Delay: 2.5-5.5s
├─ Google Trends: retry automático + 1-2s entre chamadas
└─ Wikipedia: retry automático

[Delay adaptativo: 3-6s]

Keyword 3 (índice 2)
... (aumenta delay progressivamente)
```

---

## Benefícios

✅ **Reduz Erros 429**
- Backoff exponencial dá tempo aos servidores
- Delays entre requisições evitam picos

✅ **Autorresiliente**
- Retry automático para falhas temporárias
- Não interrompe processamento

✅ **Adaptável**
- Delay aumenta conforme progride o batch
- Melhor para batches grandes (10+ keywords)

✅ **Informativo**
- Mostra tentativas de retry
- Log claro de delays

✅ **Robusto**
- Tratamento específico de cada tipo de erro
- Wikipedia com fallback

---

## Timing Esperado

### Antes (sem otimizações)
```
5 keywords × 5 segundos/keyword = 25 segundos
❌ Taxa alta de 429 errors
```

### Depois (com otimizações)
```
5 keywords:
  - Keyword 1: 0s (sem delay inicial)
  - Keyword 2: +3s (delay)
  - Keyword 3: +5s (delay maior)
  - Keyword 4: +6s (delay maior ainda)
  - Keyword 5: +7s (delay máximo)
  
Total: ~25-30 segundos
✅ Taxa muito reduzida de 429 errors
```

---

## Configurações Tuneáveis

Se ainda receber 429, você pode ajustar em:
**`execution/trends_tool_batch.py`**

### Para aumentar delays:
```python
# Linha ~125
base_delay = 3  # Aumentar de 3 para 5
```

### Para mais tentativas:
```python
# Linha ~116
max_retries = 3  # Aumentar para 4 ou 5
```

### Para maior delay por keyword:
```python
# Linha ~313
base_delay = 2 + (keyword_index * 0.5)  # Aumentar multiplicador
```

---

## Logs Durante Execução

Você verá algo assim:

```
📂 Lendo arquivo: keywords.csv
✓ Validando dados...
✓ 5 keywords para processar

📊 Processando (1/5): Python
  → Buscando Google Trends: Python (geo=BR, timeframe=today 12-m)
  ✓ Google Trends obtido com sucesso
  → Buscando Wikipedia: Python (pt)
  ✓ Wikipedia obtido com sucesso
✓ Keyword processada com sucesso

⏳ Aguardando 3.2s para evitar rate limit...

📊 Processando (2/5): Django
  → Buscando Google Trends: Django (geo=BR, timeframe=today 12-m)
  ⚠️ Rate limit (429) detectado! Aguardando antes de nova tentativa...
  ⏳ Tentativa 2/3 (aguardando 6.3s)...
  ✓ Google Trends obtido com sucesso
  → Buscando Wikipedia: Django (pt)
  ✓ Wikipedia obtido com sucesso
✓ Keyword processada com sucesso

... (continua com delays progressivos)
```

---

## Recomendações

### Para 5-10 keywords
- ✅ Configuração padrão funciona bem
- Tempo: ~30-45 segundos

### Para 10-50 keywords
- ⚠️ Considere aumentar `base_delay` para 4-5
- Considere aumentar `max_retries` para 4
- Tempo: ~1-3 minutos

### Para 50+ keywords
- ⚠️ Processar em **múltiplas execuções** (10-20 keywords cada)
- Aguardar 5-10 minutos entre execuções
- Ou solicitar acesso direto à API do Google

---

## Testing

Para testar com retry:

```python
from execution.trends_tool_batch import TrendsBatchAnalyzer

# Criar CSV com 1 keyword
# Executar durante pico de uso (para aumentar chance de 429)

analyzer = TrendsBatchAnalyzer()
results = analyzer.process_batch('test.csv')

# Verificar se recuperou do erro 429
for r in results:
    if r['success']:
        print(f"✅ {r['keyword']} processado com sucesso")
    else:
        print(f"❌ {r['keyword']} falhou")
```

---

## Próximas Melhorias (Futuro)

- [ ] Cache de resultados para evitar re-requisições
- [ ] Processamento em paralelo com rate limiting inteligente
- [ ] Usar proxy rotativo (se disponível)
- [ ] API oficial do Google Trends (requer chave)
- [ ] Database para armazenar dados brutos

---

## Resumo

| Aspecto | Antes | Depois |
|--------|-------|--------|
| Delays | Nenhum | Adaptativo + Backoff |
| Retry | Nenhum | 3 tentativas automáticas |
| Rate Limit | Falha | Recuperação automática |
| Timeout | Falha | Retry e fallback |
| User-Agent | TrendTool | Realista (navegador) |
| Robutez | Baixa | Alta |

---

**Data**: 20 de Fevereiro de 2026  
**Status**: ✅ Implementado e Testado  
**Versão**: 2.0
