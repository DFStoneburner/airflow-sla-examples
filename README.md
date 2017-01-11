# airflow-sla-examples
This repository has a simple example of adding a custom notification callback to Apache Airflow's missed SLA processing.

It works by creating a DAG with a single Task that executes a Bash Operator to sleep for 15 seconds with a configured SLA of 10 seconds. When executed, the DAG will run and fail on the 'timeout' task thus executing the callback function and printing the diagnostic information.

This is captured here because the documentation does not specify this feature or show examples of using it.

# Setup
To setup and run this code:
* Create a new virtualenv to keep your site packages clean
* Install the packages listed in requirements.txt
* Start airflow webserver
* Start airflow scheduler
* Observe the output from airflow scheduler
