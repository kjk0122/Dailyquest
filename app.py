from flask import Flask, render_template, request, jsonify
import datetime as dt

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.pkogdim.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/quest", methods=["GET"])
def quest_get():
    quest_list = list(db.quest.find({}, {'_id': False}))
    return jsonify({'quests': quest_list})


@app.route("/quest", methods=["POST"])
def quest_post():
    quest_receive = request.form['quest_give']

    count = list(db.quest.find({}, {'_id': False}))
    num = len(count) + 1
    postdate = str(dt.datetime.now().year) + '. ' + str(dt.datetime.now().month) + '. ' + str(
        dt.datetime.now().day) + '. ' + str(dt.datetime.now().hour) + ':' + str(dt.datetime.now().minute) + ':' + str(
        dt.datetime.now().second)

    doc = {
        'num': num,
        'quest': quest_receive,
        'done': 0,
        'date': postdate,
        'donedate': ''
    }
    db.quest.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/quest/done", methods=["POST"])
def quest_done():
    num_receive = request.form['num_give']

    donedate = str(dt.datetime.now().year) + '. ' + str(dt.datetime.now().month) + '. ' + str(
        dt.datetime.now().day) + '. ' + str(dt.datetime.now().hour) + ':' + str(dt.datetime.now().minute) + ':' + str(
        dt.datetime.now().second)

    db.quest.update_one({'num': int(num_receive)}, {'$set': {'donedate': donedate}})
    db.quest.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '달성 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
