import time
from bson import ObjectId
from flask import *
from flask_pymongo import PyMongo
from source import output


app = Flask('Volidity')
app.config['MONGO_URI'] = 'mongodb+srv://anyone:xyz@flask.ngjrl.mongodb.net/DeFiExchange?retryWrites=true&w=majority'
mongo = PyMongo(app)
LOCK = 50 * 60

# todo figure out login system
# todo change dashboard to create
# todo create saved strat web page


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', identity='null', display=False)
    elif request.method == 'POST':
        form = dict(request.form)
        user = list(mongo.db.user.find({'user': form['user']}))
        if len(user) == 0:
            return render_template('login.html', identity='null', msg='could not find username', display=True)
        else:
            # if user['pass'] != form['pass']:
            #    return render_template('login.html', identity='null', msg='username and password do not match', display=True)
            #else:
            mongo.db.session.delete_many({'user': form['user']})
            mongo.db.session.insert_one({'user': form['user'], 'time': time.time(), 'ip': request.remote_addr, 'admin': False})
            identity = list(mongo.db.session.find({'user': form['user']}))[0]['_id']
            return redirect('/dashboard/{}'.format(identity))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html', identity='null', display=False)
    elif request.method == 'POST':
        form = dict(request.form)
        users = list(mongo.db.user.find({'user': form['user']}))
        if len(users) > 0:
            return render_template('registration.html', identity='null', msg='username already exists', display=True)
        mongo.db.user.insert_one(form)
        mongo.db.session.insert_one({'user': form['user'], 'time': time.time(), 'ip': request.remote_addr, 'admin': False})
        identity = list(mongo.db.session.find({'user': form['user']}))[0]['_id']
        return redirect('/dashboard/{}'.format(identity))



# @app.route('/dashboard/<identity>', methods=['GET', 'POST'])
# def dashboard(identity):
#     if request.method == 'GET':
#         if not verify_login(identity):
#             return redirect('/login')
#         return render_template('dashboard.html')
#     elif request.method == 'POST':
#         if not verify_login(identity):
#             return redirect('/login')


@app.route('/dashboard/<identity>', methods=['GET', 'POST'])
def dashboard(identity):
    if request.method == 'GET':
        if not verify_login(identity):
            return redirect('/login')
        return render_template('dashboard.html', identity=identity)
    elif request.method == 'POST':
        if not verify_login(identity):
            return redirect('/login')

        user = list(mongo.db.session.find({'_id': ObjectId(identity)}))[0]['user']

        form = dict(request.form)
        master = {}

        # generate name
        master['name'] = form['name']
        master['user'] = user

        # generate lookback
        start_date = form['startDate']
        start_date = start_date.split('-')
        start_date = '{}-{}-{}'.format(start_date[1], start_date[2], start_date[0])
        end_date = form['endDate']
        end_date = end_date.split('-')
        end_date = '{}-{}-{}'.format(end_date[1], end_date[2], end_date[0])
        master['lookback'] = {'startDate': start_date, 'endDate': end_date, 'step': int(form['step']), 'rollingLookbackPeriod': 520}

        # generate trade structure
        long = []
        short = []
        index = 1
        while 'type{}'.format(index) in form.keys():
            if form['type{}'.format(index)] == 'long':
                long.append({
                    'ticker': form['ticker{}'.format(index)],
                    'execution': form['execution{}'.format(index)],
                    'riskManagement': {
                        'order': form['order{}'.format(index)],
                        'takeProfit': float(form['takeProfit{}'.format(index)]),
                        'stopLoss': float(form['stopLoss{}'.format(index)]),
                        'marketOnClose': int(form['marketOnClose{}'.format(index)])
                    }
                })
            else:
                short.append({
                    'ticker': form['ticker{}'.format(index)],
                    'execution': form['execution{}'.format(index)],
                    'riskManagement': {
                        'order': form['order{}'.format(index)],
                        'takeProfit': form['takeProfit{}'.format(index)],
                        'stopLoss': form['stopLoss{}'.format(index)],
                        'marketOnClose': form['marketOnClose{}'.format(index)]
                    }
                })
            index += 1
        master['tradeStructure'] = {'long': long, 'short': short}

        # generate signals
        index = 1
        indicators = []
        while 'priceType{}'.format(index) in form.keys():
            positive = []
            negative = []
            symbol_index = 1
            # todo add threshold to html
            while 'sigType_{}_{}'.format(index, symbol_index) in form.keys():
                if 'sigType_{}_{}'.format(index, symbol_index) == 'positive':
                    positive.append({
                        'symbol': form['symbols_{}_{}'.format(index, symbol_index)],
                        'multiplier': float(form['multiplier_{}_{}'.format(index, symbol_index)])
                    })
                else:
                    negative.append({
                        'symbol': form['symbols_{}_{}'.format(index, symbol_index)],
                        'multiplier': float(form['multiplier_{}_{}'.format(index, symbol_index)])
                    })
                symbol_index += 1
            indicators.append({
                'positive': positive,
                'negative': negative,
                'aggregation': form['aggregation{}'.format(index)],
                'priceType': form['priceType{}'.format(index)],
                'thresholdType': form['thresholdType{}'.format(index)],
                'threshold': float(form['threshold{}'.format(index)]),
                'triggerType': form['triggerType{}'.format(index)],
                'triggerBias': form['triggerBias{}'.format(index)]
            })
            index += 1
        master['signals'] = {'indicators': indicators, 'combination': int(form['combination'])}
        print(master)

        mongo.db.strategies.insert_one(master)

        strat_id = list(mongo.db.strategies.find(master))[0]['_id']

        # return render_template('create.html', identity=identity, success=True)
        return redirect('/view/{}/{}'.format(identity, strat_id))


@app.route('/view/<identity>/<strategy>', methods=['GET'])
def view(identity, strategy):
    if request.method == 'GET':
        if not verify_login(identity):
            return redirect('/login')
        strategy_dic = list(mongo.db.strategies.find({'_id': ObjectId(strategy)}))[0]
        print(strategy_dic)
        datafame = output.main(strategy_dic).to_dict()
        for i in range(len(datafame['Date'])):
            x = datafame['Date'][i].split('-')
            datafame['Date'][i] = '{}-{}-{}'.format(x[2], x[0], x[1])
        print(list(datafame.keys()))
        print(datafame['Date'])
        return render_template('view.html', identity=identity, strategy=strategy_dic, datafame=datafame)


def verify_login(identity):
    print(identity)
    try:
        session = list(mongo.db.session.find({'_id': ObjectId(identity)}))
    except:
        return True
    else:
        if len(session) == 0:
            return False
        else:
            session = session[0]
            if time.time() - session['time'] > LOCK:
                mongo.db.session.delete_one({'_id': ObjectId(identity)})
                return False
            return True


if __name__ == '__main__':
    app.run(debug=True)
