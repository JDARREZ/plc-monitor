# PLC Monitor (Allen Bradley)

Aplicación de escritorio en **Python + PyQt5** para monitorear variables (tags) de un PLC Allen Bradley por **EtherNet/IP** usando `pylogix`.

## 1) Descripción del proyecto

La app permite:
- Configurar conexión al PLC (IP, slot, polling)
- Descubrir tags del PLC y seleccionar múltiples variables a monitorear
- Graficar variables en tiempo real
- Guardar lecturas en SQLite (`id, tag_name, value, timestamp`)
- Consultar historial por rango de fechas/tag y exportar a CSV

## 2) Interfaz y paneles

- **Setup**: IP PLC, slot, polling, prueba de conexión y guardado de configuración persistente
- **Monitor**: descubrimiento de tags, filtro por nombre, checkboxes para selección, valor actual
- **Gráficas**: curvas por tag con color/leyenda, zoom/pan, auto-scroll, pausa/reanudar, valores actuales
- **Historial**: consulta por fechas/tag, tabla de resultados, exportación a CSV
- **Barra de estado**: estado de conexión, IP y cantidad de tags monitoreados

## 3) Requisitos del sistema

- Python 3.10+
- Acceso de red al PLC Allen Bradley
- Windows/Linux/macOS

## 4) Instalación paso a paso

```bash
git clone https://github.com/JDARREZ/plc-monitor.git
cd plc-monitor
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## 5) Ejecutar en modo desarrollo

```bash
python src/main.py
```

## 6) Generar ejecutable (.exe)

### Windows
```bat
build.bat
```
Genera: `dist\plc-monitor.exe`

### Linux/macOS
```bash
./build.sh
```
Genera: `dist/plc-monitor`

## 7) Guía de uso

1. Ir a **Setup**, configurar IP/slot/polling y guardar
2. Presionar **Probar conexión**
3. Ir a **Monitor** y pulsar **Descubrir tags**
4. Seleccionar tags (checkboxes) y pulsar **Aplicar selección**
5. Revisar gráficas en **Gráficas**
6. Consultar y exportar datos desde **Historial**

## 8) Troubleshooting

- **"pylogix no está instalado"**: ejecutar `pip install -r requirements.txt`
- **No conecta al PLC**: validar IP, slot, firewall y conectividad de red
- **No aparecen tags**: confirmar permisos y estado del PLC
- **Sin datos en historial**: verificar que haya tags seleccionados y conexión activa
