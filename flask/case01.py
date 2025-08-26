from flask import Flask,request
import json

app = Flask(__name__)
# app.debug=True 调试模式
@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
def do_the_login():
    return '你执行了Post登录'
def show_the_login_form():
    name='王五'
    return f'{name}get登录方法'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        re=do_the_login()
        return re
        #return '你执行了Post登录'
    else:
        re= show_the_login_form()
        return re
        #return '你执行了get登录'

@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    # 这是json用法1
    print(request.json.get('name'))
    # 这是json用法2
    print(json.loads(request.data).get('name'))
    # 这是form用法
    print(request.form)
    print(request.form['name'])
    print(request.form.get('name'))
    print(request.form.getlist('name'))
    print(request.form.get('nickname', default='little apple'))
    return 'welcome'
if __name__ == '__main__':
    app.run(port=5000, debug=True)