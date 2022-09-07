from flask import Flask,jsonify,request
app = Flask(__name__)

#资源存在代码，问题是没有存储型，创建的用户不存在。 所以后面要引用数据库
user_list = [
  {
    'username':'abc',
    'password':'abc'
  },
  {
    'username':'123',
    'password':'123'
  }
]


@app.route('/')
def hello_world():
  return 'Hello World!'

#抽象一种对象用户，对于用户，抽象化和对象化不明显，所以要用扩展, flask restful api

#默认方法GET，所以可以不写；rest api概念里面，一般一个api返回的对象是jason
#flask提供了一个方法jsonify,可以把python一个对象转成jason
@app.route('/users', methods=['GET'])
def get_users():
  return jsonify(user_list)

#创建用户： POST, 需要flask提供的一个方法，request,它可以获取后台传过来的jason数据
#可以转换成python的字典
@app.route('/user', methods=['POST'])
def create_user():
  user = request.get_json()
  user_check = list(
    filter(
      lambda x: user.get('username') == x['username'],
      user_list
      )
    )

  if not user_check:
    user_list.append(user)
    return jsonify({
    'message': 'user created'
  })
  else:
    return jsonify(
      {'message': 'user exist'}
    )



#测试使用postman

#Delete方法; 可以用一个URL使用不同的方法
@app.route('/user/<username>', methods=['DELETE','PUT'])
def delete_user(username):
  user_find = None
  for user in user_list:
    if user['username'] == username:
      user_find = user
  if not user_find:
      return jsonify(
        {'message': 'user not found'}
      )
  if request.method == 'DELETE':
    user_list.remove(user_find)
    return jsonify(
    {'message':'user deleted'}
  )
  elif request.method == 'PUT':
    #new_passwd = {"password": 'xxx'}
    new_passwd = request.get_json()
    user_list.remove(user_find)
    user_list.append(
      {
        'username': username,
        'password': new_passwd['password']
      }
    )
    return jsonify(
      {'message': 'user password updated'}
    )

#Update 方法



if __name__=="__main__":
  app.run()