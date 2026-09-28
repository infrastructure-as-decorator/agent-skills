# Infrastructure as Decorators Agent Skills

Este repositorio de GitHub es un catálogo portable de dos Agent Skills independientes:

- `build-with-lambda-api-decorators`: para desarrolladores que construyen aplicaciones con las APIs públicas de `lambda-api-decorators` y `lambda-api-decorators-cdk`.
- `maintain-lambda-api-decorators`: para contributors y maintainers del runtime, CDK, ejemplos, documentación, contratos, tests, workflows y releases.

No es necesario instalar ambos. Cada skill se instala y actualiza individualmente, aunque ambos se versionan bajo el mismo tag del catálogo. `lambda-api-decorators-development` fue reemplazado por estos dos skills y no existe un tercer alias activo.

## Instalación desde GitHub

GitHub es el único canal de distribución. `gh skill` está en public preview y requiere GitHub CLI `2.90.0` o posterior. Antes de instalar un skill externo, revisa su contenido con `gh skill preview`. `gh skill` instala el skill en la ubicación correspondiente al agente y scope seleccionados.

Skill para desarrolladores de aplicaciones:

```bash
gh skill preview infrastructure-as-decorator/agent-skills \
  build-with-lambda-api-decorators
gh skill install infrastructure-as-decorator/agent-skills \
  build-with-lambda-api-decorators
```

Skill para contributors y maintainers:

```bash
gh skill preview infrastructure-as-decorator/agent-skills \
  maintain-lambda-api-decorators
gh skill install infrastructure-as-decorator/agent-skills \
  maintain-lambda-api-decorators
```

Para fijar una instalación a una versión del catálogo:

```bash
gh skill install infrastructure-as-decorator/agent-skills \
  build-with-lambda-api-decorators@v1.0.0
```

`v1.0.0` es solamente un ejemplo; no se afirma que ese tag exista todavía. Las actualizaciones de un skill instalado se gestionan con `gh skill update`. El catálogo usa tags SemVer y GitHub Releases; no se crea una versión dentro de `SKILL.md`, `agents/openai.yaml` ni los contratos.

## Contratos y desarrollo

Los contratos `_agent/api-contract.json` y `_agent/behavior.md` se distribuyen dentro de los paquetes Python. Usan `schema_version: "1.0"`; el JSON no contiene la versión del paquete. La versión se obtiene desde metadata de distribución. Si no existe evidencia suficiente de publicación, el resolver informa `publication_state: unknown`.

Los contratos empaquetados son la autoridad para consumidores. Durante el desarrollo de las librerías, source y tests siguen siendo la autoridad. Los scripts de resolución y auditoría están reservados al skill de mantenimiento y no son un requisito normal para desarrollar una aplicación.

## Desarrollo del catálogo

```bash
python -m pytest -q
python -m compileall -q skills tests
git diff --check
```

No se mantienen snapshots estáticos de APIs, CHANGELOG ni contratos copiados en este repositorio.
