from flask import Flask

app = Flask(__name__)

from cindydb.views import user, views
