"""
A simple example showing the basics of using a custom SLA notification response.
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, datetime


# Our notification function which simply prints out some fo the information passed in to the SLA notification miss.
def print_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    print 'SLA was missed on DAG %(dag)s by task id %(blocking_tis)s with task list %(task_list)s which are blocking ' \
          '%(blocking_task_list)s' % locals()

# Set up some simple DAG args, note the email is set to None to avoid the missed SLA from creating a failure in the
# DAG. SLA emails are sent out if the SLA is missed and the email is defined, there is currently not a flag to disable.
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 1, 1),
    'email': None,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Create a basic DAG with our args
dag = DAG(
    'basic_sla',
    default_args=default_args,
    # Add our method as a SLA callback
    sla_miss_callback=print_sla_miss,
    # A common interval to make the job fire when we run it
    schedule_interval=timedelta(hours=1)
)

# Add a task that will always fail the SLA
t1 = BashOperator(
    task_id='timeout',
    # Set our task up with a 10 second SLA
    sla=timedelta(seconds=10),
    # Sleep 15 seconds to guarantee we miss the SLA
    bash_command='sleep 15',
    # Do not retry so the SLA miss fires after the first execution
    retries=0,
    dag=dag,
)
