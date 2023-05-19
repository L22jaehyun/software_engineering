from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'secret key'

# MongoDB 클라이언트 생성
client = MongoClient('mongodb+srv://ys990728:ys3863228@cluster0.g6hx7ds.mongodb.net/?retryWrites=true&w=majority')
db = client['coin_exchange']  # MongoDB 데이터베이스 선택
users_collection = db['users']  # 사용자 컬렉션 선택
<<<<<<< HEAD
market_collection = db['market'] # 마켓 컬렉션 선택
board_collection = db['board'] # 게시판 컬렉션 선택

initial_coin = {'market_coin':100,'coinprice':100}
market_collection.insert_one(initial_coin)
=======

>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)

@app.route('/', methods=['GET', 'POST']) #로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
<<<<<<< HEAD
        if request.method == 'POST':
            coinprice = market_collection.find_one()['coinprice']
            username = request.form['username']
            password = request.form['password']
            user = users_collection.find_one({'username': username, 'password': password})
            if user:
                session['username'] = username
                flash("로그인에 성공했습니다!")
                return render_template('login.html', coinprice=coinprice,login=True)
            else:
                flash("존재하지 않는 회원입니다!")
                return render_template('login.html', coinprice=coinprice,register=True)
        else:
            coinprice = market_collection.find_one()['coinprice']
            if 'username' in session:
                return render_template('login.html', coinprice=coinprice,login=True)
            else :               
                return render_template('login.html', coinprice=coinprice,register=True)
=======
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
>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)

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

<<<<<<< HEAD
@app.route('/logout',methods=['POST']) #로그아웃
=======
@app.route('/logout') #로그아웃
>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)
def logout():
    session.pop('username', None)
    flash("로그아웃되었습니다!")
    return redirect(url_for('login'))


@app.route('/account') #계정
def account():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
<<<<<<< HEAD
        username =user.get('username')
        balance = int(user.get('balance', 0))
        coin = int(user.get('coin', 0))
        selling_coin = int(user.get('selling_coin', 0))
        
        
        market_coin = int(market_collection.find_one()['market_coin'])
        return render_template('account.html',username=username,balance=balance, coin=coin,selling_coin=selling_coin,market_coin=market_coin)
=======
        balance = user.get('balance', 0)
        coin = user.get('coin', 0)
        selling_coin = user.get('selling_coin', 0)
        return render_template('account.html', balance=balance, coin=coin,
                               selling_coin=selling_coin)
>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)
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
<<<<<<< HEAD
        deposit_amount = request.form['deposit_amount']
        if not deposit_amount.isdigit():
            flash("입금할 금액은 숫자로 입력해주세요.")
            return redirect(url_for('account'))

        deposit_amount = int(deposit_amount)
=======
        deposit_amount = float(request.form['deposit_amount'])

>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)
        updated_balance = balance + deposit_amount

        users_collection.update_one({'username': session['username']}, {'$set': {'balance': updated_balance}})
        flash("입금이 완료되었습니다!")
    return redirect(url_for('account'))

<<<<<<< HEAD

=======
>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)
@app.route('/withdraw', methods=['POST'])  # 출금
def withdraw():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        balance = user.get('balance', 0)

        # 사용자가 입력한 출금할 금액
<<<<<<< HEAD
        withdraw_amount = request.form['withdraw_amount']
        if not withdraw_amount.isdigit():
            flash("출금할 금액은 숫자로 입력해주세요.")
            return redirect(url_for('account'))
        withdraw_amount = int(request.form['withdraw_amount'])
=======
        withdraw_amount = float(request.form['withdraw_amount'])
>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)

        # 출금 가능한 잔액보다 큰 금액을 출금하려고 하면 출금되지 않음
        if withdraw_amount > balance:
            flash("출금 가능한 잔액보다 큰 금액을 출금할 수 없습니다!")
        else:
            updated_balance = balance - withdraw_amount
            users_collection.update_one({'username': session['username']}, {'$set': {'balance': updated_balance}})
            flash("출금이 완료되었습니다!")
    return redirect(url_for('account'))

<<<<<<< HEAD
@app.route('/buy_market',methods=['POST']) #마켓에서 코인 구매
def buy_market():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        balance = user.get('balance', 0)
        coin = user.get('coin',0)
        buy_market = request.form['buy_market']
        market_coin = int(market_collection.find_one()['market_coin'])
        if not buy_market.isdigit():
                flash("구매할 개수는 숫자로 입력해주세요.")
                return redirect(url_for('account'))
        buy_market = int(buy_market)
        
        #마켓이 보유한 것 보다 많은 코인을 구매하려고 하면 구매가 불가능함
        if buy_market > market_coin:
            flash("마켓이 보유한 것보다 많은 개수를 구매할 수 없습니다!")
        else:
            if balance < buy_market * 100: # 사고자 하는 개수에 비해서 가진 금액이 부족할 경우
                flash("보유한 금액이 부족하여 구매할 수 없습니다!")
                return redirect(url_for('account'))
            else:
                updated_market_coin = market_coin - buy_market
                updated_balance = balance - buy_market*100
                updated_coin = coin + buy_market
                market_collection.update_one({},{'$set':{'market_coin':updated_market_coin}})
                users_collection.update_one({'username': session['username']}, {'$set': {'balance': updated_balance}})
                users_collection.update_one({'username': session['username']}, {'$set': {'coin': updated_coin}})
                flash("코인 구매가 완료되었습니다.")
                return redirect(url_for('account'))
        
    return redirect(url_for('account'))
@app.route('/board',methods=['GET','POST']) # 매매 게시판 들어갈 때
def board():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        username =user.get('username')
        balance = int(user.get('balance', 0))
        coin = int(user.get('coin', 0))
        selling_coin = int(user.get('selling_coin', 0))
               
        market_coin = int(market_collection.find_one()['market_coin'])
        return render_template('board.html',username=username,balance=balance,coin=coin,selling_coin=selling_coin)
    else:
        return redirect(url_for('login'))
@app.route('/user_buy',methods=['GET','POST']) #
def user_buy():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        username =user.get('username')
        balance = int(user.get('balance', 0))
        coin = int(user.get('coin', 0))
        selling_coin = int(user.get('selling_coin', 0))
          
        market_coin = int(market_collection.find_one()['market_coin'])
        return render_template('board.html')
    else:
        return redirect(url_for('login'))

@app.route('/user_sell',methods=['GET','POST'])
def user_sell():
    if 'username' in session:
        sell_amount = request.form['sell_amount']
        sell_price = request.form['sell_price']
        user = users_collection.find_one({'username': session['username']})
        username =user.get('username')
        balance = int(user.get('balance', 0))
        coin = int(user.get('coin', 0))
        selling_coin = int(user.get('selling_coin', 0))
        if sell_amount.isdigit() & sell_price.isdigit():
            sell_amount = int(sell_amount)
            sell_price = int(sell_price)
            if sell_amount>coin :# 보유하고 있는 코인보다 많이 팔려고 하면?
                flash("보유하고 있는 코인의 개수보다 많이 판매할 수 없습니다!")
            else:
                board_collection.insert_one
                ({
                    'username': username,
                    'sell_amount': sell_amount,
                    'balance': sell_price
                })
            updated_coin = coin - sell_amount
            updated_selling_coin = selling_coin + sell_amount
            users_collection.update_one({'username': session['username']}, {'$set': {'coin': updated_coin}})
            users_collection.update_one({'username': session['username']}, {'$set': {'selling_coin': updated_selling_coin}})
            return render_template('board.html',sell_amount=sell_amount,sell_price=sell_price,username=username,balance=balance,coin=coin,selling_coin=selling_coin)
        else:
                flash("판매 개수와 금액을 숫자로 입력해주세요.")
    else:
        return redirect(url_for('login'))
=======
>>>>>>> efe450c (출금 입금 추가 및 몽고DB 연결)
if __name__ == '__main__':
    app.run(debug=True)
