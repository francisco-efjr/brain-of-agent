# Docstrings e comentários de documentação por linguagem

Conteúdo: 1 regra geral · 2 Python · 3 TypeScript e JavaScript · 4 Rust · 5 Java · 6 versões e onde conferir.

Fontes (redação própria; licenças limitam a cópia): PEP 257 (domínio público), guia de Python do Google seção 3.8 (CC-By 3.0 no README do repositório), documentação do `doctest` (PSF v2; exemplos 0BSD), JSDoc (CC BY-SA 3.0, destilar), TSDoc (sem licença declarada, destilar), Rustdoc (licença não declarada, destilar), Javadoc do JDK 21 (Oracle, destilar). Itens V-33 a V-36. Rótulo: Verificado nas fontes; onde indicado, Inferido.

## 1. Regra geral

Documente o que a assinatura e os tipos não dizem: comportamento não óbvio, unidades, restrições, efeitos colaterais, erros da interface. O guia já adotado pelo projeto vence. Todo exemplo de documentação pública é teste. Atualize a docstring no mesmo commit que o código.

## 2. Python

### Regras (Google 3.8 + PEP 257)

- Aspas triplas `"""`; resumo em **uma linha física de até 80 caracteres** terminando em ponto (ou `?`/`!`), linha em branco, descrição.
- Seções: `Args` (nome: descrição; tipos só se não houver anotação), `Returns` ou `Yields` (omitir se só retorna `None`), `Raises` (só as da interface), `Attributes` (classes).
- PEP 257: forma imperativa ("Converte..."); Google aceita terceira pessoa. Siga o projeto; sem guia, Google com seções e registre a escolha.
- Linha em branco depois da docstring de **classe**.
- `Examples:` com `>>> ` é convenção de Napoleon/Sphinx (Inferido; não consta na lista de seções de V-33).

### Exemplo (executado na construção)

Arquivo `duracao.py`; comando `python -I -m doctest -v duracao.py` rodado em Python 3.14.4 local, resultado: 3 testes, 3 passaram. O exemplo é ilustrativo para o seu projeto; reexecute no ambiente dele.

```python
import re

_PADRAO = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")


def parse_duration(texto: str) -> int:
    """Converte uma duração como "1h30m" em segundos.

    Aceita horas (h), minutos (m) e segundos (s), nessa ordem; cada parte é
    opcional, mas ao menos uma deve estar presente.

    Args:
        texto: Duração textual, por exemplo "1h30m", "45s" ou "2h".

    Returns:
        Total de segundos.

    Raises:
        ValueError: Se o texto estiver vazio ou não seguir o formato.

    Examples:
        >>> parse_duration("1h30m")
        5400
        >>> parse_duration("45s")
        45
        >>> parse_duration("abc")
        Traceback (most recent call last):
            ...
        ValueError: formato inválido: 'abc'
    """
    correspondencia = _PADRAO.fullmatch(texto)
    if not texto or correspondencia is None:
        raise ValueError(f"formato inválido: {texto!r}")
    horas, minutos, segundos = (int(parte or 0) for parte in correspondencia.groups())
    return horas * 3600 + minutos * 60 + segundos
```

Pontos a notar: o resumo (48 caracteres) não repete a assinatura; `Raises` lista só o `ValueError` da interface, não `TypeError` por passar `None`; a mensagem do traceback é literal e precisa bater.

### Doctest, o essencial

- Prompt `>>> ` e continuação `... `; a saída esperada vem na linha seguinte até a próxima `>>> ` ou linha em branco; `<BLANKLINE>` representa linha em branco na saída.
- Traceback: compara tipo e mensagem da exceção final; as linhas intermediárias podem ser `...`.
- Rodar: `python -I -m doctest -v arquivo.py` (executa o código de topo do módulo). `-I` isola de `PYTHONPATH` e do diretório atual, útil ao testar código recebido de terceiros. Pytest: `--doctest-modules` (Inferido).

## 3. TypeScript e JavaScript

### TSDoc (conferir se as ferramentas do projeto leem TSDoc ou JSDoc)

- Tipos já estão no código: `@param nome - descrição` (hífen é a sintaxe do TSDoc) e `@returns` só para o que o tipo não diz.
- `@example` para uso, `@deprecated` com a alternativa, `@typeParam` para genéricos, `@throws` para exceções da interface, `@remarks` para detalhe longo.

```ts
/**
 * Calcula o desconto aplicável ao carrinho.
 *
 * @param carrinho - Itens e cupom; valores em centavos.
 * @returns Desconto em centavos; `0` quando o cupom é inválido ou expirou.
 * @example
 * ```ts
 * calcularDesconto({ itens: [{ preco: 10000 }], cupom: "BEMVINDO10" }); // 1000 (ilustrativo)
 * ```
 * @deprecated Use {@link calcularDescontoComFrete} quando houver frete.
 */
export function calcularDesconto(carrinho: Carrinho): number {
```

O exemplo é ilustrativo e **não executado**: nomes e valores são fictícios.

### JSDoc (JavaScript sem TypeScript)

- O bloco precisa começar com `/**` (`/*` e `/***` são ignorados).
- `@param {string} titulo - Título do livro.` com tipo entre chaves (só quando não há TypeScript), `@returns {number} ...`.

## 4. Rust

- `///` documenta o item seguinte; `//!` documenta o módulo ou crate. O texto antes da primeira linha em branco vira o resumo nas buscas.
- Seção `# Examples` com bloco copiável; blocos sem linguagem são Rust e **são compilados e executados** por `cargo test --doc`; passa se compila e roda sem panic.
- Atributos de bloco: `no_run` (compila, não roda: rede, efeitos externos), `ignore` (só com motivo entre parênteses), `should_panic`, `compile_fail`, `edition2024` etc.
- Linhas começando com `# ` ficam ocultas na documentação e são compiladas.
- Seções `# Errors` e `# Panics` são convenção da comunidade (Inferido, fora das páginas lidas).

```rust
/// Converte uma duração como `1h30m` em segundos.
///
/// # Errors
///
/// Retorna `Err` se o texto não seguir o formato.
///
/// # Examples
///
/// ```
/// let segundos = meu_crate::parse_duration("1h30m")?;
/// assert_eq!(segundos, 5400);
/// # Ok::<(), meu_crate::Erro>(())
/// ```
pub fn parse_duration(texto: &str) -> Result<u64, Erro> {
```

Nome do crate e tipo `Erro` são ilustrativos; o exemplo **não foi compilado** (sem toolchain Rust na construção). Comando: `cargo test --doc`.

## 5. Java (Javadoc)

- Primeira frase da descrição é o resumo; `@param` por parâmetro e por tipo genérico; `@return`; `@throws` (preferido a `@exception`); `@since` em API pública nova; HTML 5.
- `{@return ...}` em linha vale desde o JDK 16; antes disso use o bloco `@return`.

```java
/**
 * Converte uma duração textual em segundos.
 *
 * @param texto duração no formato {@code 1h30m}
 * @return total de segundos
 * @throws IllegalArgumentException se o formato for inválido
 * @since 1.2
 */
public static int parseDuration(String texto)
```

Exemplo ilustrativo; **não compilado**. Gere a doc com a ferramenta do projeto (`javadoc`, Maven ou Gradle) e proponha o comando ao usuário.

## 6. Versões e onde conferir

| Item | Onde conferir | Observação |
| --- | --- | --- |
| Python | https://docs.python.org/3/library/doctest.html | página lida cobre 3.15.0 (V-33) |
| Guia Google Python | https://google.github.io/styleguide/pyguide.html | seção 3.8 |
| PEP 257 | https://peps.python.org/pep-0257/ | |
| TSDoc | https://tsdoc.org/ | descrito como proposta |
| JSDoc | https://jsdoc.app/ | |
| Rustdoc | https://doc.rust-lang.org/rustdoc/ | páginas citam edições; confira `rustc --version` |
| Javadoc | https://docs.oracle.com/en/java/javase/21/docs/specs/javadoc/doc-comment-spec.html | JDK 21; JDK mais novo: não verificado |
