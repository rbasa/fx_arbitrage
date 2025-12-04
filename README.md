# Trading Algorítmico - Trabajo Práctico Final

## Descripción

Este proyecto implementa un sistema de procesamiento de datos de mercado (market data) para el ejercicio de FX, incluyendo funciones para leer datos de mercado y mantener un order book actualizado.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Configuración del Entorno

### Paso 1: Crear un entorno virtual (recomendado)

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
# venv\Scripts\activate
```

### Paso 2: Instalar dependencias

```bash
# Asegúrate de estar en el directorio raíz del proyecto
pip install -r requirements.txt
```

### Paso 3: Verificar la instalación

```bash
# Verificar que Python está funcionando correctamente
python --version

# Verificar que las dependencias se instalaron correctamente
python -c "import pandas; import numpy; print('Dependencias instaladas correctamente')"
```

## Estructura del Proyecto

```
tpFinal/
├── data/                    # Archivos CSV con datos de mercado
│   ├── GFGC79115D_11_11.csv
│   ├── GFGV79115D_11_11.csv
│   └── ...
├── consignas/              # Consignas del trabajo práctico
├── fx_orderbook.py         # Módulo principal con funciones de FX
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## Uso

### Ejecutar el procesamiento de datos

```bash
# Desde el directorio raíz del proyecto
python fx_orderbook.py
```

## Funcionalidades

- **Lectura de market data**: Función para leer y parsear archivos CSV con datos de mercado
- **Order Book**: Estructura de datos para mantener el libro de órdenes actualizado
- **Procesamiento**: Función `run()` que recorre todos los archivos de datos y actualiza el order book

## Notas

- Los archivos de datos deben estar en la carpeta `data/`
- El formato de los archivos CSV incluye niveles de bid/offer con precios y cantidades
- El sistema procesa los datos cronológicamente para mantener el estado del order book

