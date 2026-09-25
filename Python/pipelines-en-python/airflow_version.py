import time
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
import uuid

from utils.xml_adapter import XMLAdapter
from utils.data_save_factory import DataSaveFactory

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "xml"

FREQUENCIES = ["Weekly", "Fortnightly", "bi-weekly"]


def logging_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        t1 = time.perf_counter()
        print(f"Llamando funcion: {func.__name__}")
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f"Funcion {func.__name__} completada")
        print(f"Tiempo de ejecucion: {t2 - t1:.4f}s")
        return result

    return inner


@logging_decorator
def extract_data():
    return [XMLAdapter(DATA_DIR / f"shopping_behavior_{year}.xml").get_data() for year in (2023, 2024, 2025)]


@logging_decorator
def step1(**context):
    df_list = context["ti"].xcom_pull(task_ids="extract_data")
    results = []
    for df in df_list:
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        df = df[df["payment_method"] == "PayPal"]
        df = df[df["frequency_of_purchases"].isin(FREQUENCIES)]
        results.append(df)
    return results


@logging_decorator
def step2(**context):
    df_list = context["ti"].xcom_pull(task_ids="step1")
    results = []
    for df in df_list:
        df = (
            df[["customer_id", "category", "purchase_amount_(usd)"]]
            .groupby(["customer_id", "category"])
            .sum()
            .reset_index()
        )
        df["rank"] = df.groupby("category")["purchase_amount_(usd)"].rank(
            method="dense", ascending=False
        )
        df = df[df["rank"] == 1]
        results.append(df)
    return results


@logging_decorator
def step3(**context):
    df_list = context["ti"].xcom_pull(task_ids="step2")
    results = []
    for df in df_list:
        results.append(list(df[["customer_id", "category"]].itertuples(index=False, name=None)))
    return results


@logging_decorator
def step4(**context):
    results = context["ti"].xcom_pull(task_ids="step3")
    return [
        DataSaveFactory().save_file(save_type="txt", result=result, id=uuid.uuid4(), output_dir=BASE_DIR)
        for result in results
    ]


def build_dag():
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    default_args = {
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }

    with DAG(
        dag_id="shopping_behavior_pipeline",
        default_args=default_args,
        description="Replicating pipeline with Airflow",
        schedule=None,
        start_date=datetime(2025, 1, 1),
        catchup=False,
        tags=["pipeline", "shopping"],
    ) as dag:
        tasks = [
            PythonOperator(task_id=name, python_callable=callable_)
            for name, callable_ in [
                ("extract_data", extract_data),
                ("step1", step1),
                ("step2", step2),
                ("step3", step3),
                ("step4", step4),
            ]
        ]

        for upstream, downstream in zip(tasks, tasks[1:]):
            upstream >> downstream

    return dag


dag = build_dag()
