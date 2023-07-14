from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
      return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
      return render_template('login.html')


@app.route('/dashboard')
def dashboard():
   return dashboard

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    
    return interpretation




@app.route('/result')
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
