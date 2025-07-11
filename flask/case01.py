from flask import Flask,request

app = Flask(__name__)
# app.debug=True 调试模式

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #do_the_login()
        return '你执行了Post登录'
    else:
        #show_the_login_form()
        return '你执行了get登录'

@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    print(request.form)
    print(request.form['name'])
    print(request.form.get('name'))
    print(request.form.getlist('name'))
    print(request.form.get('nickname', default='little apple'))
    return 'welcome'
if __name__ == '__main__':
    app.run(port=5000, debug=True)