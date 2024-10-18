import os

host = "127.0.0.1"
port = 9008
hello_message = "Hello from dog alarm"

log_file_name = "dog_alarm.log"

def get_log_directory():
    return "./logs/"

def get_log_filename():
    return log_file_name