from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def get_key(ti):
    sample_xcom_key = 'xcom test'
    ti.xcom_push(
        key='sample_xcom_key',
        value=sample_xcom_key
    )

def pull_key(ti):
    smpl_key = ti.xcom_pull(
        key='sample_xcom_key',
        task_ids='task1'
    )
    print(smpl_key)

with DAG(
        'd-savelko_task8',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
        },
        description='A simple tutorial DAG',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2022, 1, 1),
        catchup=False,
        tags=['example'],
) as dag:
    task1 = PythonOperator(
        task_id="task1",
        python_callable=get_key,
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=pull_key,
    )

    task1 >> task2

