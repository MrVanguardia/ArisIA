# ArisIA - Asistente IA para Linux 🤖

## Distribuciones Soportadas

El instalador es compatible con las siguientes familias de distribuciones:

- Debian/Ubuntu y derivadas (usando apt)
- Fedora y derivadas (usando dnf)
- Arch Linux y derivadas (usando pacman)
- OpenSUSE (usando zypper)
- Void Linux (usando xbps)
- Gentoo (usando emerge)
- Alpine (usando apk)

## Requisitos del Sistema

- Python 3.8 o superior
- 4GB RAM mínimo (8GB recomendado)
- 2GB espacio en disco
- Conexión a Internet para la instalación

## Solución de Problemas

Si encuentras algún error durante la instalación:

1. Verifica que tienes conexión a Internet
2. Asegúrate de tener suficiente espacio en disco
3. Ejecuta el instalador con permisos de root
4. Verifica que tu sistema cumple los requisitos mínimos

## Desinstalación

Para desinstalar ArisIA:

```bash
sudo rm -rf /usr/local/share/arisia
sudo rm /usr/local/bin/arisia
sudo rm /usr/share/applications/arisia.desktop
```

## Soporte

Si necesitas ayuda, puedes:

1. Abrir un issue en el repositorio
2. Consultar la documentación en línea
3. Contactar al desarrollador

## Licencia

Este proyecto está bajo la licencia MIT.
