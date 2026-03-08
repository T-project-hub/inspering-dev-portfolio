from __future__ import annotations
import os
import io
import csv
from datetime import datetime, date
from uuid import uuid4
from typing import Optional, Iterable

from flask import (
    Flask, request, redirect, url_for, session, g, abort, flash,
    render_template_string, send_from_directory
)

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import IntegrityError
from email_validator import validate_email, EmailNotValidError
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from PIL import Image

App_Title ="In Jesus Name Amen!!!"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-change-me"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
