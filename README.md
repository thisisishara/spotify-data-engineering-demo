# Spotify_Data_Engineering_Project
Simple Python ETL Project to extract Spotify Playback history using SpotifyAPI and Automate the ETL pipeline using Apache Airflow. The playlist of the user will get downloaded daily, verified and stored in a sqlite database.

# Dev Environment
*. VirtualEnv was used as the development environment
*. the venv files have not been pushed and need to be manually configured
*. setup steps may slighly differ depending on the operating system and the dev env

# Setting up the venv and installing requirements
*. install pip, python3 and upgrade to the latest versions
*. pip install virtualenv
*. python -m venv spotify-venv
*. source spotify-venv/bin/activate
*. pip install -r requirements.txt
*. additionally, change the python interpreter to the interpreter which resides within the venv just created in vscode or pycharm

# Setting up airflow (Linux)
*. pip install --upgrade pip
*. pip freeze
*. export AIRFLOW_HOME=~/usr/username/airflow
*. pip install apache-airflow

# In case airflow installation encounters rust compilation errors
*. run pip install setuptools_rust and try installing airflow again or try installing a specific version of airflow

# Airflow initialization
*. airflow db init
*. airflow webserver -p 8080
*. in a different terminal> airflow scheduler

# Airflow user account creation
*. irflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
*. [kill webserver: sudo pkill -9 -f "airflow scheduler"]