# Instagram Content Automation Bot

Este proyecto es una herramienta para automatizar la subida de contenido a múltiples cuentas de Instagram. Además, permite descargar y guardar los videos más virales de un usuario dado para reutilizar ese contenido en las cuentas automatizadas. Ideal para creadores de contenido, marketers o growth hackers que gestionan varias cuentas y buscan ahorrar tiempo.

---

## Funcionalidades

- **Automatización de publicaciones**: Sube contenido a un número arbitrario de cuentas de Instagram de forma programada.
- **Extracción de contenido viral**: Dado un nombre de usuario, guarda los n videos más virales del perfil.
- **Gestión multi-cuenta**: Control centralizado para manejar y publicar en varias cuentas a la vez.
- **Optimización del engagement**: Usa contenido viral previamente probado para maximizar las interacciones.

---

## Tecnologías utilizadas

### Instagrapi
- **Propósito**: Api no oficial de Python para interactuar con Instagram.
- **Uso**: Permite, entre otras cosas, subir contenido a las cuentas automatizadas.

### JSON
- **Propósito**: Tener información estructurada.
- **Uso**: Tener sesiones guardadas con el objetivo de no iniciar sesión varias veces y organizar el contenido que se publica.

### Instaloader
- **Propósito**: Biblioteca de Python para interactuar con Instagram.
- **Uso**: Descarga de contenido (fotos, videos, historias) de perfiles específicos.
