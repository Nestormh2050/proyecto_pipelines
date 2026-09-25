from pathlib import Path

import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
PRUEBAS_DIR = BASE_DIR / "directorio_pruebas"

CANTIDAD_ARCHIVOS = 10
FILAS_POR_ARCHIVO = 100


def main():
    PRUEBAS_DIR.mkdir(parents=True, exist_ok=True)

    df = sns.load_dataset("tips")

    for x in range(CANTIDAD_ARCHIVOS):
        sample = df.sample(FILAS_POR_ARCHIVO)
        sample.to_csv(PRUEBAS_DIR / f"sample_file_{x + 1}.csv", index=False)
        print(f"Escrito {PRUEBAS_DIR / f'sample_file_{x + 1}.csv'}")


if __name__ == "__main__":
    main()
