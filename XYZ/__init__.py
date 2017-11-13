from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app #引入celery实例对象
import pymysql

pymysql.install_as_MySQLdb()