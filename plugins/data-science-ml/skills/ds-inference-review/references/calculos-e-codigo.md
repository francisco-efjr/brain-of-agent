# Cálculos e código para revisão de inferência

Validado em 2026-10-10. Redação própria; fórmulas de conhecimento estatístico estável (Inferido) e estrutura de V-26/V-27 (pitcany e K-Dense, MIT, destiladas). As contas de exemplo (SRM = 25,6; 1 − 0,95²⁰ ≈ 0,64; n por braço ≈ 15,7·σ²/δ² para α = 0,05 e poder 80%) foram conferidas por cálculo direto em 2026-10-10; o restante do código não foi executado no plugin (Não verificado). Confira versões: `pip show scipy statsmodels` (o `confidence_interval()` do `ttest_ind` existe no SciPy 1.10+).

## Sumário
1. SRM
2. Diferença de médias com IC (Welch) e tamanho de efeito
3. Diferença de proporções com IC
4. MDE e tamanho de amostra
5. Clusters: DEFF
6. Multiplicidade: Holm, Bonferroni, BH
7. CUPED
8. Bootstrap (quando o pressuposto do teste é duvidoso)
9. Probabilidade de falso positivo na família

## 1. SRM

```python
from scipy.stats import chisquare

obs = [50800, 49200]                 # usuários por braço (controle, variante)
plan = [0.5, 0.5]                    # razão planejada
exp = [sum(obs) * p for p in plan]
stat, p = chisquare(obs, f_exp=exp)
print(round(stat, 2), p)             # 25.6, p ~ 4.2e-07 -> sinaliza (convenção: p < 0.001)
```

Se sinalizar, **não leia o resto**: investigue atribuição, filtros assimétricos, bots, redirecionamento, falha de log. Teste SRM em cada recorte relevante (plataforma, país) para localizar a origem. Com mais de dois braços, use as mesmas contagens e razões; `chisquare` aceita vetores de qualquer tamanho.

## 2. Diferença de médias com IC (Welch) e tamanho de efeito

```python
import numpy as np
from scipy import stats

a, b = np.asarray(control), np.asarray(variant)
res = stats.ttest_ind(b, a, equal_var=False)            # Welch
ci = res.confidence_interval(confidence_level=0.95)     # SciPy >= 1.10: IC da diferença (b - a)
diff = b.mean() - a.mean()

sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
d = diff / sp                                            # d de Cohen
g = d * (1 - 3 / (4 * (len(a) + len(b)) - 9))            # Hedges' g (correção de viés para n pequeno)
print(f"n={len(a)}/{len(b)} média={a.mean():.3f}/{b.mean():.3f} DP={a.std(ddof=1):.3f}/{b.std(ddof=1):.3f}")
print(f"t={res.statistic:.3f} gl={res.df:.1f} p={res.pvalue:.4g} dif={diff:.3f} IC95=[{ci.low:.3f}, {ci.high:.3f}] g={g:.2f}")
```

Relate p **exato** (não "p < 0,05"). Se a métrica é muito assimétrica (receita por usuário), o IC da diferença de médias por Welch pode ser instável com n pequeno: use bootstrap (seção 8) e diga qual foi usado.

## 3. Diferença de proporções com IC

```python
def two_prop_ci(x1, n1, x0, n0, z=1.96):
    p1, p0 = x1 / n1, x0 / n0
    se = np.sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
    d = p1 - p0
    return d, d - z * se, d + z * se        # Wald; com contagens pequenas prefira Newcombe (statsmodels)

d, lo, hi = two_prop_ci(x1=2310, n1=50800, x0=2150, n0=49200)   # exemplo ilustrativo
```

`statsmodels.stats.proportion.confint_proportions_2indep(count1, nobs1, count2, nobs2, method="newcomb")` dá um IC melhor para contagens pequenas (confira a assinatura na versão instalada). Teste de duas proporções: `statsmodels.stats.proportion.proportions_ztest`.

## 4. MDE e tamanho de amostra

```python
from scipy.stats import norm

def mde_means(sigma, n_per_arm, alpha=0.05, power=0.80):
    """Menor diferença de médias detectável (bilateral, duas amostras independentes)."""
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    return (za + zb) * sigma * np.sqrt(2 / n_per_arm)

def n_per_arm_means(sigma, delta, alpha=0.05, power=0.80):
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    return 2 * (sigma * (za + zb) / delta) ** 2     # ~ 15,7 * sigma^2 / delta^2  (aprox. 16)

def n_per_arm_props(p_base, delta, alpha=0.05, power=0.80):
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    p_bar = p_base + delta / 2
    return 2 * p_bar * (1 - p_bar) * ((za + zb) / delta) ** 2
```

Compare o MDE com o **menor efeito que vale lançar**. Se MDE > efeito de interesse, o teste não tem poder para ele: aumente n, reduza variância (CUPED, métrica menos ruidosa) ou aceite que será inconclusivo. Regra de bolso (Inferido): n por braço ≈ 16·σ²/δ².

## 5. Clusters: DEFF

```python
def deff(m, icc):               # m = tamanho médio do cluster
    return 1 + (m - 1) * icc

n_eff = n_total / deff(m=25, icc=0.05)    # ex.: DEFF = 2,2 -> o n efetivo cai mais da metade
```

Se a randomização é por cluster (loja, cidade, sessão), a análise precisa respeitar o cluster (erro-padrão agrupado ou modelo misto). Com poucos clusters (por exemplo, 3 tratados), o erro-padrão robusto é instável e a inferência paramétrica é frágil: use permutação/placebo entre clusters e fale com cautela.

## 6. Multiplicidade: Holm, Bonferroni, BH

```python
from statsmodels.stats.multitest import multipletests

pvals = [0.003, 0.012, 0.03, 0.04, 0.20]        # família confirmatória declarada ANTES de olhar
rej_h, p_holm, _, _ = multipletests(pvals, alpha=0.05, method="holm")
rej_b, p_bonf, _, _ = multipletests(pvals, alpha=0.05, method="bonferroni")
rej_f, p_bh,   _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")   # triagem exploratória
```

Família confirmatória: Holm (mais poderoso que Bonferroni, mesmo controle de FWER) ou Bonferroni. BH controla a taxa de descobertas falsas (FDR): serve para triagem exploratória, não para afirmar claims confirmatórios. Defina a família antes dos resultados.

## 7. CUPED

```python
def cuped(y, x_pre):
    """Ajusta y usando covariável pré-exposição x_pre (mesma unidade, medida ANTES da randomização)."""
    theta = np.cov(y, x_pre, ddof=1)[0, 1] / np.var(x_pre, ddof=1)
    return y - theta * (x_pre - x_pre.mean()), theta

y_adj, theta = cuped(y_all, x_pre_all)           # calcule theta nos dois braços juntos
# redução esperada da variância ~ rho^2 (correlação entre y e x_pre ao quadrado)
```

Condição: a covariável deve ser medida antes da exposição e não pode ser afetada pelo tratamento. Use o mesmo `theta` nos dois braços, estimado com os dados combinados; analise `y_adj` com o mesmo teste da seção 2.

## 8. Bootstrap

```python
rng = np.random.default_rng(42)
B = 10_000
diffs = np.empty(B)
for i in range(B):
    diffs[i] = rng.choice(b, size=len(b)).mean() - rng.choice(a, size=len(a)).mean()
lo, hi = np.percentile(diffs, [2.5, 97.5])       # IC percentil da diferença de médias
```

Com unidade de randomização diferente do usuário (por exemplo, loja), reamostre a unidade de randomização (cluster bootstrap), não as linhas. Declare B, seed e método.

## 9. Probabilidade de falso positivo na família

```python
k, alpha = 20, 0.05
print(1 - (1 - alpha) ** k)      # 0.6415: 20 testes independentes a 5% -> ~64% de ao menos um falso positivo
```

Vale para testes independentes; com dependência o número muda, mas a lição se mantém: conte toda a família (métricas × variantes × segmentos × olhadas) e corrija a parte confirmatória.
