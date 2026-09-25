""" OS module
    Provee funciones para interactuar con el sistema operativo
    Tareas comunes como listar el contenido de un directorio o carpeta, ver las propiedades de un archivo
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PRUEBAS_DIR = BASE_DIR / "directorio_pruebas"
BACKUP_DIR = BASE_DIR / "directorio_backup"


def os_demo():
    PRUEBAS_DIR.mkdir(parents=True, exist_ok=True)

    files = os.listdir(PRUEBAS_DIR)
    for file in files:
        print(" -", file)

    file_path = os.path.join(PRUEBAS_DIR, "sample_file_1.csv")
    print(file_path)

    if os.path.exists(file_path):
        stats = os.stat(file_path)
        print(f"El archivo {file_path} existe y su tamano es {stats.st_size} bytes.")
    else:
        print(f"El archivo {file_path} no existe.")

    os.environ["MY_VARIABLE"] = "12345"
    print("MY_VARIABLE:", os.environ.get("MY_VARIABLE"))


""" pathlib module
    Más moderna y es una forma orientadaba objetos para manejar rutas de archivos. Hace el código más entendible
    y conciso. En general, es una mejor opción que OS.path.
"""
def pathlib_demo():
    current_dir = Path(".")

    file_path = current_dir / PRUEBAS_DIR.name / "sample_file_1.csv"

    if file_path.exists():
        print(f"Archivo {file_path} ya existe ({file_path.stat().st_size} bytes).")
    else:
        file_path.write_text("Hola, pathlib", encoding="utf-8")
        print(f"El archivo {file_path} fue creado con un texto de muestra")

    return file_path


""" shutil module
    Ofrece funciones para copiar, mover y eliminar archivos y carpetas.
"""
import shutil


def shutil_demo(source_file):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_file = BACKUP_DIR / "backup_sample_file_1.csv"

    if source_file.exists():
        shutil.copy2(source_file, backup_file)
        print(f"Archivo copiado {source_file} a {backup_file}")
    else:
        print(f"Archivo de origen {source_file} no existe")
        return

    temp_dir = BASE_DIR / "temp_dir"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        print(f"Directorio temporal previo eliminado: {temp_dir}")

    temp_dir.mkdir()
    (temp_dir / "temporal.txt").write_text("temporal", encoding="utf-8")
    print(f"Directorio temporal creado {temp_dir}")

    shutil.rmtree(temp_dir)
    print(f"Directorio temporal eliminado: {temp_dir}")


""" glob module
    Permite buscar rutas de archivos que coinciden con un patron especifico.
"""
import glob


def glob_demo():
    py_files = glob.glob(str(BASE_DIR / "*.py"))
    print("Archivos .py en el directorio actual:")
    for py_file in py_files:
        print(" -", py_file)


def main():
    os_demo()
    source_file = pathlib_demo()
    shutil_demo(source_file)
    glob_demo()


if __name__ == "__main__":
    main()
