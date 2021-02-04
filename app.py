"""Flask app for Cupcakes"""
# .env
import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, Cupcake

# .env
load_dotenv()

app = Flask(__name__)

# .env
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcake"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)