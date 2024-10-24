import os

host = "127.0.0.1"
port = 9008
hello_message = "Hello from dog alarm"

log_file_name = "dog_alarm.log"
modul_topic = "/dog_alarm"
wildcard_modul_topic = "/dog_alarm/#"
alarm_topic = "/alarm"
alarm_topic_image = "/alert_image"
image_topic = "/image"

def get_log_directory():
    return "./logs/"

def get_log_filename():
    return log_file_name