from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'secret key'

# MongoDB 클라이언트 생성
client = MongoClient('mongodb+srv://ys990728:ys3863228@cluster0.g6hx7ds.mongodb.net/?retryWrites=true&w=majority')
db = client['coin_exchange']  # MongoDB 데이터베이스 선택
users_collection = db['users']  # 사용자 컬렉션 선택


@app.route('/', methods=['GET', 'POST']) #로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            flash("로그인에 성공했습니다!")
            return redirect(url_for('account'))
        else:
            flash("존재하지 않는 회원입니다!")
            return render_template('login.html', register=True)
    else:
        return render_template('login.html', register=True)

@app.route('/register', methods=['GET', 'POST']) #회원가입
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user:
            flash("이미 존재하는 회원입니다!")
            return render_template('register.html', register=True)
        else:
            balance = 0
            coin = 0
            selling_coin = 0
            users_collection.insert_one({
                'username': username,
                'password': password,
                'balance': balance,
                'coin': coin,
                'selling_coin': selling_coin
            })
            flash("회원 가입에 성공했습니다!")
            return redirect(url_for('login'))
    else:
        return render_template('register.html', register=True)

@app.route('/logout') #로그아웃
def logout():
    session.pop('username', None)
    flash("로그아웃되었습니다!")
    return redirect(url_for('login'))


@app.route('/account') #계정
def account():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        balance = user.get('balance', 0)
        coin = user.get('coin', 0)
        selling_coin = user.get('selling_coin', 0)
        return render_template('account.html', balance=balance, coin=coin,
                               selling_coin=selling_coin)
    else:
        return redirect(url_for('login'))


@app.route('/delete-account', methods=['POST']) #계정탈퇴
def delete_account():
    if 'username' in session:
        users_collection.delete_one({'username': session['username']})
        session.pop('username', None)
        flash("회원 탈퇴 완료")
    return redirect(url_for('login'))

@app.route('/deposit', methods=['POST'])  # 입금
def deposit():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        balance = user.get('balance', 0)

        # 사용자가 입력한 입금할 금액
        deposit_amount = float(request.form['deposit_amount'])

        updated_balance = balance + deposit_amount

        users_collection.update_one({'username': session['username']}, {'$set': {'balance': updated_balance}})
        flash("입금이 완료되었습니다!")
    return redirect(url_for('account'))

@app.route('/withdraw', methods=['POST'])  # 출금
def withdraw():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        balance = user.get('balance', 0)

        # 사용자가 입력한 출금할 금액
        withdraw_amount = float(request.form['withdraw_amount'])

        # 출금 가능한 잔액보다 큰 금액을 출금하려고 하면 출금되지 않음
        if withdraw_amount > balance:
            flash("출금 가능한 잔액보다 큰 금액을 출금할 수 없습니다!")
        else:
            updated_balance = balance - withdraw_amount
            users_collection.update_one({'username': session['username']}, {'$set': {'balance': updated_balance}})
            flash("출금이 완료되었습니다!")
    return redirect(url_for('account'))

if __name__ == '__main__':
    app.run(debug=True)
