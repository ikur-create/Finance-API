# Monte Carlo Gold — Simulación de Regímenes del Oro
## ¿Qué hace este proyecto?

Este modelo de simulación estocástica descarga datos históricos reales del precio del oro, analiza su distribución empírica y simula miles de trayectorias futuras posibles usando **Monte Carlo por bootstrap no paramétrico**, con soporte para fat tails.

A diferencia de los modelos clásicos que asumen distribución normal, este enfoque **resamplea directamente los retornos históricos observados**, capturando automáticamente:

- **Fat tails** — eventos extremos más frecuentes de lo que predice una gaussiana
- **Asimetría** — el oro cae más bruscamente de lo que sube
- **Clústeres de volatilidad** — periodos de alta y baja turbulencia

---

## Outputs del modelo

### Análisis estadístico
| Métrica | Descripción |
|---|---|
| Media / Volatilidad diaria | Retorno esperado y dispersión histórica |
| Skewness | Asimetría de la distribución de retornos |
| Curtosis en exceso | Indicador de fat tails (normal = 0) |
| VaR 95% | Pérdida máxima esperada el 95% de los días |
| CVaR 95% | Pérdida promedio en el 5% peor de los días |
| Sharpe anualizado | Retorno ajustado por riesgo |

### Frecuencia de movimientos
Cuenta cuántos días históricos el oro subió o bajó un ±1%, ±2%, ±5%, ±10%, ±15%, ±20%.

### Simulación Monte Carlo
- **N trayectorias** proyectadas al horizonte elegido
- **Percentiles P1–P99** del precio futuro
- Probabilidad de ganancia, pérdida >20%, ganancia >20%

### Visualizaciones (7 gráficos)
1. Precio histórico del oro
2. Histograma de retornos vs. distribución normal teórica
3. Frecuencia de movimientos por umbral
4. QQ-Plot (visualización de fat tails)
5. Volatilidad rodante 21 días anualizada
6. Trayectorias Monte Carlo con bandas de percentiles
7. Distribución del precio final simulado

---

## Instalación y uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/monte-carlo-gold.git
cd monte-carlo-gold
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
python mc_oro.py
```

El gráfico se guarda automáticamente como `monte_carlo_oro.png`.

---

## Configuración

Edita los parámetros al final de `mc_oro.py`:

```python
TICKER          = "GC=F"       # Futuros oro COMEX. Alternativas: "GLD", "IAU"
FECHA_INICIO    = "2010-01-01" # Inicio del histórico
N_SIMULACIONES  = 1000         # Número de trayectorias
HORIZONTE_DIAS  = 252          # 252 días ≈ 1 año bursátil
SEED            = 42           # Reproducibilidad
```

### Tickers compatibles
| Ticker | Descripción |
|---|---|
| `GC=F` | Futuros del oro COMEX *(recomendado)* |
| `GLD` | ETF SPDR Gold Shares |
| `IAU` | ETF iShares Gold Trust |

---

## Metodología

### ¿Por qué bootstrap en lugar de distribución normal?

El modelo clásico de Black-Scholes asume retornos normalmente distribuidos. Los mercados reales no lo son:

```
Curtosis empírica del oro (2010–2026): ~9.1
Curtosis de una distribución normal:    3.0
```

Un modelo gaussiano **infraestima** la probabilidad de eventos extremos. El bootstrap resuelve esto sin necesidad de asumir ninguna distribución: simplemente sortea retornos del pasado.

### Proceso de simulación

```
Para cada trayectoria p = 1..N:
  1. Sortear aleatoriamente 'horizonte' retornos del histórico real
  2. Precio_t = Precio_0 × exp( Σ log-retornos sorteados )
  3. Registrar precio final
→ Calcular percentiles sobre todas las trayectorias
```

### Retornos logarítmicos

Se usan retornos logarítmicos `r_t = ln(P_t / P_{t-1})` en lugar de aritméticos porque son **aditivos en el tiempo** y más estables numéricamente en horizontes largos.

---
## 📈 Ejemplo de resultados

Con datos del oro desde 2010 hasta 2026 y un horizonte de 252 días:

```
🎯 DISTRIBUCIÓN DEL PRECIO FINAL SIMULADO
  P5  (bajista extremo) :  $4,189  (-18%)
  P25                   :  $4,987   (-2%)
  Mediana               :  $5,543   (+8%)
  P75                   :  $6,269  (+23%)
  P95 (alcista extremo) :  $7,320  (+43%)

  Prob. de ganancia  : 69.4%
  Prob. pérdida >20% :  3.4%
  Prob. ganancia >20%: 28.2%
```

---

## Disclaimer

Este proyecto es exclusivamente de carácter **educativo y de investigación**. No constituye asesoramiento financiero ni recomendación de inversión. Los resultados de simulaciones pasadas no garantizan rendimientos futuros.
