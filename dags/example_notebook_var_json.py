from datetime import timedelta

from airflow.models import DAG
from airflow.operators.papermill_operator import PapermillOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
    'provide_context': True
}

with DAG(
    dag_id='example_notebook_var_json',
    default_args=default_args,
    catchup=False,
    schedule_interval='*/4 * * * *',
    dagrun_timeout=timedelta(minutes=60)
) as dag:

    send_this = PapermillOperator(
        task_id="send",
        provide_context=True,
        input_nb="dags/notebooks/example_notebook_var_json/create_json_var.ipynb",
        output_nb="dags/notebooks/outnbs/out-json_var.ipynb",
        parameters={"msg": "Sended"}
    )

    recive_this = PapermillOperator(
        task_id="recive",
        provide_context=True,
        input_nb="dags/notebooks/example_notebook_var_json/consume_json_var.ipynb",
        output_nb="dags/notebooks/outnbs/out-json_var.ipynb",
        parameters={"msgs": 'Recived' }
    )

    delete_vars = PapermillOperator(
        task_id="delete",
        provide_context=True,
        input_nb="dags/notebooks/example_notebook_var_json/delete_json_var.ipynb",
        output_nb="dags/notebooks/outnbs/out-delete_json_var.ipynb",
        parameters={"msgs": 'deleted' }
    )

    send_this >> recive_this >> delete_vars