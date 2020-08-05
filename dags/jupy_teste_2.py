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
    dag_id='example_notebook_xcom',
    default_args=default_args,
    catchup=False,
    schedule_interval='*/4 * * * *',
    dagrun_timeout=timedelta(minutes=60)
) as dag:

    opr_hello = BashOperator(task_id='say_Hi',
                             bash_command='echo "Hi!!"')
    
    opr_sleep = BashOperator(task_id='sleep_me',
                             bash_command='sleep 5')

    send_this = PapermillOperator(
        task_id="send",
        provide_context=True,
        input_nb="dags/notebooks/send_xcom.ipynb",
        output_nb="dags/notebooks/out-xcom.ipynb",
        parameters={"msg": "Sended"}
    )

    recive_this = PapermillOperator(
        task_id="recive",
        provide_context=True,
        input_nb="dags/notebooks/recive_xcom.ipynb",
        output_nb="dags/notebooks/out-xcom.ipynb",
        parameters={"msgs": "Recived"}
    )

    opr_hello >> send_this >> opr_sleep >> recive_this