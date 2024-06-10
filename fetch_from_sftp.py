from airflow import DAG
from airflow.providers.sftp.sensors.sftp import SFTPSensor
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG('sftp_file_monitor', default_args=default_args, schedule_interval='@daily') as dag:

    # Dummy start task
    start = DummyOperator(
        task_id='start'
    )

    # Task to monitor file changes on SFTP
    check_file_update = SFTPSensor(
        task_id='check_file_update',
        path='/upload/test_file.txt',  # Path on the SFTP server
        poke_interval=60,  # Check every 60 seconds
        timeout=600,  # Timeout after 600 seconds
        sftp_conn_id='sftp_default',
    )

    # Task to download the file from SFTP
    download_file = SFTPOperator(
        task_id='download_file',
        ssh_conn_id='sftp_default',
        local_filepath='/tmp/downloaded_test_file.txt',  # Path inside the container
        remote_filepath='/home/foo/upload/test_file.txt',  # Path on the SFTP server
        operation='get',
    )

    # Task to execute a command on Windows machine via SSH
    execute_less = SSHOperator(
        task_id='execute_less',
        ssh_conn_id='ssh_default',
        command='powershell.exe -File C:\\path\\to\\less_script.ps1'
    )

    # Dummy end task
    end = DummyOperator(
        task_id='end'
    )

    # Define task dependencies
    start >> check_file_update >> download_file >> execute_less >> end
