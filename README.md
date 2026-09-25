# Proyecto Pipelines

Código de los tutoriales de [CampBi](https://www.youtube.com/@campbi).

```
Python/
├── pipelines-en-python/          Refactorización progresiva de un pipeline de datos
│   ├── data/csv/                 shopping_behavior_2023|2024|2025.csv
│   ├── data/xml/                 los mismos datos en XML
│   └── utils/                    XMLAdapter, DataSaveFactory
└── automatizalo-todo-con-python/ Manejo de archivos, web scraping, comandos del sistema
```

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
.venv/bin/activate            # Linux / macOS
pip install -r requirements.txt
```

Airflow va aparte porque necesita Linux (ver [Problemas conocidos](#problemas-conocidos)):

```bash
pip install -r requirements.txt -r requirements-airflow.txt
```

## `Python/pipelines-en-python`

Cada archivo es una versión del **mismo pipeline**, con un patrón de diseño distinto.
El objetivo de negocio es común a todas: sobre el dataset de comportamiento de compras,
filtrar los pagos con `PayPal` y compras `Weekly`/`Fortnightly`/`bi-weekly`, agrupar por
`customer_id` + `category`, y quedarse con **el cliente que más gastó en cada categoría**.

| Archivo | Patrón / idea | Entrada |
|---|---|---|
| `version_1.py` | Script monolítico, un solo bloque | CSV 2023 |
| `version_2.py` | Descomposición en `step1`..`step4` | CSV 2023 |
| `version_3.py` | Composición funcional con `apply()` | 3 CSV |
| `version_4.py` | Patrón **Pipeline** (`pipeline(*steps)`) | 3 CSV |
| `version_5_adapter_pattern.py` | Patrón **Adapter** (normaliza XML a CSV) | 3 XML |
| `version_6_decorator_pattern.py` | Patrón **Decorator** (logging + cronometraje) | 3 XML |
| `airflow_version.py` | Orquestación con Apache Airflow (XCom) | 3 XML |

```bash
cd Python/pipelines-en-python
python version_1.py
```

Cada ejecución escribe `result.txt` (v1, v2) o `result_<uuid>.txt` (v3 a v6) en la misma
carpeta, con una línea por categoría en formato `customer_id, category`. Ambos formatos de
entrada producen resultados idénticos.

`airflow_version.py` necesita un entorno Airflow. Copia el archivo (o la carpeta) al
`dags_folder` de tu Airflow, o exponlo con `airflow dags test shopping_behavior_pipeline`.
El DAG se llama `shopping_behavior_pipeline` y corre bajo demanda (`schedule=None`).

## `Python/automatizalo-todo-con-python`

| Archivo | Contenido |
|---|---|
| `manejo_archivos.py` | `os`, `os.path`, `pathlib`, `shutil`, `glob` |
| `web_scrapping.py` | `requests`, Selenium, Scrapy |
| `automatizacion_sistema.py` | `subprocess` para ejecutar comandos del sistema |
| `populate_tests.py` | Genera 10 CSV de muestra con el dataset `tips` de seaborn |

```bash
cd Python/automatizalo-todo-con-python
python populate_tests.py       # genera directorio_pruebas/ (necesario para manejo_archivos.py)
python manejo_archivos.py
python automatizacion_sistema.py
```

`web_scrapping.py` abre Chrome real: requiere Chrome y el driver de selenium-manager.
El spider de Scrapy (`ExampleSpider`) solo es ejecutable dentro de un proyecto Scrapy.
`populate_tests.py` descarga el dataset `tips` la primera vez, así que necesita internet.

## Datos

`Customer Shopping Behavior Dataset` (Kaggle), 3 años con 3.900 / 3.600 / 3.700 registros
y 19 columnas. Disponible en CSV y en XML dentro de `data/`.

## Problemas conocidos

- **`airflow_version.py` requiere Linux.** Airflow no soporta Windows de forma nativa
  (falla con `cannot import name 'ObjectStoragePath' from 'airflow.sdk'`). En Windows usa
  WSL2 o un contenedor Linux. El resto del repo sí funciona en Windows.
- **`web_scrapping.py` abre Chrome real** y necesita el driver de selenium-manager.
  El spider de Scrapy (`ExampleSpider`) solo corre dentro de un proyecto Scrapy.
- **`populate_tests.py` necesita internet** la primera vez: descarga el dataset `tips`.
- El DAG de Airflow pasa DataFrames por XCom, que es un anti-patrón de Airflow (el estado
  del pipeline queda en la metadata DB). Para producción, escribir a disco o a un
  warehouse en vez de usar XCom.

## Licencia

Material educativo de los tutoriales de CampBi.
