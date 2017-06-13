cd /home/damin/python_workspace
source /home/damin/python_workspace/flask_venv/bin/activate
export FLASK_APP=toolbox.py
export FLASK_DEBUG=True
export APPLICATION_SETTINGS=app_settings.ProductionConfig
cd /home/damin/python_workspace/toolbox
#flask run
uwsgi config.ini