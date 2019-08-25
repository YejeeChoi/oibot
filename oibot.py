#-*- coding:utf-8 -*-
from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime
app = Flask(__name__)

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('chat.html')

## API 역할을 하는 부분
@app.route('/chat', methods=['POST'])
def chat():
   global conversation
   global nowTime

   query_message = request.form['query_give']  # 클라이언트로부터 메시지를 받는 부분

   headers = {'Content-Type': 'application/json',
              'Authorization': 'Basic a2V5OjdjYWYwZmE2MDU5YjFhZmI5ZWM1MWQ5NDE0YmE2OWU2'}
   data = str({"request": {"query": query_message}})
   response = requests.post(
      'https://builder.pingpong.us/api/builder/5d5178e4e4b0179878bfc837/integration/v0.2/custom/1', headers=headers,
      data=data.encode('utf-8'))
   receive_message = response.json()['response']['replies'][0]['text']

   conversation = {'send': query_message, 'receive': receive_message}

   time = datetime.now()
   nowTime = time.strftime('%H:%M:%S')

   return jsonify({'result': 'success', 'conversation': conversation, 'time': nowTime})

@ app.route('/chat', methods=['GET'])
def view():
   return jsonify({'result': 'success', 'conversation': conversation, 'time': nowTime})

@ app.route('/time', methods=['GET'])
def time():
   time = datetime.now()
   nowTime = time.strftime('%H:%M:%S')
   return jsonify({'result': 'success', 'time': nowTime})

# @app.route('/chat', methods=['GET'])
# def pingpong():
#    global query
#
#    headers = {'Content-Type': 'application/json',
#               'Authorization': 'Basic a2V5OjdjYWYwZmE2MDU5YjFhZmI5ZWM1MWQ5NDE0YmE2OWU2'}
#    data = str({"request": {"query": query}})
#    response = requests.post(
#       'https://builder.pingpong.us/api/builder/5d5178e4e4b0179878bfc837/integration/v0.2/custom/1', headers=headers,
#       data=data)
#
#    # print(response.json()['response']['replies'][0]['text'])
#
#    return jsonify({'result':'success', 'send': query, 'receive': response.json()['response']['replies'][0]['text']})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)