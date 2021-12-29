# 서버를 돌아가게 만드는 파일은 보통 'app.py'라고 이름을 많이 붙이므로 알아두자!

# 라이브러리 : 내가 짜는 코드 안으로 다른사람이 만들어 놓은 코드를 가져다 쓸 수 있음
# 프레임워크 : 다른사람이 짜둔 어떤 규칙이나 틀 안에서 내가 코딩을 자유롭게 할 수 있음

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
   # return '<button> This is Clouds Home!</button>'
   # html도 가능하다!?  하지만 이 곳에 입력하면 너무 복잡하기 때문에 전용 파일을 하나 만들어줌 (index.html)
   # 이 프레임워크는 render_template을 사용하면 알아서 templates 폴더 안에 있는 index.html을 가져다 보여줌
   return render_template('index.html')

@app.route('/test', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

@app.route('/test', methods=['POST'])
def test_post():
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

@app.route('/mypage')
def mypage():
   return 'This is myPage!'

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)