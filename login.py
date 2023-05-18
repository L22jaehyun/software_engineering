from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret key'

users = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                flash("로그인에 성공했습니다!")  # 로그인 성공 메시지 표시
                return redirect(url_for('account'))  # 로그인 성공 시 계정 관리 페이지로 이동
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
        flash("회원 가입에 성공했습니다!")  # 회원 가입 성공 메시지 표시
        return redirect(url_for('login'))
    else:
        return render_template('register.html', register=True)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash("로그아웃되었습니다!")  # 로그아웃 메시지 표시
    return redirect(url_for('login'))

@app.route('/account')
def account():
    if 'username' in session:
        account_number = '1234567890'  # 예시: 계좌 번호
        balance = 1000  # 예시: 잔액
        coins = ['Bitcoin', 'Ethereum', 'Litecoin']  # 예시: 보유 코인
        selling_coins = ['Ripple', 'Cardano']  # 예시: 판매 중인 코인
        return render_template('account.html', account_number=account_number, balance=balance, coins=coins, selling_coins=selling_coins)
    else:
        return redirect(url_for('login'))

@app.route('/delete-account', methods=['POST'])
def delete_account():
    # 회원 탈퇴 로직 작성
    flash("회원 탈퇴 완료")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)