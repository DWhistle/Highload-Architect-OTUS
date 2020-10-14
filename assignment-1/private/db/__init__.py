from mysql import connector
from flask import current_app


def get_db():
    db_config = current_app.config['db']
    return connector.connect(**db_config)