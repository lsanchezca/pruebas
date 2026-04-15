# 🚛 Truck Telemetry Viewer

Visualizador interactivo de datos de telemetría de camiones. Muestra posiciones de vehículos en tiempo real sobre un mapa interactivo y tabla de datos.

## 📋 Características

- **Tabla de datos**: Vista de todos los registros de telemetría con búsqueda y filtrado
- **Mapa interactivo**: Visualización en Leaflet con puntos de entrega (bins) y camiones distribuidos
- **Datos en vivo**: Importación desde CSV a base de datos SQLite
- **APIs JSON**: Endpoints para consumir datos desde el frontend
- **Dashboard**: Estadísticas en tiempo real (camiones activos, peso promedio, etc.)

## 🚀 Inicio rápido

### 1. Instalar dependencias

```bash
cd django_test/mytestsite
python -m venv .venv
.venv\Scripts\activate  # En Windows

pip install django pandas django-extensions
```

### 2. Preparar la base de datos

```bash
python manage.py migrate
python manage.py runscript import_data
```

### 3. Ejecutar el servidor

```bash
python manage.py runserver
```

Abre: `http://127.0.0.1:8000/data_viewer/view_data/`

## 📁 Estructura del proyecto

```
pruebas/
├── django_test/mytestsite/        # Proyecto Django
│   ├── manage.py
│   ├── data_viewer/                # App principal
│   │   ├── models.py              # DataEntry y bin
│   │   ├── views.py               # APIs
│   │   ├── urls.py                # Rutas
│   │   ├── import_data.py         # Script de importación
│   │   └── templates/             # HTML templates
│   └── mytestsite/                # Configuración
├── data/                           # Archivos CSV
│   ├── raspberrypi_aws_truck_raw_simulated.csv
│   ├── raspberrypi_aws_truck_preprocessed.csv
│   └── raspberrypi_aws_truck_preprocessed_bins.csv
├── data_preprocesor.py            # Script de preprocesamiento
└── README.md
```

## 🗺️ Rutas disponibles

| URL | Descripción |
|-----|-------------|
| `/data_viewer/view_data/` | Tabla interactiva |
| `/data_viewer/view_map/` | Mapa con bins y camiones |
| `/data_viewer/api/data/` | API JSON - datos tabla |
| `/data_viewer/api/map/` | API JSON - datos mapa |
| `/admin/` | Panel de administración Django |

## 📊 Modelos de datos

### DataEntry
```
- truck_id: ID del camión
- timestamp: Fecha y hora del registro
- latitude: Latitud
- longitude: Longitud
- weight: Peso bruto (kg)
- payload_kg: Carga (kg) [opcional]
```

### bin
```
- bin_id: ID del punto de entrega
- lat: Latitud
- lon: Longitud
```

## 🔄 Workflow

1. **Preprocesamiento**: `python data_preprocesor.py`
   - Lee CSV raw
   - Limpia datos (valores nulos, conversiones numéricas)
   - Genera CSV preprocesado

2. **Importación**: `python manage.py runscript import_data`
   - Lee CSV preprocesado y bins
   - Carga en SQLite con bulk_create

3. **Visualización**: Frontend Leaflet
   - Fetch a APIs
   - Renderiza tabla y mapa
   - Agrupa camiones por bin más cercano

## 🎨 Visualización del mapa

- **Bins (verde)**: Puntos de entrega centrales
- **Camiones 🚛**: Distribuidos en círculo alrededor de cada bin
- **Colores por peso**:
  - 🔴 Rojo: > 12.5T
  - 🟠 Naranja: > 11T
  - 🔵 Azul: > 9.5T
  - 🟦 Teal: Normal

## 🛠️ Comandos útiles

```bash
# Crear nuevo superusuario
python manage.py createsuperuser

# Limpiar e reimportar datos
python manage.py runscript import_data --script-args clear

# Check del proyecto
python manage.py check

# Crear migraciones
python manage.py makemigrations
```

## 📝 Archivos CSV

### raw_simulated
12,800+ registros simulados de 80 camiones con:
- Datos GPS (con ruido realista)
- Peso y carga
- Señales de Raspberry Pi (batería, RSSI, temperatura)

### preprocessed
CSV limpio listo para importar

### preprocessed_bins
Puntos de entrega únicos identificados por agrupación de coordenadas

## 📞 Desarrollo

- **Backend**: Django 6.0.4, Python 3.13.2
- **Frontend**: Leaflet.js 1.9.4, Vanilla JavaScript
- **Database**: SQLite (auto-generada)

## 📄 Licencia

MIT
