# flash  错误提示
from flask import Flask, render_template, url_for,redirect,request,flash,session
from flask_sqlalchemy import SQLAlchemy
import sys, os
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'  # windows平台
else:
    prefix = 'sqlite:////'  # Mac   Linux平台

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask
app.config['SECRET_KEY'] = '123'
db = SQLAlchemy(app)

login_manager = LoginManager(app)


# models  数据层
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

class Movies(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

@app.route('/',endpoint='index')
def index():
    user = session.get('name') 
    return render_template('index.html',user=user)

@app.route('/login/',endpoint='login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        g_username = request.form.get('username')
        g_password = request.form.get('password')
        u = User.query.filter_by(username=g_username).first()
        if u:
            if g_password == u.password:
                flash('登录成功')
                session['name'] = g_username
                return redirect(url_for('index'))
        else:
            flash('该用户不存在')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/reg/',endpoint='reg',methods=['POST','GET'])
def reg():
    if request.method == 'POST':
        g_username = request.form.get('username')
        g_password = request.form.get('password')
        u = User.query.filter_by(username=g_username).first()
        if u:
            flash('该用户已存在！！！')
            return redirect(url_for('reg.html'))
        else:
            a = User(username=g_username,password=g_password)
            db.session.add(a)
            db.session.commit()
            flash('注册成功') 
            session['name'] = g_username
            return redirect('index')
    return render_template('reg.html')

# 添加电影
@app.route('/add/',endpoint='add',methods=['POST','GET'])
def add():
    if request.method == 'POST':
         # 获取数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year)>4 or len(title)>20:
            flash('输入错误')
            return redirect(url_for('index'))
        m = Movies.query.filter_by(title=title).first()
        if m:
            flash('该电影已存在')
            return redirect(url_for('index'))
        # 保存
        movies = Movies(title=title,year=year)
        db.session.add(movies)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('index'))

# 删除电影
@app.route('/delete/<id>',endpoint='delete')
def delete(id):
    move = Movies.query.filter_by(id=id).first()
    db.session.delete(move)
    db.session.commit()
    return redirect(url_for('index'))


# 退出（注销session）
@app.route('/end/',endpoint='end')
def end():
    session.clear()
    return redirect(url_for('index'))


# 自定义404（500，其他错误都可以）  错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# 模板上下文处理函数(全局) 
@app.context_processor
def common_user():
    movies = Movies.query.all()
    return dict(movies=movies)

# 用户登录登出
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return redirect('index')



