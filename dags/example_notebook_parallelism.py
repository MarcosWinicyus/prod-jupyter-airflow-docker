from datetime import timedelta

from airflow.models import DAG
from airflow.operators.papermill_operator import PapermillOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'Airflow',
    'start_date': days_ago(2)
}

with DAG(
    dag_id='example_notebook_parallelism',
    default_args=default_args,
    catchup=False,
    schedule_interval='*/2 * * * *',
    dagrun_timeout=timedelta(minutes=60)
) as dag:

    opr_hello = BashOperator(task_id='say_Hi',
                             bash_command='echo "Hi!!"')

    for i in range(3):
        task = PapermillOperator(
            task_id='note_runme_' + str(i),
            input_nb='dags/notebooks/example_notebook_parallelism/runme_' + str(i) + '.ipynb',
            output_nb="dags/notebooks/outnbs/out.ipynb",
            parameters={"msgs": "Tarefa paralela " + str(i), "time": "{{ execution_date }}"}
        )
        task >> opr_hello
    
    opr_sleep = BashOperator(task_id='sleep_me',
                             bash_command='sleep 5')

    opr_hello >> opr_sleep

    run_this = PapermillOperator(
        task_id="run_example_notebook",
        input_nb="dags/notebooks/example_notebook_parallelism/hello_world.ipynb",
        output_nb="dags/notebooks/outnbs/out.ipynb",
        parameters={"msgs": "Ran from Airflow at {{ execution_date }}!"}
    )

    opr_sleep >> run_this