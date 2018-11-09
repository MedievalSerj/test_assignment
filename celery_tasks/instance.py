import os
from os import getenv

import jsonlines
from celery import Celery


def configure_app(app):
    config_name = getenv('ENV', 'development').lower().capitalize()
    app.config_from_object(f'celery_tasks.config.{config_name}Config')


def create_app():
    app = Celery('celery_tasks')
    configure_app(app)
    return app


app = create_app()


@app.task
def save_to_jsonl(serializable, directory, filename):
    """Saves serializable to jsonl file
    :param serializable: any json serializable
    :param directory: path to directory to save to
    :param filename: name of the file
    """
    with jsonlines.open(os.path.join(directory, filename), 'w') as writer:
        writer.write_all(serializable)
