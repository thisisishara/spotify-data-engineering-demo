from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from sys import path
path.append("/home/ishara/PythonProjects/Spotify_Data_Engineering_Project/")

from spotify_etl import run_spotify_etl

default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'start_date': days_ago(0,0,0,0,0),
    'email':['thisismaduishara@gmail.com'],
    'email_on_failure':True,
    'email_on_retry':False,
    'retries':1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='spotify DAG with ETL',
    schedule_interval=timedelta(days=1)
)

run_etl = PythonOperator(
    task_id= 'spotify_etl_task',
    python_callable=run_spotify_etl,
    dag=dag
)

run_etl
# if more tasks: run_etl1 >> task2 >> [task3,task4]