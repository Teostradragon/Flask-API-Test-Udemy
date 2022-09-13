from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from datetime import timedelta
from restdemo import db
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
      return "id={}, username={}".format(
        self.id, self.username
      )

    #通过循环遍历table,columns。
    def as_dict(self):
      return {c.name: getattr(self,c.name) for c in self.__table__.columns}
    #创建一个方法可以创建hash值
    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)

    def generate_token(self):
      # Generates the access token
      try:
        #  Set up a payload with an expiration time
        payload = {
          'exp': datetime.datetime.utcnow() + timedelta(minutes=5),
          'iat': datetime.datetime.utcnow(),
          'sub': self.username
        }
        # create the byte string token using the payload and the SECRET key
        jwt_token = jwt.encode(
          payload,
          current_app.config.get('SECRET'),
          algorithm='HS256'
        )
        return jwt_token

      except Exception as e:
          # return an error in string format if an exception occurs
          return str(e)

