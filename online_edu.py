from flask import Flask,render_template,request
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'get':
        return render_template('login.html')
    else:
        return render_template('login.html' )

if __name__ == '__main__':
    app.run()
