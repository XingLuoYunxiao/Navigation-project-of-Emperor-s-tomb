from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, TangLing, Itinerary, Review, Spot
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import date
import requests

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_weather_info(city_name):
    url = f"https://wttr.in/{city_name}?format=%C+%t+%w+%h"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    return "无法获取天气信息"

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
    return render_template('register.html', hide_nav=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('登录失败，请检查邮箱和密码')
    return render_template('login.html', hide_nav=True)

@app.route('/index')
@login_required
def index():
    tang_lings = TangLing.query.all()
    tang_lings_by_dynasty = {}
    for tang_ling in tang_lings:
        dynasty = tang_ling.dynasty
        if dynasty not in tang_lings_by_dynasty:
            tang_lings_by_dynasty[dynasty] = []
        tang_lings_by_dynasty[dynasty].append(tang_ling)
    
    return render_template('index.html', tang_lings_by_dynasty=tang_lings_by_dynasty)

@app.route('/tang_ling/<int:id>', methods=['GET', 'POST'])
@login_required
def tang_ling_detail(id):
    tang_ling = TangLing.query.get_or_404(id)
    reviews = Review.query.filter_by(tang_ling_id=id).all()
    spots = Spot.query.filter_by(tang_ling_id=id).all()
    city_name = "陕西"  # 城市名称以中文显示
    weather_info = get_weather_info(city_name)

    if request.method == 'POST':
        user_id = current_user.id
        content = request.form['content']
        new_review = Review(user_id=user_id, tang_ling_id=id, content=content, date=date.today())
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('tang_ling_detail', id=id))
    
    return render_template('tang_ling_detail.html', tang_ling=tang_ling, reviews=reviews, spots=spots, weather_info=weather_info, city_name=city_name)

@app.route('/itinerary')
@login_required
def itinerary():
    tang_lings = TangLing.query.all()
    itineraries = Itinerary.query.filter_by(user_id=current_user.id).all()
    return render_template('itinerary.html', tang_lings=tang_lings, itineraries=itineraries)

@app.route('/add_itinerary', methods=['POST'])
@login_required
def add_itinerary():
    tang_ling_id = request.form['tang_ling_id']
    date = request.form['date']
    description = request.form['description']
    new_itinerary = Itinerary(user_id=current_user.id, tang_ling_id=tang_ling_id, date=date, description=description)
    db.session.add(new_itinerary)
    db.session.commit()
    flash('行程已添加')
    return redirect(url_for('itinerary'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    tang_lings = TangLing.query.filter(TangLing.name.ilike(f'%{query}%')).all()
    return render_template('search_results.html', tang_lings=tang_lings)