# SurTV relases publicos

Repositorio publico para artefactos que la app SurTV puede consumir sin exponer
datos sensibles.

## Contenido permitido

- APKs oficiales firmadas.
- `releases/latest.json` con metadata de version.
- Logos publicos de canales.
- Hashes SHA256.
- Changelog publico.
- EPG publico si no contiene datos sensibles.

## Contenido no permitido

- Tokens.
- Credenciales.
- Cookies.
- Claves privadas.
- Headers sensibles.
- URLs tokenizadas.
- Catalogo operativo completo si contiene datos protegibles.

## Estructura

```text
releases/latest.json
releases/apk/
logos/
epg/
catalog/
schemas/
```

No publicar `catalog/app-catalog.json` hasta tener definido si el catalogo sera
publico firmado o servido por backend privado.
