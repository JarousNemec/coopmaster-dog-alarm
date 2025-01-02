import json
import logging

import requests

from app import configuration


def check_dog():
    detected, actual_image = detect_dog()
    mqtt_client = configuration.get_mqtt_client()

    try:
        mqtt_client.connect()
        report_dog(mqtt_client, detected)
        publish_actual_image(mqtt_client, actual_image)
        if detected:
            publish_detected_image(mqtt_client, actual_image)
    except:
        logging.error(
            f"Could not connect to MQTT broker. No data will be published. Check connection to MQTT server")
    finally:
        mqtt_client.close()


def report_dog(mqtt_client, dog_detected):

    payload = "yes" if dog_detected else "no"

    result = mqtt_client.publish(configuration.config.MQTT_DOG_DETECTED_TOPIC, payload.encode())

    logging.info(f"Going to publish following payload to {configuration.config.MQTT_DOG_DETECTED_TOPIC}: {payload.encode()}")
    # Check if the message was successfully published
    status = result[0]
    if status == 0:
        logging.info("Dog detected status reported successfully")
    else:
        logging.error(f"Dog detected reported with error {status}")


def publish_actual_image(mqtt_client, actual_image):
    with open(actual_image, "rb") as image_file:
        image_bytes = image_file.read()

        result = mqtt_client.publish(configuration.config.MQTT_DOG_ACTUAL_IMAGE, image_bytes)

        logging.info(
            f"Going to publish following payload to {configuration.config.MQTT_DOG_ACTUAL_IMAGE}: {len(image_bytes)}")
        # Check if the message was successfully published
        status = result[0]
        if status == 0:
            logging.info("Chicken coop actual image reported successfully")
        else:
            logging.error(f"Chicken coop actual image reported with error {status}")


def publish_detected_image(mqtt_client, actual_image):
    with open(actual_image, "rb") as image_file:
        image_bytes = image_file.read()

        result = mqtt_client.publish(configuration.config.MQTT_DOG_ALARM_IMAGE, image_bytes)

        logging.info(
            f"Going to publish following payload to {configuration.config.MQTT_DOG_ALARM_IMAGE}: {len(image_bytes)}")
        # Check if the message was successfully published
        status = result[0]
        if status == 0:
            logging.info("Chicken coop actual image reported successfully")
        else:
            logging.error(f"Chicken coop actual image reported with error {status}")


def detect_dog():
    temp_img_path = get_image()
    results = configuration.model(temp_img_path)  # image you weant to predict on

    detected = False

    for result in results:
        boxes = result.boxes
        names = result.names
        for box in boxes:
            cls = box.cls  # Class ID
            conf = box.conf  # Confidence score for this detection
            # print(f"Detected class ID: {names[int(cls)]}, Confidence: {int(float(conf)*100)}")
            if names[int(cls)] == "dog":
                detected = True

    return detected, temp_img_path


def get_image():
    host = configuration.config.DOG_CAMERA_HOST
    port = configuration.config.DOG_CAMERA_PORT

    url = f'http://{host}:{port}/api/dog/image'

    try:
        response = requests.get(url)
        response.raise_for_status()
        image = 'dog.jpg'
        with open(image, 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)
            file.close()

        return image
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the HTTP request
        print(f"An error occurred: {e}")
