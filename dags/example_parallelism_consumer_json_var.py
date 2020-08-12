from datetime import timedelta

from airflow.models import DAG
from airflow.operators.papermill_operator import PapermillOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Airflow',
    'start_date': days_ago(2)
}

with DAG(
    dag_id='example_parallelism_consumer_json_var',
    default_args=default_args,
    catchup=False,
    schedule_interval='*/2 * * * *',
    dagrun_timeout=timedelta(minutes=60)
) as dag:

    create_vars = PapermillOperator(
        task_id="Create",
        input_nb="dags/notebooks/example_parallelism_consumer_json_var/create_json_var.ipynb",
        output_nb="dags/notebooks/outnbs/out-json_var_parallelism.ipynb",
        parameters={"msg": "Created"}
    )

    print_json_var = PapermillOperator(
        task_id="print_json_var",
        input_nb="dags/notebooks/example_parallelism_consumer_json_var/print_json_var.ipynb",
        output_nb="dags/notebooks/outnbs/out-json_var_parallelism.ipynb",
        parameters={"msg": "Print"}
    )

    for i in range(3):
        task = PapermillOperator(
            task_id='consumer_json_' + str(i),
            input_nb='dags/notebooks/example_parallelism_consumer_json_var/runme_' + str(i) + '.ipynb',
            output_nb="dags/notebooks/outnbs/out-json_var_parallelism.ipynb",
            parameters={"msgs": "Consumer"}
        )
        create_vars >> task >> print_json_var
    
    delete_vars = PapermillOperator(
        task_id="delete",
        input_nb="dags/notebooks/example_parallelism_consumer_json_var/delete_json_var.ipynb",
        output_nb="dags/notebooks/outnbs/out-delete_json_var.ipynb",
        parameters={"msgs": 'deleted' }
    )

    print_json_var >> delete_vars
