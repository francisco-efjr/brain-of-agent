# ASP.NET Core: tratamento de erros e API

Fontes: documentação Microsoft "Handle errors in ASP.NET Core" (V-22, https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling, versão .NET 10, Verificado em 2026-10-10; leitura de cerca de 100 mil de 243 mil caracteres) e `aspnet-rest-apis.instructions.md` do awesome-copilot (V-22, MIT; é um roteiro de tópicos, não um conjunto de regras; prompt-score 50). Código abaixo é redação própria. **Confirme a versão do SDK/runtime** (`dotnet --version`, `<TargetFramework>` no `.csproj`). Autenticação/autorização, Minimal APIs x controllers e validação estão **rasos** (lacuna declarada em `fontes.md` do playbook): o que está marcado Inferido vem de conhecimento estável e deve ser conferido.

## Sumário

1. Checklist
2. Pipeline de erros
3. IExceptionHandler com ProblemDetails
4. Validação e autorização (Inferido)
5. Pontos de atenção da documentação
6. Verificação por busca

## 1. Checklist

- [ ] `UseExceptionHandler` configurado fora de Development; `UseDeveloperExceptionPage` só em Development (V-22).
- [ ] `AddProblemDetails()` registrado: respostas de erro no formato Problem Details (a documentação cita RFC 7807; a **RFC 9457 a obsoleta**).
- [ ] Tratadores de exceção por `IExceptionHandler` via `AddExceptionHandler<T>()`; chamados **em ordem** de registro; `TryHandleAsync` retorna `true` para encerrar a cadeia e então **deve escrever a resposta completa**, senão o resultado é 404 (V-22). Exige `UseExceptionHandler` no pipeline.
- [ ] Mapeamento exceção de domínio → status em um lugar só, com `type`, `title` e `status` estáveis; sem stack/SQL no `detail`.
- [ ] Respostas de erro sem corpo (401/403/404 do framework) também em Problem Details (`UseStatusCodePages()` com `AddProblemDetails()`); `UseStatusCodePagesWithReExecute` preserva o status original, `WithRedirects` não (V-22).
- [ ] A partir do .NET 10, os diagnósticos (logs/métricas) de exceções **tratadas** por `IExceptionHandler` são suprimidos por padrão (V-22): registre explicitamente o que importa.
- [ ] Autorização por objeto no serviço/handler (resource-based), não só `[Authorize]`.
- [ ] Segredos por configuração segura (User Secrets em dev, variáveis/cofre em produção), nunca no `appsettings.json` versionado.
- [ ] Rate limit em login/reset; `Cache-Control: no-store` em dado sensível.

## 2. Pipeline de erros

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddProblemDetails();                       // formato Problem Details
builder.Services.AddExceptionHandler<DomainExceptionHandler>();   // ordem de registro = ordem de execução

var app = builder.Build();

app.UseExceptionHandler();                                  // usa os IExceptionHandler registrados
app.UseStatusCodePages();                                   // 4xx sem corpo viram Problem Details

app.MapGet("/orders/{id:guid}", async (Guid id, ClaimsPrincipal user, IOrderService svc) =>
    Results.Ok(await svc.GetAsync(id, user)));              // service lança DomainException

app.Run();
```

Em desenvolvimento, `app.UseDeveloperExceptionPage()` pode ser condicionado a `app.Environment.IsDevelopment()`. A doc mostra um exemplo de `StatusCodeSelector` dentro de `IsDevelopment()` que parece invertido (V-22): não o copie sem testar.

## 3. IExceptionHandler com ProblemDetails

```csharp
public sealed class DomainExceptionHandler(IProblemDetailsService problems, ILogger<DomainExceptionHandler> log)
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext ctx, Exception ex, CancellationToken ct)
    {
        if (ex is not DomainException d) return false;      // deixa o próximo tratador (ou o padrão) decidir

        log.LogWarning(ex, "domain error {Code}", d.Code);  // .NET 10 suprime o diagnóstico padrão: logue aqui
        ctx.Response.StatusCode = d.Status;
        return await problems.TryWriteAsync(new ProblemDetailsContext
        {
            HttpContext = ctx,
            ProblemDetails = new ProblemDetails
            {
                Type = $"https://api.exemplo.com.br/problems/{d.Code}",
                Title = d.Title,                            // estável, não varia por ocorrência
                Status = d.Status,                          // igual ao HTTP
                Detail = d.PublicDetail,                    // sem dado sensível
            },
        });
    }
}
```

`IProblemDetailsService.TryWriteAsync` negocia o tipo de conteúdo (`application/problem+json`) e aplica personalizações registradas em `AddProblemDetails` (Inferido a partir do conhecimento do framework; confirme na versão). Retornar `true` só quando a resposta foi **de fato** escrita (`TryWriteAsync` pode devolver `false`): propague o valor, como acima.

## 4. Validação e autorização (Inferido)

- Controllers com `[ApiController]` respondem 400 com `ValidationProblemDetails` em falha de model binding/validação. Minimal APIs não validam DTOs automaticamente em versões anteriores ao .NET 10, que trouxe suporte embutido à validação (Inferido: confirme na documentação da versão); sem ele, use FluentValidation ou `IValidatableObject` na borda.
- JWT: `AddAuthentication().AddJwtBearer(o => { o.Authority = ...; o.Audience = ...; })` valida emissor, audiência e vida do token com as opções padrão de `TokenValidationParameters` (Inferido); confirme que `ValidateAudience`, `ValidateIssuer`, `ValidateLifetime` não foram desligados no código (busca abaixo).
- Políticas: `builder.Services.AddAuthorizationBuilder().AddPolicy("orders:write", p => p.RequireClaim("scope", "orders:write"))` e `.RequireAuthorization("orders:write")` na rota. Para BOLA, use `IAuthorizationService.AuthorizeAsync(user, recurso, requisito)` com o recurso carregado, ou filtre pelo dono na consulta.
- Binding de DTO: modelos de entrada sem propriedades privilegiadas (`OwnerId`, `Role`); `[Bind]`/DTOs dedicados evitam *overposting*.

## 5. Pontos de atenção da documentação

- Cita RFC 7807; a RFC 9457 a obsoleta e mantém o mesmo formato base (V-14, V-22).
- Exemplo de `StatusCodeSelector` parece invertido; confira.
- Se o tratador devolve `true` sem escrever resposta, o cliente vê 404.
- A ordem dos `IExceptionHandler` é a de registro: coloque os específicos antes dos genéricos.

## 6. Verificação por busca

```bash
grep -rEn "UseExceptionHandler|UseDeveloperExceptionPage|AddProblemDetails|AddExceptionHandler" --include=*.cs .
grep -rEn "IExceptionHandler|TryHandleAsync" --include=*.cs .
grep -rEn "ValidateAudience|ValidateIssuer|ValidateLifetime|RequireHttpsMetadata" --include=*.cs .   # false é achado
grep -rEn "AllowAnonymous|\[Authorize|RequireAuthorization" --include=*.cs .
grep -rEn "ex\.(Message|StackTrace|ToString)\(?" --include=*.cs . | head -40     # vazamento em resposta (candidato)
dotnet build -warnaserror ; dotnet test        # via fluxo normal de permissão; cole a saída
```
