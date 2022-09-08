from flask import Flask,request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
#先定义一个app，然后通过这个app实体化了一个api
api = Api(app)

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

  #get user detail information
  def get(self, username):
    for user in user_list:
      if user['username'] == username:
        return user
    return {'message': 'user not found'}, 404     #如果资源不存在返回一个404 NOT FOUND

  #create a user
  def post(self, username):
    #定义一个parser,并且只要password 这一个字段

    #data字典，当信息被调用的时候传给data。
    data = User.parser.parse_args()

    user = {
      'username': username,
      'password': data.get('password') #直接data调用就可以
    }
    for u in user_list:
      if u['username'] == username:
        return{'message': 'user already exist'}
    user_list.append(user)
    return user, 201

#delete a user
  def delete(self, username):
    user_find = None
    for user in user_list:
      if user['username'] == username:
        user_find = user
    if user_find:
      user_list.remove(user_find)
      return user_find
    else:
      return {'message': 'user not found'} , 204

#update a user
  def put(self, username):
    user_find = None
    for user in user_list:
      if user['username'] == username:
        user_find = user
    if user_find:
      data = User.parser.parse_args()
      user_list.remove(user_find)
      user_find['password'] = data['password']
      user_list.append(user_find)
      return user_find
    else:
      return{'message': 'user not found'} ,204

#新resource
class UserList(Resource):
  def get(self):
    return user_list


api.add_resource(Helloworld, '/')
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
  app.run()
