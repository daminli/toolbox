cd /home/damin/python_workspace
source flask_venv/bin/activate
export APPLICATION_SETTINGS=cfg.ProductionConfig
python toolbox/db_manage.py db init