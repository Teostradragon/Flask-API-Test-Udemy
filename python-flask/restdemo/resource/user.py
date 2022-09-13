from flask_restful import Resource, reqparse

from restdemo import db
from restdemo.model.user import User as UserModel

user_list = []

#password最小不能少于五个字符
def min_length_str(min_length):
  def validate(s):
    if s is None:
      raise Exception('password required')
    if not isinstance(s,(int, str)):
      raise Exception('password format error')
    s = str(s)
    if len(s) >= min_length:
      return str(s)
    raise Exception("String must be at least %i characters long" % min_length)
  return validate

#然后定义了一个Helloworld的对象，一个资源，这个资源继承了resource作为这个父类
class Helloworld(Resource):

#在class里面定义了get方法
  def get(self):
    return 'hello world'

class User(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument(
    'password', type=min_length_str(5), required=True, #检查password这个类型，是否必须
    help='{error_msg}'
  )
  parser.add_argument(
    'email', type=str, required=True, help='required email'
  )

  #get user detail information
  def get(self, username):
    user = db.session.query(UserModel).filter(
      UserModel.username == username
    ).first()
    if user:
      return user.as_dict()
    return {'message': 'user not found'}, 404     #如果资源不存在返回一个404 NOT FOUND

  #create a user
  def post(self, username):
    #定义一个parser,并且只要password 这一个字段

    #data字典，当信息被调用的时候传给data。
    data = User.parser.parse_args()
    user = db.session.query(UserModel).filter(
      UserModel.username == username
    ).first()
    if user:
      return{'message': 'user already exist'}
    user = UserModel(
      username=username,
      email = data['email']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return user.as_dict(), 201


#delete a user
  def delete(self, username):
    #先查找用户是否存在
    user = db.session.query(UserModel).filter(
      UserModel.username == username
    ).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return {'message': 'user deleted'}
    else:
      return {'message': 'user not found'}, 204


  def put(self, username):
    #update a user
    user = db.session.query(UserModel).filter(
      UserModel.username == username
    ).first()
    if user:
      data = User.parser.parse_args()
      user.password_hash = data['password']
      db.session.commit()
      return user.as_dict()
    else:
      return{'message': "user not found"}, 204


#新resource

class UserList(Resource):


  def get(self):
    users = db.session.query(UserModel).all()
    return [u.as_dict() for u in users]


