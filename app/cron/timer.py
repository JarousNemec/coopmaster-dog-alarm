import json
import logging
import random
from datetime import datetime

import cv2

from apscheduler.schedulers.background import BackgroundScheduler

from app import configuration
from app.mqtt import mqtt_helper

# todo:resize images to reduce data size
def publish_dog_alert(cfg, mqtt_client, image_topic, topic):
    logging.info("Starting task publish_dog_alert")
    values = [12, 2, 8, 4, 7, 6, 10, 0, 0, 0, 0]

    dog_count = random.choice(values)
    payload = json.dumps({"dog_count": dog_count})
    mqtt_helper.publish(mqtt_client, topic, payload)
    with open('C:/Users/mortar/PycharmProjects/CoopMaster_modules/dog_alarm/app/cron/dogo.png', 'rb') as file:
        file_content = file.read()
        byte_arr = bytearray(file_content)
        mqtt_helper.publish_bytes(mqtt_client, image_topic, byte_arr)

# todo:resize images to reduce data size
def publish_current_image(cfg, mqtt_client, topic):
    logging.info("Starting task publish_current_image")

    cam = cv2.VideoCapture("C:/Users/mortar/PycharmProjects/CoopMaster_modules/dog_alarm/app/cron/kvok_venkovni.mp4")
    currentframe = 1

    success = True
    while success:

        # reading from frame
        success, frame = cam.read()
        if currentframe % 30 == 0 and frame is not None:
            _, frame_buff = cv2.imencode('.png', frame)
            mqtt_helper.publish_bytes(mqtt_client, topic, frame_buff.tobytes())
        currentframe += 1
    cam.release()


def start_cron(cfg, mqtt_client):
    scheduler = BackgroundScheduler()

    interval = 5
    dog_alarm_topic = mqtt_helper.get_basic_topic(configuration.alarm_topic)
    dog_alarm_topic_image = mqtt_helper.get_basic_topic(configuration.alarm_topic_image)
    scheduler.add_job(lambda: publish_dog_alert(cfg, mqtt_client, dog_alarm_topic_image,dog_alarm_topic), 'interval', seconds=interval)

    # interval = 360
    image_topic = mqtt_helper.get_basic_topic(configuration.image_topic)
    scheduler.add_job(lambda: publish_current_image(cfg, mqtt_client, image_topic), 'date',
                      next_run_time=datetime.now())

    logging.getLogger('apscheduler').setLevel(logging.WARNING)
    scheduler.start()
