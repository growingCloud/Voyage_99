import mongo as mongo
from flask_pymongo import PyMongo
from flask import Flask, request, render_template, abort, redirect, url_for, flash, session, jsonify
from flask import Blueprint
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import time
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/toy_practice"
mongo = PyMongo(app)

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


# 로그인 후 권한 부여 (Authority) 함수
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member_login", next_url=request.url))
        return f(*args, **kwargs)
    return decorated_function


# 조회수 카운팅 기능
@app.route('/viewcount', methods=['POST'])
def view_count():
    view_id= request.get_json()['view_name']
    print(view_id);

    board = mongo.db.board
    check_id = board.find_one({"_id": ObjectId(view_id)})
    count = check_id['view'] + 1
    board.update_one({"_id": ObjectId(view_id)}, {
        "$set": {
            "view": count,
        }
    })
    return jsonify({'msg':'성공'})


# 게시글 작성 (Create)
@app.route('/write', methods=['GET', 'POST'])
# 회원에게만 글 작성 권한 부여
@login_required
def board_write():
    if session["id"] is None or session["id"] == "":
        return redirect(url_for("member_login"))

    if request.method == "POST":
        name = request.form.get("name")
        writer_id = session.get("id")
        title = request.form.get("title")
        contents = request.form.get("contents")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        board = mongo.db.board

        post = {
            "writer_id": writer_id,
            "name": name,
            "title": title,
            "contents": contents,
            "view": 0,
            "pubdate": current_utc_time,
        }

        print(post)
        idx = board.insert_one(post)

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
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})
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

            comment = mongo.db.comment
            comments = comment.find({"root_idx": str(data.get("_id"))})

            return render_template("view.html", comments=list(comments), result=result)
            # return render_template("view.html", result=result, page=page, search=search, keyword=keyword)
    return abort(404)  # 맞는 페이지가 없을때 404나 400 페이지 내보내기


# 게시글 리스트 페이지 (Read_List)
@app.route('/list', methods=['GET'])
def board_lists():
    # 페이지네이션 기능 추가
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 100, type=int)

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
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 2:
        search_list.append({"title": {"$regex": keyword}})
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 3:
        search_list.append({"name": {"$regex": keyword}})

    # 검색 대상이 하나라도 존재하는 경우, query 변수에 $or 연산자로 리스트를 쿼리함
    if len(search_list) > 0:
        query = {"$or": search_list}

    search = search
    keyword = keyword

    board = mongo.db.board
    datas = board.find(query).skip((page-1) * limit).limit(limit)

    # 페이지네이션 관련 수식
    # total_count = board.find(query).countDocuments()        # 게시물의 총 갯수
    # last_page_num = math.ceil(total_count / limit)          # 마지막 페이지의 수, 게시물이 하나라도 있으면 페이지가 존재해야 하므로 소수점이 생기면 무조건 올림!
    # block_size = 5                                          # 페이지 블럭을 5개씩 지정
    # block_num = int((page - 1) / block_size)                # 현재 게시글 블럭의 위치
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


# 게시글 수정 페이지 (Edit)
@app.route("/edit", methods=["GET", "POST"])
def board_edit():
    idx = request.args.get("idx")

    if request.method == "GET":
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})
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
        board = mongo.db.board

        data = board.find_one({"_id": ObjectId(idx)})

        if data.get("writer_id") == session.get("id"):
            board.update_one({"_id": ObjectId(idx)}, {
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
    board = mongo.db.board
    data = board.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id": ObjectId(idx)})
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
        members = mongo.db.members
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
        members.insert_one(addmem)
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

        members = mongo.db.members
        data = members.find_one({"email": email})

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

# 비밀번호 보안기능 추가
def hash_password(password):
    return generate_password_hash(password)
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

        c_comment = mongo.db.comment

        post = {
            "root_idx": str(root_idx),
            "writer_id": writer_id,
            "name": name,
            "comment": comment,
            "pubdate": current_utc_time,
        }

        print(post)
        x = c_comment.insert_one(post)
        return redirect(url_for("board_view", idx=root_idx))
    return abort(404)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5007, debug=True)