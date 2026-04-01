# config.py - Application Configuration

import os

class Config:
    # Flask Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'village_sattam_secret_key_2025')

    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'village_sattam')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

    # App Settings
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True