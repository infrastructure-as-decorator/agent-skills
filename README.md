# Infrastructure as Decorators agent skills

Este repositorio contiene dos skills portables basados en Agent Skills:

- `build-with-lambda-api-decorators` ayuda a desarrolladores a construir, probar y revisar aplicaciones que consumen las APIs públicas de `lambda-api-decorators` y `lambda-api-decorators-cdk`.
- `maintain-lambda-api-decorators` ayuda a contributors y maintainers a cambiar las librerías, CDK, ejemplos y documentación oficial, coordinando source, tests, contratos, wheels y releases.

Usa el skill de consumidores para solicitudes como “agrega `/me` protegido con Cognito a mi aplicación” o “usa `current_user` en mi handler”. Usa el skill de mantenimiento para “corrige `ResourceBuilder`”, “crea un ejemplo oficial con la versión publicada” o cambios en Docusaurus y workflows.

## Instalación

Para herramientas compatibles con Agent Skills, copia o enlaza uno o ambos directorios bajo el directorio de skills de la herramienta, por ejemplo:

```bash
cp -R .agents/skills/build-with-lambda-api-decorators ~/.codex/skills/
cp -R .agents/skills/maintain-lambda-api-decorators ~/.codex/skills/
```

También pueden instalarse como skills locales copiándolos a `.agents/skills/` del proyecto consumidor o mantenedor. No hay una dependencia obligatoria de Codex, Claude Code o GitHub Copilot; cada herramienta compatible puede descubrir `SKILL.md` y, opcionalmente, usar `agents/openai.yaml` como metadata específica de OpenAI.

`lambda-api-decorators-development` fue reemplazado por estos dos skills; no existe un tercer alias activo.

## Contratos y tooling

Los contratos `_agent/api-contract.json` y `_agent/behavior.md` se distribuyen dentro de los paquetes Python. La versión proviene de metadata de distribución (o de `METADATA` en un wheel), nunca del JSON; el JSON describe el contrato y no contiene una versión del paquete. La instalación por sí sola no demuestra publicación, por lo que el resolver informa `publication_state: unknown` cuando no existe evidencia suficiente.

Los contratos empaquetados sirven para consumidores y distribuciones. Durante el desarrollo de las librerías, source y tests siguen siendo la autoridad. Los scripts internos de resolución, auditoría y validación pertenecen al skill de mantenimiento y no son un requisito normal para desarrollar una aplicación.

## Desarrollo de este repositorio

```bash
python -m pytest -q
python -m compileall -q .agents tests
git diff --check
```

No se mantienen snapshots estáticos de APIs, changelogs ni contratos copiados en este repositorio.
