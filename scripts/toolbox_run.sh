cd /home/damin/python_workspace
source flask_venv/bin/activate
export FLASK_APP=toolbox.py
export FLASK_DEBUG=1
export APPLICATION_SETTINGS=app_settings.ProductionConfig
cd toolbox
flask run