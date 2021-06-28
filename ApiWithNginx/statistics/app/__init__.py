from flask import Flask
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

from app import views