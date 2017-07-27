from flask import Flask,render_template,request,redirect,url_for,session
import config
from modles import User,Question,Comment
from exts import db
from decorators import login_limit

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions' : Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password==password).first()
        if user:
            session['user_id'] = user.id
            #一个月不用登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号码或密码错误'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        name = request.form.get('name')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        #手机号码验证,如果被注册,不能再注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '手机号码被注册'
        else:
            if password != password1:
                return '两次密码不同'
            else:
                #往数据库添加数据
                user = User(telephone=telephone,name=name,password=password)
                db.session.add(user)
                db.session.commit()
                #注册成功跳转到登录页面
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('index'))


@app.route('/question/',methods=['GET','POST'])
@login_limit
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        usr = User.query.filter(User.id==user_id).first()
        question.author = usr
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/',methods=['GET','POST'])
@login_limit
def detail(question_id):
    if request.method == 'GET':
        question1 = Question.query.filter(Question.id==question_id).first()
        return render_template('detail.html',question=question1)
    else:
        comment = request.form.get('comment')
        comment1 = Comment(comment=comment)
        question1 = Question.query.filter(Question.id==question_id).first()
        comment1.question = question1
        author_id =session.get('user_id')
        user = User.query.filter(User.id == author_id).first()
        comment1.author = user
        db.session.add(comment1)
        db.session.commit()
        return redirect(url_for('detail',question_id=question1.id))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()
