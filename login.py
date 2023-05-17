from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret key'

users = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('home'))
        flash("존재하지 않는 회원입니다!")
        return render_template('login.html', register=True)
    else:
        return render_template('login.html', register=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users.append({'username': username, 'password': password})
        return redirect(url_for('login'))
    else:
        return render_template('register.html', register=True)

@app.route('/home')
def home():
    if 'username' in session:
        return '로그인 성공! 환영합니다, ' + session['username'] + '님!'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
