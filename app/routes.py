from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('两次密码输入不匹配，请重试')
            return redirect(url_for('register'))
            
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return render_template('login.html', message="登录成功，三秒后跳转到主页")
        else:
            flash('登录失败，请检查邮箱和密码')
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')