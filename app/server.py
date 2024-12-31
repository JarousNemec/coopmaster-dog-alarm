import logging

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask, request, jsonify
from waitress import serve
from app import configuration
from app.blueprints.admin_blueprint import admin_blueprint

from app.cron.dog_repoter import check_dog


def flask_app():
    app = Flask('__main__')

    app.config['MQTT_BROKER_URL'] = '127.0.0.1'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = 'admin'  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = 'password'  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    @app.route("/")
    def hello_world():
        logging.info("Hello World!")
        return configuration.hello_message

    app.register_blueprint(admin_blueprint)

    return app


def server():
    manager_app = flask_app()

    host = configuration.config.HOST
    port = configuration.config.PORT

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_dog, 'interval', seconds=configuration.config.REPORT_INTERVAL)
    scheduler.start()

    logging.info(f"Serving on http://{host}:{port}/api/ping")
    logging.info(f"Serving on http://{host}:{port}/api/predict")
    serve(manager_app, port=port)
