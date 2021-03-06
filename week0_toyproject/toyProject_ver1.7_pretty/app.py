import mongo as mongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask import Flask, request, render_template, abort, redirect, url_for, flash, session, jsonify
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import time
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

client = MongoClient('mongodb://test:test@3.34.42.253', 27017)
db = client.toypractice


app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SECRET_KEY"] = "team29"


@app.route('/')
def home():
    return redirect(url_for('member_login'))


# current_time(datetime)을 우리가 보는 시간으로 바꿔주는 함수
@app.template_filter('format_datetime')
def format_datetime(value):
    if value is None:
        return ""  # 만약 시간값이 없다면 공백을 반환

    now_timestamp = time.time()  # offset = utc time과 한국의 time 시차 (+9:00)
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    value = datetime.fromtimestamp((int(value) / 1000)) + offset
    return value.strftime('%Y-%m-%d %H:%M:%S')


# 조회수 카운팅 기능
@app.route('/viewcount', methods=['POST'])
def view_count():
    view_id= request.get_json()['view_name']
    print(view_id);

    check_id = db.board.find_one({"_id": ObjectId(view_id)})
    count = check_id['view'] + 1
    db.board.update_one({"_id": ObjectId(view_id)}, {
        "$set": {
            "view": count,
        }
    })
    return jsonify({'msg':'성공'})


# 로그인 후 권한 부여 (Authority) 함수
def login_required(f):                                  # (3) 함수가 인자로 들어오므로 f를 받음
    @wraps(f)                                           # (4) 데코레이트 함
    def decorated_function(*args, **kwargs):            # (5) 데코레이티드 된 함수라는 표현
        if session.get("id") is None or session.get("id") == "":            # (6) 실제 작동하는 구간
            return redirect(url_for("member_login", next_url=request.url))  # (7) 현재 주소를 next_url이라는 변수에 넘겨줌 (request.url = login_required가 호출된 페이지의 현재 주소를 말함)
                                                                            # >> 사용자의 편의성을 위한 것임 (얘도 상대주소 개념, 로그인 제한을 걸었던 그 페이지를 현재주소로 해서 머물게 해주는 것!)
                                                                            # 예를 들어, 로그인 하지 않은 사용자가 글 작성을 눌러서 로그인을 했을때, 다시 첫 페이지로 가는 것이 아니라 글 작성 페이지에 머물게 해줌!
        return f(*args, **kwargs)                       # (8) args는 딕셔너리의 키를 얘기하는거고 kw는 키워드, 벨류 값임!
    return decorated_function


# 게시글 작성 (Create)
@app.route('/write', methods=['GET', 'POST'])
# 회원에게만 글 작성 권한 부여
@login_required                                         # (2) 하지민 모든 페이지에 이렇게 구현하기에 비효율적이라 데코레이터 기능을 사용한다
def board_write():
    if session["id"] is None or session["id"] == "":
        return redirect(url_for("member_login"))        # (1) 여기는 로그인 권한을 걸지 않았을 때 막는 방법

    if request.method == "POST":
        name = request.form.get("name")
        writer_id = session.get("id")
        title = request.form.get("title")
        contents = request.form.get("contents")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        post = {
            "writer_id": writer_id,
            "name": name,
            "title": title,
            "contents": contents,
            "view": 0,
            "pubdate": current_utc_time
        }

        idx = db.board.insert_one(post)

        flash("정상적으로 작성 되었습니다.")
        # SQL의 primary key와 같은 고유 번호(_id) 출력
        return redirect(url_for('board_view', idx=idx.inserted_id))
    else:
        # /write 경로로 들어오면 GET으로 받아 입력창 보여줌
        return render_template("write.html", name=session["name"])


# 게시글 상세 페이지 (Read)
@app.route('/view', methods=['GET'])
@login_required
def board_view():
    idx = request.args.get("idx")
    # page = request.args.get("page", 1, type=int)
    # search = request.args.get("search", -1, type=int)
    # keyword = request.args.get("keyword", "", type=str)

    if idx is not None:
        data = db.board.find_one({"_id": ObjectId(idx)})
        # data = board.find_one_and_update({"_id": ObjectId(idx)}, {"$inc": {"view": 1}}, return_document=True)
        if data is not None:
            result = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "pubdate": data.get("pubdate"),
                "writer_id": data.get("writer_id", "")
            }

            comments = db.c_comment.find({"root_idx": str(data.get("_id"))})

            return render_template("view.html", comments=list(comments), result=result)
            # return render_template("view.html", result=result, page=page, search=search, keyword=keyword)
    return abort(404)  # 맞는 페이지가 없을때 404나 400 페이지 내보내기


# 게시글 리스트 페이지 (Read_List)
@app.route('/list', methods=['GET'])
def board_lists():
    # 페이지네이션 기능 추가
    page = request.args.get("page", 1, type=int)        # page를 받아오는데, 값이 없으면 기본 1을 정수형으로 받아온다
    limit = request.args.get("limit", 100, type=int)    # 한 페이지 당 몇개의 게시물을 가져올지

    search = request.args.get("search", -1, type=int)
    keyword = request.args.get("keyword", "", type=str)

    # 최종적으로 완성된 쿼리를 만들 변수
    query = {}
    # 검색어 상태를 추가할 리스트 변수
    search_list = []

    # 검색기능 추가
    if search == 0:
        search_list.append({"title": {"$regex": keyword}})  # $regex : 안녕하세요 중에서 녕자를 검색할 수 있도록 해줌
    elif search == 1:
        search_list.append({"name": {"$regex": keyword}})

    # 검색 대상이 하나라도 존재하는 경우, query 변수에 $or 연산자로 리스트를 쿼리함
    if len(search_list) > 0:
        query = {"$or": search_list}

    search = search
    keyword = keyword

    datas = db.board.find(query).skip((page-1) * limit).limit(limit)
    # db.board.find(query) > 데이터가 몇개가 되었든 찾은 데이터는 모두 가져옴
    # skip((page-1) * limit) > 만약 페이지가 2라면, 2-1 = 1, 여기에 10을 곱하면 10, 10 ~ 19까지 출력하고 나머지를 생략하라는 의미
    # limit(limit) > 몇 개의 게시물을 가져올 지 변수 limit 만큼 함수 limit을 걸어줌
    # 의미 : 페이지가 2일때, 앞에 10개의 게시물을 스킵하고 다음 10개의 게시물을 제한하여 가져오겠다는 의미 (뒤도 생략)
    # 이걸 사용하면 1 페이지에 10개의 게시물이 보인다.


    # 페이지네이션 관련 수식 (page + navigation)
    # total_count = board.find(query).countDocuments()        # 게시물의 총 갯수
    # last_page_num = math.ceil(total_count / limit)          # 마지막 페이지의 수, 게시물이 하나라도 있으면 페이지가 존재해야 하므로 소수점이 생기면 무조건 올림!
    # block_size = 5                                          # 페이지 블럭을 5개씩 지정
    # block_num = int((page - 1) / block_size)                # 현재 게시글 블럭의 위치 : 지금 몇 페이지에 위치해 있는가?
    # block_start = int((block_size * block_num) + 1)         # 블럭의 시작 위치
    # block_end = math.ceil((block_start + block_size - 1))   # 블럭의 끝 위치

    return render_template(
        'list.html',
        datas = datas,
        limit = limit,
        page = page,
        # block_start = block_start,
        # block_end = block_end,
        # last_page_num = last_page_num,
        search = search,
        keyword = keyword)


# 게시글 수정 페이지 (Update)
@app.route("/edit", methods=["GET", "POST"])
def board_edit():
    idx = request.args.get("idx")

    if request.method == "GET":
        data = db.board.find_one({"_id": ObjectId(idx)})
        if data is None:
            flash("해당 게시물이 존재하지 않습니다.")
            return redirect(url_for("board_lists"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template("edit.html", data=data)
            else:
                flash("글 수정 권한이 없습니다.")
                return redirect(url_for("board_lists"))
    else:
        title = request.form.get("title")
        contents = request.form.get("contents")

        data = db.board.find_one({"_id": ObjectId(idx)})

        if data.get("writer_id") == session.get("id"):
            db.board.update_one({"_id": ObjectId(idx)}, {
                "$set": {
                    "title": title,
                    "contents": contents,
                }
            })
            flash("수정되었습니다.")
            return redirect(url_for("board_view", idx=idx))
        else:
            flash("글 수정 권한이 없습니다.")
            return redirect(url_for("board_lists"))


# 게시글 삭제 기능 추가 (Delete)
@app.route("/delete")
def board_delete():
    idx = request.args.get("idx")
    data = db.board.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        db.board.delete_one({"_id": ObjectId(idx)})
        flash("삭제 되었습니다.")
    else:
        flash("글 삭제 권한이 없습니다.")
    return redirect(url_for("board_lists"))


# 회원가입 페이지 (Join)
@app.route('/join', methods=['GET', 'POST'])
def member_join():
    if request.method == "GET":
        return render_template("join.html")
    else:
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass1", type=str)
        pass2 = request.form.get("pass2", type=str)

        # 가입 시 빈칸이 있을 경우
        if name == "" or email == "" or pass1 == "" or pass2 == "" :
            flash("입력되지 않은 값이 있습니다.")
            return render_template('join.html')

        # 비밀번호 확인과 일치하지 않을 경우
        #if pass1 != pass2:
         #   flash("비밀번호가 일치하지 않습니다.")
         #   return render_template('join.html')

        # 이메일(아이디) 중복 검사
        # count = members.find({"email": email}).countDocuments()
        # if count > 0:
        #     flash("중복된 이메일 주소가 있습니다.")
        #     return render_template('join.html')

        current_time = round(datetime.utcnow().timestamp() * 1000)

        addmem = {
            'name': name,
            'email': email,
            'pass1': hash_password(pass1),
            'joindate': current_time,
            'logintime': "",
            'logincount': 0
        }
        db.members.insert_one(addmem)
        return render_template('login.html')


# 로그인 페이지 (Login)
@app.route('/login', methods=['GET', 'POST'])
def member_login():
    if request.method == "GET":
        next_url = request.args.get("next_url", type=str)
        if next_url is not None:
            return render_template("login.html", next_url=next_url)
        else:
            return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("pass1")
        next_url = request.form.get("next_url", type=str)

        data = db.members.find_one({"email": email})

        if data is None:
            flash("회원정보가 없습니다.")
            return redirect(url_for("member_join"))
        else:
            if check_password(data.get("pass1"), password):
                # if data.get("pass") == check_password(password):
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True
                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for("board_lists"))
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("member_login"))


# 비밀번호 보안기능 (암호화)  추가
def hash_password(password):
    return generate_password_hash(password)


# 비밀번호 보안기능 (복호화)  추가
def check_password(hashed_password, user_password):
    return check_password_hash(hashed_password, user_password)


# 댓글기능 추가 (Comments)
@app.route("/comment_write", methods=["POST"])
@login_required
def comment_write():
    if session["id"] is None or session["id"] == "":
        return redirect(url_for("member_login"))

    if request.method == "POST":
        name = session.get("name")
        writer_id = session.get("id")
        root_idx = request.form.get("root_idx")
        comment = request.form.get("comment")
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        post = {
            "root_idx": str(root_idx),
            "writer_id": writer_id,
            "name": name,
            "comment": comment,
            "pubdate": current_utc_time,
        }

        print(post)
        idx = db.c_comment.insert_one(post)
        return redirect(url_for("board_view", idx=root_idx))
    return abort(404)


# 댓글삭제 기능 추가 (Comments_Delete) >> 작동 안함
@app.route("/comment_delete")
def comment_delete():
    idx = request.args.get("idx")
    data = db.c_comment.find_one({"_id": ObjectId(idx)})
    print(data)

    if data.get("writer_id") == session.get("id"):
        db.c_comment.delete_one({"_id": ObjectId(idx)})
        flash("삭제 되었습니다.")

    data = db.c_comment.find({"writer_id": session["id"]})
    my_id = str(data)

    if my_id == session["id"]:
        db.c_comment.delete_one({"writer_id": session["id"]})
        flash("삭제 되었습니다.")
    else:
        return redirect(url_for("board_view" + "idx?=" + idx))
    return redirect(url_for("board_view" + "idx?=" + idx))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5012, debug=True)