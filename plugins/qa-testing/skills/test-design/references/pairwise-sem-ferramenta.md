# Pairwise sem ferramenta externa

Apoio da skill `test-design`. Use quando há vários parâmetros independentes (navegador, SO, idioma, plano, perfil) e o produto cartesiano é grande demais. Pairwise garante que todo **par de valores** aparece em algum caso; estudos do NIST citados no brain indicam que a maioria das falhas é disparada por um ou dois parâmetros (Inferido, não reverificado). Quando o risco justifica, suba para 3-wise.

Quando não usar: os parâmetros interagem por regra de negócio (use tabela de decisão) ou o produto cartesiano cabe no tempo (execute tudo).

## Gerador em Python (biblioteca padrão)

Algoritmo guloso simples: a cada rodada escolhe o caso do produto cartesiano que cobre mais pares ainda descobertos. Não garante o mínimo absoluto de linhas, mas dá resultados próximos para o uso comum. Percorre o produto inteiro, então serve para até algumas dezenas de milhares de combinações; acima disso use uma ferramenta dedicada (por exemplo PICT da Microsoft ou ACTS do NIST, a instalar por conta do usuário; comandos Não verificáveis aqui).

Salve como `pairwise.py` fora do código de produção. Autoria própria desta fábrica, MIT; testado em Python 3.14 em 2026-10-10.

```python
"""Gerador guloso de casos par-a-par (stdlib).
Uso: python pairwise.py navegador=chrome,firefox,safari so=windows,macos idioma=pt,en"""
import itertools
import sys


def proibido(caso):
    # Restrição de exemplo: Safari só no macOS. Edite conforme o seu domínio.
    return caso.get("navegador") == "safari" and caso.get("so") == "windows"


def pairwise(params):
    nomes = list(params)
    faltam = {
        ((a, va), (b, vb))
        for a, b in itertools.combinations(nomes, 2)
        for va in params[a]
        for vb in params[b]
        if not proibido({a: va, b: vb})
    }
    casos = []
    while faltam:
        melhor, ganho_melhor = None, -1
        for combo in itertools.product(*(params[n] for n in nomes)):
            caso = dict(zip(nomes, combo))
            if proibido(caso):
                continue
            ganho = sum(
                1 for a, b in itertools.combinations(nomes, 2)
                if ((a, caso[a]), (b, caso[b])) in faltam
            )
            if ganho > ganho_melhor:
                melhor, ganho_melhor = caso, ganho
        casos.append(melhor)
        for a, b in itertools.combinations(nomes, 2):
            faltam.discard(((a, melhor[a]), (b, melhor[b])))
    return casos


if __name__ == "__main__":
    params = {}
    for arg in sys.argv[1:]:
        nome, _, valores = arg.partition("=")
        params[nome] = valores.split(",")
    for i, caso in enumerate(pairwise(params), 1):
        print(i, *[f"{k}={v}" for k, v in caso.items()])
```

## Resultado observado

```text
$ python pairwise.py navegador=chrome,firefox,safari so=windows,macos idioma=pt,en
1 navegador=chrome so=windows idioma=pt
2 navegador=chrome so=macos idioma=en
3 navegador=firefox so=windows idioma=en
4 navegador=firefox so=macos idioma=pt
5 navegador=safari so=macos idioma=pt
6 navegador=safari so=macos idioma=en
```

Seis casos cobrem todos os pares possíveis (o produto cartesiano são 12; a restrição elimina Safari no Windows). Com quatro parâmetros de três valores (81 combinações), o mesmo script gerou 9 casos.

## Restrições e riscos conhecidos

1. A função `proibido` precisa listar todas as combinações impossíveis; sem ela, pares impossíveis entram no plano. Pares impossíveis são removidos da meta de cobertura, o que mantém o laço terminando.
2. Pairwise não sabe o que é arriscado: acrescente à mão combinações de risco conhecido (o navegador mais usado com o idioma que mais gera suporte).
3. Não prova nada sobre interações de três ou mais parâmetros; para configuração crítica, peça 3-wise a uma ferramenta dedicada.
4. Confira o resultado: para cada par de valores aceitável, ao menos uma linha o contém. Um script de conferência de cinco linhas com `itertools.combinations` basta; se o conjunto de casos foi editado à mão, rode a conferência de novo.
5. Registre no plano que a técnica é pairwise e quais combinações foram acrescentadas por risco.
