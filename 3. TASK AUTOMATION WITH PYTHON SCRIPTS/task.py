import os
import shutil
import logging
from datetime import datetime
import schedule
import time
import configparser
import tkinter as tk
from tkinter import filedialog


logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='a'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


config = configparser.ConfigParser()
config_file = 'config.ini'

if not os.path.exists(config_file):
    logging.error('Configuration file config.ini not found.')
    print('Configuration file config.ini not found.')
    exit(1)

config.read(config_file)

FILE_TYPES = {
    'Documents': ['.pdf', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx', '.csv', '.odt', '.ods', '.odp', '.rtf'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
    'Music': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Scripts': ['.py', '.js', '.html', '.css', '.php', '.java', '.c', '.cpp', '.rb', '.sh', '.bat'],
    
}

def scan_directory(target_dir):
    
    logging.info(f'Scanning directory: {target_dir}')
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            category = get_file_category(file_ext)
            if category:
                move_file(file_path, category, target_dir)
            else:
                logging.info(f'No category found for file: {file}')

def get_file_category(file_ext):
    
    for category, extensions in FILE_TYPES.items():
        if file_ext in extensions:
            return category
    return None

def move_file(file_path, category, target_dir):
    
    category_dir = os.path.join(target_dir, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)
    dest_path = os.path.join(category_dir, os.path.basename(file_path))
    if os.path.exists(dest_path):
        dest_path = resolve_conflict(dest_path)
    shutil.move(file_path, dest_path)
    logging.info(f'Moved {file_path} to {dest_path}')

def resolve_conflict(file_path):
    
    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
    return new_file_path

def schedule_task(interval_minutes, target_dir):
    
    schedule.every(interval_minutes).minutes.do(scan_directory, target_dir)
    while True:
        schedule.run_pending()
        time.sleep(1)

def select_directory():
    
    root = tk.Tk()
    root.withdraw()
    target_dir = filedialog.askdirectory()
    return target_dir

if __name__ == '__main__':
    target_directory = select_directory()
    if target_directory:
        scan_directory(target_directory)
        try:
            interval = int(config['SETTINGS']['IntervalMinutes'])
            schedule_task(interval, target_directory)
        except KeyError:
            logging.error("Configuration key 'IntervalMinutes' not found in config.ini.")
            print("Configuration key 'IntervalMinutes' not found in config.ini.")
        except ValueError:
            logging.error("Invalid value for 'IntervalMinutes' in config.ini.")
            print("Invalid value for 'IntervalMinutes' in config.ini.")
    else:
        print("No directory selected.")
