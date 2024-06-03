from airflow import DAG
from airflow.providers.sftp.sensors.sftp import SFTPSensor
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG('fetch_from_sftp', default_args=default_args, schedule_interval='@daily') as dag:

    check_file_update = SFTPSensor(
        task_id='check_file_update',
        path='/upload/test_file.txt',
        poke_interval=60,
        timeout=600,
        sftp_conn_id='sftp_default',
    )

    download_file = SFTPOperator(
        task_id='download_file',
        ssh_conn_id='sftp_default',
        local_filepath='/tmp/downloaded_test_file.txt',
        remote_filepath='/upload/test_file.txt',
        operation='get',
    )

    check_file_update >> download_file
