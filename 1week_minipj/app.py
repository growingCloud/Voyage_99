from pymongo import MongoClient
from flask import Flask, request, render_template, redirect
from flask import url_for, flash, session, send_from_directory
from string import digits, ascii_uppercase, ascii_lowercase
import random
import os

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta_d8

# 이미지 저장 서버경로 및 허용하는 확장자
# 로컬에서는 절대경로로 "/Users/mac_cloud/Desktop/images" 로 사용함
BOARD_IMAGE_PATH = " "
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

# 업로드 하는 이미지의 크기 제한, 최대 15MB
app.config['BOARD_IMAGE_PATH'] = BOARD_IMAGE_PATH
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

# 만약 서버 저장 경로가 없으면 디렉토리 폴더를 만들어 줌
if not os.path.exists(app.config['BOARD_IMAGE_PATH']):
    os.mkdir(app.config['BOARD_IMAGE_PATH'])

# 파일을 받아올 때 확장자를 검사하는 함수
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

# 서버에 사진이 저장되었을 때 임의의 문자+숫자 조합으로 파일명을 변경 해 주는 함수
def rand_generator(length=8):
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(random.sample(chars, length))

# 이미지 업로드 관련 함수, filename을 random.jpg으로 하여 서버에 저장
@app.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = "{}.jpg".format(rand_generator())
            savefilepath = os.path.join(app.config["BOARD_IMAGE_PATH"], filename)
            file.save(savefilepath)
            return url_for("board_images", filename=filename)

@app.route('/images/<filename>')
def board_images(filename):
    return send_from_directory(app.config['BOARD_IMAGE_PATH'], filename)



@app.route('/')
def home():
    return redirect(url_for('game_create'))


# 게시글 작성 (Create)
@app.route('/post', methods=['GET', 'POST'])
def game_create():

    if request.method == "POST":
        user_id = request.form.get("user_id")
        img_url_left = request.form.get("img_url_left"),
        img_url_right = request.form.get("img_url_right"),
        img_title_left = request.form.get("img_title_left"),
        img_title_right = request.form.get("img_title_left"),
        contents = request.form.get("contents")

        post = {
            "user_id": user_id,
            "img_title_left": img_title_left,
            "img_title_right": img_title_right,
            "img_url_left": img_url_left,
            "img_url_right": img_url_right,
            "contents": contents,
        }

        idx = db.gameboard.insert_one(post)

        # SQL의 primary key와 같은 고유 번호(_id) 출력
        return redirect(url_for('game_detail', idx=idx.inserted_id))
    else:
        # /post 경로로 들어오면 GET으로 받아 입력창 보여줌
        return render_template("post.html")


# 게시글 수정 페이지 (Update)
@app.route("/api/edit", methods=["PATCH"])
def game_edit():
    idx = request.args.get("idx")

    if request.method == "GET":
        data = db.gameboard.find_one({"_id": ObjectId(idx)})
        if data is None:
            flash("해당 게시물이 존재하지 않습니다.")
            return redirect(url_for("game_lists"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template("edit.html", data=data)
            else:
                flash("글 수정 권한이 없습니다.")
                return redirect(url_for("board_lists"))
    else:
        img_title_left = request.form.get("img_title_left"),
        img_title_right = request.form.get("img_title_left"),
        img_url_left = request.form.get("img_url_left"),
        img_url_right = request.form.get("img_url_right"),
        contents = request.form.get("contents")

        data = db.gameboard.find_one({"_id": ObjectId(idx)})

        if data.get("writer_id") == session.get("id"):
            db.gameboard.update_one({"_id": ObjectId(idx)}, {
                "$set": {
                    "img_title_left": img_title_left,
                    "img_title_right": img_title_right,
                    "img_url_left": img_url_left,
                    "img_url_right": img_url_right,
                    "contents": contents,
                }
            })
            flash("수정되었습니다.")
            return redirect(url_for("game_view", idx=idx))
        else:
            flash("글 수정 권한이 없습니다.")
            return redirect(url_for("game_lists"))


# 게시글 삭제 기능 추가 (Delete)
@app.route("/api/detail", methods=["DELETE"])
def game_delete():
    idx = request.args.get("idx")
    data = db.gameboard.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        db.gameboard.delete_one({"_id": ObjectId(idx)})
    else:
        flash("글 삭제 권한이 없습니다.")
    return redirect(url_for("game_lists"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5004, debug=True)