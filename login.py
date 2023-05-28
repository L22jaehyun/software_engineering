from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'secret key'

# MongoDB 클라이언트 생성
client = MongoClient('mongodb+srv://ys990728:ys3863228@cluster0.g6hx7ds.mongodb.net/?retryWrites=true&w=majority')
db = client['coin_exchange']  # MongoDB 데이터베이스 선택
users_collection = db['users']  # 사용자 컬렉션 선택
market_collection = db['market']  # 마켓 컬렉션 선택
board_collection = db['board']  # 게시판 컬렉션 선택

# 데이터베이스에 마켓 정보가 없는 경우에만 초기 마켓 정보 추가
if market_collection.count_documents({}) == 0:
    initial_coin = {'market_coin': 100, 'coinprice': 100}
    market_collection.insert_one(initial_coin)


@app.route('/', methods=['GET', 'POST'])  # 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        coinprice = market_collection.find_one()['coinprice']
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            flash("로그인에 성공했습니다!")
            return render_template('login.html', coinprice=coinprice, login=True)
        else:
            flash("존재하지 않는 회원입니다!")
            return render_template('login.html', coinprice=coinprice, register=True)
    else:
        coinprice = market_collection.find_one()['coinprice']
        if 'username' in session:
            return render_template('login.html', coinprice=coinprice, login=True)
        else:
            return render_template('login.html', coinprice=coinprice, register=True)

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

@app.route('/logout',methods=['POST']) #로그아웃
def logout():
    session.pop('username', None)
    flash("로그아웃되었습니다!")
    return redirect(url_for('login'))


@app.route('/account') #계정
def account():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        username =user.get('username')
        balance = int(user.get('balance', 0))
        coin = int(user.get('coin', 0))
        selling_coin = int(user.get('selling_coin', 0))
        
        
        market_coin = int(market_collection.find_one()['market_coin'])
        return render_template('account.html',username=username,balance=balance, coin=coin,selling_coin=selling_coin,market_coin=market_coin)
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
        deposit_amount = request.form['deposit_amount']
        if not deposit_amount.isdigit():
            flash("입금할 금액은 숫자로 입력해주세요.")
            return redirect(url_for('account'))

        deposit_amount = int(deposit_amount)
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
        withdraw_amount = request.form['withdraw_amount']
        if not withdraw_amount.isdigit():
            flash("출금할 금액은 숫자로 입력해주세요.")
            return redirect(url_for('account'))
        withdraw_amount = int(request.form['withdraw_amount'])

        # 출금 가능한 잔액보다 큰 금액을 출금하려고 하면 출금되지 않음
        if withdraw_amount > balance:
            flash("출금 가능한 잔액보다 큰 금액을 출금할 수 없습니다!")
        else:
            updated_balance = balance - withdraw_amount
            users_collection.update_one({'username': session['username']}, {'$set': {'balance': updated_balance}})
            flash("출금이 완료되었습니다!")
    return redirect(url_for('account'))

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

@app.route('/board', methods=['GET', 'POST'])
def board():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        username = user.get('username')
        balance = int(user.get('balance', 0))
        coin = int(user.get('coin', 0))

        # Calculate the total number of coins being sold by the user
        sell_list = board_collection.find({'username': username})
        selling_coin = sum(item['sell_amount'] for item in sell_list)

        sell_list = board_collection.find()  # 판매 게시글 모두 가져오기

        return render_template('board.html', username=username, balance=balance, coin=coin, selling_coin=selling_coin,
                               sell_list=sell_list)
    else:
        return redirect(url_for('login'))




@app.route('/user_sell', methods=['GET', 'POST'])
def user_sell():
    if 'username' in session:
        if request.method == 'POST':
            sell_amount = request.form['sell_amount']
            sell_price = request.form['sell_price']
            username = session['username']
            user = users_collection.find_one({'username': username})
            coin = user.get('coin', 0)

            if sell_amount.isdigit() and sell_price.isdigit():
                sell_amount = int(sell_amount)
                sell_price = int(sell_price)

                if sell_amount < 0 or sell_price < 0:
                    flash("판매 개수와 금액은 1 이상의 자연수만 입력 가능합니다!")
                elif sell_amount > coin:
                    flash("보유하고 있는 코인의 개수보다 많이 판매할 수 없습니다!")
                else:
                    board_collection.insert_one({
                        'username': username,
                        'sell_amount': sell_amount,
                        'sell_price': sell_price
                    })

                    updated_coin = coin - sell_amount
                    users_collection.update_one({'username': username}, {'$set': {'coin': updated_coin}})
                    flash("판매 게시글이 등록되었습니다.")
                    return redirect(url_for('board'))
            else:
                flash("판매 개수와 금액을 숫자로 입력해주세요.")

        sell_list = board_collection.find()
        return render_template('board.html', sell_list=sell_list)
    else:
        return redirect(url_for('login'))

@app.route('/user_sell_cancel', methods=['POST'])
def user_sell_cancel():
    if 'username' in session:
        sell_amount = int(request.form['sell_amount'])
        sell_price = int(request.form['sell_price'])
        seller_username = request.form['seller_username']

        # Delete the sell post from the board collection
        board_collection.delete_one({
            'username': seller_username,
            'sell_amount': sell_amount,
            'sell_price': sell_price
        })

        # Update the user's coin balance by adding the canceled sell amount
        users_collection.update_one(
            {'username': seller_username},
            {'$inc': {'coin': sell_amount}}
        )

        flash("판매 게시글이 취소되었습니다.")
        return redirect(url_for('board'))
    else:
        return redirect(url_for('login'))



@app.route('/user_purchase', methods=['POST'])  # 유저로부터 코인 구매
def user_purchase():
    if 'username' in session:
        user = users_collection.find_one({'username': session['username']})
        balance = user.get('balance', 0)
        coin = user.get('coin', 0)
        purchase_amount = request.form['purchase_amount']
        purchase_price = request.form['purchase_price']
        seller_username = request.form['seller_username']

        purchase_amount = int(purchase_amount)
        purchase_price = int(purchase_price)

        if purchase_amount * purchase_price > balance:
            flash("보유한 금액이 부족하여 구매할 수 없습니다!")
            return redirect(url_for('board'))

        seller = users_collection.find_one({'username': seller_username})
        seller_coin = seller.get('coin', 0)
        seller_balance = seller.get('balance', 0)

        updated_balance = balance - purchase_amount * purchase_price
        updated_coin = coin + purchase_amount
        updated_seller_balance = seller_balance + purchase_amount * purchase_price
        updated_seller_coin = seller_coin - purchase_amount

        users_collection.update_one({'username': session['username']}, {'$set': {'balance': updated_balance}})
        users_collection.update_one({'username': session['username']}, {'$set': {'coin': updated_coin}})
        users_collection.update_one({'username': seller_username}, {'$set': {'balance': updated_seller_balance}})
        users_collection.update_one({'username': seller_username}, {'$set': {'coin': updated_seller_coin}})

        board_collection.delete_one({'username': seller_username, 'sell_amount': purchase_amount, 'sell_price': purchase_price})

        flash("코인 구매가 완료되었습니다.")

        return redirect(url_for('board'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)