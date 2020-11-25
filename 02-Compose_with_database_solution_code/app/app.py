import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Declare our Flask application.
app = Flask(__name__)
# We attach the database URL to our application. We are using environment
# variables.
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{dbuser}:{dbpass}@db/{dbname}".format(
    dbuser=os.environ["POSTGRES_USER"],
    dbpass=os.environ["POSTGRES_PASSWORD"],
    dbname=os.environ["POSTGRES_DB"]
)

# Finally we need to initiate a DB instance so Flask can communicate with our
# database.
db = SQLAlchemy(app)


# We are defining a simple table User which store an id and a username.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# This function helps us to initialize the database by creating the table and
# inserting some datas.
def initialize_database():
    # Drop all tables in order to have a clean database on restart.
    db.drop_all()
    # Create tables schemas.
    db.create_all()
    # Add some usernames. Feel free to add or modify.
    db.session.add(User(username="Luke Skywalker"))
    db.session.add(User(username="Chewbacca"))
    db.session.add(User(username="Han Solo"))
    db.session.add(User(username="Leia Organa"))
    # Save it to actual database.
    db.session.commit()


# This is our main route.
@app.route("/")
def get_all():
    # We get all rows from table User.
    users = User.query.all()
    # We create a list of all user's username.
    users_list = [user.username for user in users]
    # We are returning a string as output:
    string_answer = f"Username in database are: {users_list}"
    return string_answer


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0")
