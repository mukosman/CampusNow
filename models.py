import datetime
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *
from flask_mysqldb import MySQL

DATABASE = MySQLDatabase('campus_now', user='root', password='root',host='127.0.0.1', port=3306)

class user(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ("-joined_at",)

    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                )
        except IntegrityError:
            raise ValueError("Account already exists")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([user,], safe=True)
    DATABASE.close()