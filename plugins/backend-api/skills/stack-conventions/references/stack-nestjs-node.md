# NestJS e Node: guards, validação e erros

Fontes: documentação oficial de Guards do NestJS (V-19, https://docs.nestjs.com/guards, Verificado em 2026-10-10; licença do projeto: Não verificado); OWASP (V-09, V-10); RFC 9457 (V-14). Código abaixo é redação própria. **Confirme a versão instalada**: `npm ls @nestjs/core @nestjs/common @nestjs/jwt class-validator` (assinaturas de `Reflector` e de `@nestjs/jwt` mudam entre versões maiores). Express/Fastify puros, tRPC e NestJS com GraphQL/microserviços: **lacuna** (lacunas registradas em `fontes.md` do playbook). Um arquivo de regras da comunidade para NestJS foi **rejeitado** na pesquisa por conter instrução de override e tabela de imports banidos sem fonte; só a ideia de checar a existência do pacote foi aproveitada.

## Sumário

1. Checklist
2. Guard de autenticação e papéis
3. Autorização por objeto
4. Validação de entrada
5. Erros em RFC 9457
6. Ordem de execução
7. Verificação por busca

## 1. Checklist

- [ ] Guard de autenticação **valida** o token (algoritmo fixo, `iss`, `aud`, `exp`) e anexa `request.user` (V-19).
- [ ] Guard de papéis lê metadata da rota (`Reflector.createDecorator` ou `@SetMetadata`) (V-19).
- [ ] Guard global via `APP_GUARD` num módulo (permite injeção de dependências); `app.useGlobalGuards()` fora de módulo **não** injeta dependências (V-19).
- [ ] Negar por padrão: guard global de autenticação + decorador `@Public()` explícito para exceções.
- [ ] Guard que devolve `false` resulta em 403 (`ForbiddenException`) (V-19); falta de credencial deve ser 401 (`UnauthorizedException`).
- [ ] Autorização por **objeto** (dono/tenant) no service/repositório: guard de papel não basta.
- [ ] `ValidationPipe` global com `whitelist: true`, `forbidNonWhitelisted: true`, `transform: true` (class-validator) contra atribuição em massa (Inferido; padrão de práticas Nest, confirme nas docs da versão).
- [ ] DTOs de saída separados (serialização por classe/`ClassSerializerInterceptor` ou mapeamento explícito) sem campos sensíveis.
- [ ] Filtro de exceção global gera `application/problem+json` sem stack.
- [ ] Rate limit em login/reset (`@nestjs/throttler` ou equivalente): chave de credencial validada.
- [ ] Antes de importar um pacote: `npm ls <pacote>` e a doc oficial; na dúvida, não importe.

## 2. Guard de autenticação e papéis

```typescript
import { CanActivate, ExecutionContext, Injectable, SetMetadata, UnauthorizedException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { JwtService } from '@nestjs/jwt';

export const IS_PUBLIC = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC, true);

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private readonly jwt: JwtService, private readonly reflector: Reflector) {}

  async canActivate(ctx: ExecutionContext): Promise<boolean> {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC, [ctx.getHandler(), ctx.getClass()]);
    if (isPublic) return true;
    const req = ctx.switchToHttp().getRequest();
    const [tipo, token] = (req.headers.authorization ?? '').split(' ');
    if (tipo !== 'Bearer' || !token) throw new UnauthorizedException();
    try {
      req.user = await this.jwt.verifyAsync(token, {
        publicKey: process.env.JWT_PUBLIC_KEY,
        algorithms: ['RS256'],                 // fixado no servidor
        issuer: process.env.JWT_ISSUER,
        audience: process.env.JWT_AUDIENCE,
      });
    } catch {
      throw new UnauthorizedException();
    }
    return true;
  }
}
```

Papéis por metadata (Nest 10 ou superior; confirme a assinatura na sua versão):

```typescript
export const Roles = Reflector.createDecorator<string[]>();

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}
  canActivate(ctx: ExecutionContext): boolean {
    const roles = this.reflector.getAllAndOverride(Roles, [ctx.getHandler(), ctx.getClass()]);
    if (!roles) return true;
    const user = ctx.switchToHttp().getRequest().user;
    return roles.some((r) => user?.roles?.includes(r));   // false => 403
  }
}

// app.module.ts
providers: [
  { provide: APP_GUARD, useClass: AuthGuard },     // 1º: autentica e anexa request.user
  { provide: APP_GUARD, useClass: RolesGuard },    // 2º: lê metadata de papéis
],

// controller
@Roles(['admin'])
@Delete(':id')
remover(@Param('id') id: string) { /* ... */ }
```

`@SetMetadata('roles', [...])` com `reflector.get('roles', ...)` é a forma anterior, ainda válida. A ordem de execução entre dois `APP_GUARD` segue a de registro (Inferido; confirme na sua versão).

## 3. Autorização por objeto

```typescript
async obterPedido(id: string, user: { sub: string }) {
  const pedido = await this.repo.findOne({ where: { id, ownerId: user.sub } });   // dono vem do token
  if (!pedido) throw new NotFoundException();   // alheio e inexistente indistinguíveis
  return PedidoDto.from(pedido);                 // DTO de saída, sem campos internos
}
```

Escopos/papéis do token não substituem o filtro de dono (BOLA). Guard de papel só decide a função (BFLA).

## 4. Validação de entrada

```typescript
// main.ts
app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }));
```

DTO de entrada sem `ownerId`, `role`, `status` ou `total`: quem calcula e atribui é o servidor. Limites de corpo no adaptador (`bodyParser`/`json({ limit })`) e tamanho de upload.

## 5. Erros em RFC 9457

Filtro global (adaptador Express; para Fastify use `reply.type(...).send(...)`, confirme a API):

```typescript
@Catch()
export class ProblemFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const res = host.switchToHttp().getResponse();
    const status = exception instanceof HttpException ? exception.getStatus() : 500;
    const title = exception instanceof HttpException ? exception.message : 'Internal Server Error';
    res.status(status).type('application/problem+json').json({
      type: 'about:blank', title, status,   // sem stack, SQL ou hostname; detalhe vai para o log
    });
  }
}
```

Erros do `ValidationPipe` chegam como `BadRequestException` (400) com lista de mensagens: mapeie para a extensão `errors` do projeto, sem ecoar valores sensíveis.

## 6. Ordem de execução

A documentação confirma: guards executam **depois** dos middlewares e **antes** de interceptors e pipes (V-19). A ordem entre interceptors e pipes não é definida na página lida: não a afirme sem conferir na versão. Consequência prática: autenticação/papel (guard) corre antes da validação (pipe); o filtro de exceção captura o que for lançado em qualquer etapa.

## 7. Verificação por busca

```bash
grep -rEn "@(Get|Post|Put|Patch|Delete)\(" src | wc -l                # total de rotas
grep -rEn "@UseGuards|APP_GUARD|@Public\(|@Roles\(" src               # compare com as rotas
grep -rEn "useGlobalGuards|forbidNonWhitelisted|whitelist" src
grep -rEn "algorithms|ignoreExpiration|verify\(|decode\(" src          # JWT: decode sem verify é achado
grep -rEn "Object\.assign\(|\.\.\.(dto|body)" src                      # atribuição em massa (heurística)
```

Leia o código antes de reportar: a presença de `@UseGuards` na classe cobre os métodos; `@Public()` fora de rotas realmente públicas é achado.
