# Sinks de DOM, greps e correções seguras

Base: V-22 (OWASP, DOM-based XSS), V-19 (FE1 a FE8), V-59 (CSP e Trusted Types). Lista de sinks e regra "todo sink novo com dado externo vira achado" são destilação com redação própria. Padrões de busca são pistas: confirme lendo o arquivo (falso positivo é esperado).

## Sumário

1. Como buscar sem ruído
2. Sinks e padrões
3. Equivalentes seguros por framework
4. Sanitização de HTML
5. `postMessage`
6. Open redirect
7. Token e segredo

## 1. Como buscar sem ruído

- Use a ferramenta Grep com `glob` restrito ao código do projeto (por exemplo `src/**/*.{ts,tsx,js,jsx,vue,svelte,html}`). O ripgrep respeita `.gitignore`, que normalmente já exclui `node_modules`, `dist`, `.next` e `.nuxt`; confirme que o `.gitignore` do projeto os lista.
- Nunca rode em dependências: milhares de falsos positivos e nenhum código seu.
- Para cada ocorrência, registre `arquivo:linha`, o valor que chega ao sink e de onde ele vem. Sem origem, o item é "origem não determinada".

## 2. Sinks e padrões

Cada linha: sink, padrão (regex ripgrep) e o que confirmar.

- `innerHTML`, `outerHTML`: `\.(innerHTML|outerHTML)\s*=`. Valor vem de fora? Troque por `textContent` ou sanitize.
- `insertAdjacentHTML`, `document.write`: `insertAdjacentHTML\(|document\.write(ln)?\(`.
- Avaliação dinâmica de código: `\beval\(|new Function\(|set(Timeout|Interval)\(\s*['"\x60]`. `setTimeout` com string equivale a `eval`. Trocar por função.
- React: `dangerouslySetInnerHTML`.
- Vue: `v-html`. Svelte: `\{@html`. Angular: `bypassSecurityTrust(Html|Script|Style|Url|ResourceUrl)` e `\[innerHTML\]`.
- `srcdoc`, `DOMParser().parseFromString`, `iframe` com `src` de dado externo.
- Navegação: `(window\.)?location(\.href)?\s*=|location\.(assign|replace)\(` com valor derivado de parâmetro.
- `href`/`src` com URL de usuário: `href=\{[^}]*(url|link|href)`. O protocolo é permitido por allowlist (`http:`, `https:`, `mailto:`)? Bloqueie `javascript:` e `data:`.
- Mensagens entre janelas: `postMessage\(|addEventListener\(\s*['"]message['"]`.
- Armazenamento: `(localStorage|sessionStorage)\.(setItem|getItem)` perto de `token|jwt|session|secret|password`.
- Variáveis públicas: `NEXT_PUBLIC_|VITE_|NUXT_PUBLIC_|PUBLIC_` perto de `SECRET|KEY|TOKEN|PASSWORD|PRIVATE`.
- Merge profundo: `Object\.assign\(|_\.merge\(|merge\(|__proto__|constructor\.prototype`, com objeto vindo de JSON, URL ou formulário.
- Marcadores de Markdown: `marked\(|markdown-it|react-markdown|rehype-raw`. O renderizador converte para HTML? Houve sanitização depois? (`marked` não sanitiza a saída; `react-markdown` não renderiza HTML cru sem `rehype-raw`: conhecimento estável do ecossistema, Inferido; confirme na documentação da versão.)

## 3. Equivalentes seguros por framework

| Situação | Inseguro | Seguro |
| --- | --- | --- |
| Texto de usuário em React | `dangerouslySetInnerHTML={{ __html: texto }}` | `{texto}` (escapado pelo framework) |
| Texto de usuário em Vue | `<div v-html="texto">` | `{{ texto }}` |
| Texto de usuário em Svelte | `{@html texto}` | `{texto}` |
| Texto em DOM imperativo | `el.innerHTML = texto` | `el.textContent = texto` |
| HTML de terceiros que precisa ser HTML | injeção direta | sanitização contextual (seção 4), idealmente com Trusted Types |
| Angular | `bypassSecurityTrustHtml(dado)` | deixar o sanitizador embutido tratar `[innerHTML]`; contornar só com valor controlado por você |

## 4. Sanitização de HTML

```ts
import DOMPurify from 'dompurify';

// Permita só o que o produto precisa (exemplo: comentários com formatação básica).
const limpo = DOMPurify.sanitize(comentario.html, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'],
  ALLOWED_ATTR: ['href'],
});
```

```tsx
<div dangerouslySetInnerHTML={{ __html: limpo }} />
```

Pontos de revisão: a sanitização acontece o mais perto possível do sink, depois de qualquer transformação (sanitizar e depois concatenar reabre o risco); a lista de tags e atributos é explícita; links ganham verificação de protocolo; a sanitização do cliente não substitui a do servidor quando o HTML é armazenado e servido a outros clientes. Sanitizador não é sandbox (V-22). Com SSR, DOMPurify precisa de DOM: confirme como o projeto o usa no servidor (por exemplo com `jsdom` ou pacote isomórfico), pois a configuração varia (Não verificado aqui). Com Trusted Types, a política nomeada chama o sanitizador e o sink só aceita `TrustedHTML` (veja o bloco da skill).

## 5. `postMessage`

```ts
// Ruim: aceita mensagem de qualquer origem e age.
window.addEventListener('message', (e) => aplicarConfig(e.data));

// Bom: origem exata, formato validado, ação restrita.
const ORIGEM_ESPERADA = 'https://parceiro.exemplo.com';
window.addEventListener('message', (e) => {
  if (e.origin !== ORIGEM_ESPERADA) return;
  const dado = validarMensagem(e.data); // schema que rejeita o inesperado
  if (dado) aplicarConfig(dado);
});

// Envio de dado sensível: destino explícito, nunca '*'.
janelaFilha.postMessage(payload, ORIGEM_ESPERADA);
```

## 6. Open redirect

```ts
// Ruim: destino vem do parâmetro "next".
redirect(searchParams.get('next') ?? '/');

// Bom: só caminho relativo do próprio site.
function destinoSeguro(valor: string | null): string {
  if (!valor) return '/';
  // aceita "/algo"; rejeita "//outro.com" e "/\outro.com", que o navegador trata como outro host
  if (!valor.startsWith('/') || valor.startsWith('//') || valor.startsWith('/\\')) return '/';
  return valor;
}
redirect(destinoSeguro(searchParams.get('next')));
```

Allowlist de caminhos conhecidos é ainda mais restritiva e preferível em fluxo de login.

## 7. Token e segredo

- Token de sessão ou de refresh em `localStorage` fica legível por qualquer script que rode na página, inclusive de um XSS. A alternativa é cookie `HttpOnly; Secure; SameSite=Lax` (ou `Strict`) emitido pelo servidor. Isso muda o back-end: entregue um pedido de integração ao `backend-api` com o contrato e o risco, em vez de remendar o cliente.
- CSRF: cookie de sessão pede `SameSite` e verificação de origem ou token no servidor. Server Actions e Route Handlers exigem autenticação e autorização dentro de cada um (V-46).
- Segredo em variável pública ou em código: o repositório e o bundle já o expuseram. Rotacione, mova o uso para o servidor (Route Handler, Server Action, proxy) e só então corrija o código. Variável sem prefixo público não vai ao bundle no Next (V-14), mas isso não torna uma chave "segura" para chamar do navegador.
- Segredo nunca entra em arquivo versionado nem em relatório: ao citar um achado, mascare o valor (`sk-***`).
