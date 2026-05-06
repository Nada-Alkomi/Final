from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# ================= TASKS =================

def extract_stock_data():
    print("Extracting stock data...")

def transform_data():
    print("Transforming data...")

def load_to_database():
    print("Loading data into database...")

def run_pipeline():
    subprocess.run([
        "python",
        "D:/final_DataEngineering/stock-data-pipeline/main.py"
    ])

# ================= DAG =================

with DAG(
    dag_id="stock_data_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_stock_data",
        python_callable=extract_stock_data
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )

    load_task = PythonOperator(
        task_id="load_to_database",
        python_callable=load_to_database
    )

    pipeline_task = PythonOperator(
        task_id="run_full_pipeline",
        python_callable=run_pipeline
    )

    extract_task >> transform_task >> load_task >> pipeline_task