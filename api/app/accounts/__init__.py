from flask import Blueprint
from config import Config

accounts_bp = Blueprint('accounts', __name__, url_prefix=f"{Config.URL_PREFIX}/accounts")

from .api import *
