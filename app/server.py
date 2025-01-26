import logging

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask, request, jsonify
from waitress import serve
from app import configuration
from app.blueprints.admin_blueprint import admin_blueprint

from app.cron.dog_repoter import check_dog


def flask_app():
    app = Flask('__main__')

    @app.route("/")
    def hello_world():
        message = 'Coopmaster dog alarm.'
        logging.info(message)
        return message

    app.register_blueprint(admin_blueprint)

    return app


def server():
    manager_app = flask_app()

    host = configuration.config.HOST
    port = configuration.config.PORT

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_dog, 'interval', seconds=configuration.config.REPORT_INTERVAL, max_instances=1)
    scheduler.start()

    logging.info(f"Serving on http://{host}:{port}/api/ping")
    logging.info(f"Serving on http://{host}:{port}/api/predict")
    serve(manager_app, port=port)
