from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from pro import run_twitter_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 14),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    dag_id='twitter_etl_dag',
    default_args=default_args,
    description='ETL DAG to fetch tweets and store in S3',
    schedule=timedelta(days=1),  # ✅ this is correct now
    catchup=False,
    tags=['twitter', 'etl']
)

run_etl = PythonOperator(
    task_id='complete_twitter_etl',
    python_callable=run_twitter_etl,
    dag=dag
)

run_etl
