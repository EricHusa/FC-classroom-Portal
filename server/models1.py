from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON  # for if we need to store a json object in the DB
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

db = SQLAlchemy()

connection = psycopg2.connect(user = " ",
                                  password = "log2fopd",
                                  host = " ",
                                  port = "5432",
                                  database = "foodcomputer")

    
    cursor = connection.cursor()
    #Print PostgresSQL Connection properties
    print ( connection.get_dsn_paramaeters(), "\n")

    #Print PostgresSQL
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")


#if load does not work
def create_tables():
    #Creation of tables 
    cursor.execute('''CREATE TABLE Climate
            (id     character varying(55)     PRIMARY KEY,
            date_created     date,
            climate_file     json);''')
    print("Climate table created successfully)


    cursor.execute('''CREATE TABLE Class
            (name        character varying(50),
            students     text[],
            computer_id  uuid,
            teacher      character varying(15)[],
            FOREIGN KEY (computer_id),
            FOREIGN KEY (teacher));''')
    print("Class table created successfully")

    cursor.execute('''CREATE TABLE Computer
            (fopd_id     uuid     NOT NULL,
            name         character varying(25),
            active       boolean,
            climate      character varying(55));''')
    print("Computer table created successfully")


    cursor.execute('''CREATE TABLE Experiment
            (title       character varying(50),
            plant        character varying(25),
            description  character varying(200),
            assignment   text[],
            gif          bytea,
            start_date   date,
            computer_id  uuid,
            class_name   character varying(50)
            FOREIGN KEY (computer_id));''')
    print("Experiment table created successfully")


    cursor.execute('''CREATE TABLE Observations_<computer>_<class>
            (date         date,
            height        smallint,
            notes         character varying(200)[]);''')
    print("Observations table created successfully")


    cursor.execute('''CREATE TABLE School_user
            (username    character varying(15)[],
            password     character varying[],
            role         integer,
            PRIMARY KEY (username));''')
    print("School_user table created successfully")

    cursor.commit()
    print("All tables inserted successfully")

    
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgresSQL", error)
finally:
    #closing database connection test.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")
    
    

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # role = db.relationship('Role', backref="assignment", lazy=False)

    # hash the password upon instantiating a new User object
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return '<label {}>'.format(self.label)

    def to_dict(self):
        return dict(id=self.id,
                    name=self.label
                    )


class Example(db.Model):
    __tablename__ = 'sample'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<label {}>'.format(self.text)

    def to_dict(self):
        return dict(id=self.id,
                    text=self.text
                    )

