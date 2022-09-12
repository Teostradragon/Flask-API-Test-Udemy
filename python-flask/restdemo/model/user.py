from restdemo import db


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


