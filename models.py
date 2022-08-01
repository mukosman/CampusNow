import datetime
from choices import GENDER_CHOICES, YEAR_IN_SCHOOL_CHOICES, RACES_IN_CHOICES
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *
from flask_mysqldb import MySQL
from wtforms import StringField

DATABASE = MySQLDatabase('campus_now', user='root', password='root',host='127.0.0.1', port=3306)

class user(UserMixin, Model):
    #registration
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    #profile - personal
    name = CharField(max_length=100)
    address = StringField()
    phone = CharField(max_length = 10)
    gender = CharField(
        max_length=2,
        choices=GENDER_CHOICES,
    )
    race = CharField(
        max_length=2,
        choices=RACES_IN_CHOICES,
    )

    #Profile - Academics
    highschool = CharField(max_length = 500)
    standings = CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
    )
    gpa = CharField(max_length = 4)
    grad_year = CharField(max_length = 4)
    sat_reading_writing = CharField(max_length = 3)
    sat_math = CharField(max_length = 3)
    act = CharField(max_length = 3)

    #Profile - Interest
    preferred_major = CharField()
    alternate_major = CharField()
    sports = CharField()
    religion = CharField()


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

    @classmethod
    def update_user(cls,email,name,address,phone,gender,race,highschool,standings,gpa,grad_year,sat_math,sat_reading_writing,act,preferred_major,alternate_major,sports,religion):
        try:
            with DATABASE.transaction():
                r = cls.update(
                    name=name,
                    address= address,
                    phone = phone,
                    gender = gender,
                    race = race,
                    highschool = highschool,
                    standings = standings,
                    gpa = gpa,
                    grad_year = grad_year,
                    sat_math = sat_math,
                    sat_reading_writing = sat_reading_writing,
                    act = act,
                    preferred_major = preferred_major,
                    alternate_major = alternate_major,
                    sports = sports,
                    religion = religion,
                ).where(cls.email==email).execute()
            
                print(r)
        except IntegrityError:
            raise ValueError("Error submitting")

    

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([user,], safe=True)
    DATABASE.close()