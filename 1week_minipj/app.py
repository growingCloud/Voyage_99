from pymongo import MongoClient
from flask import Flask, request, render_template, redirect
from flask import url_for, flash, session, jsonify, send_from_directory
from string import digits, ascii_uppercase, ascii_lowercase
import random
import os

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta_d8

BOARD_IMAGE_PATH = "/Users/mac_cloud/Desktop/images"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app.config['BOARD_IMAGE_PATH'] = BOARD_IMAGE_PATH
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

if not os.path.exists(app.config['BOARD_IMAGE_PATH']):
    os.mkdir(app.config['BOARD_IMAGE_PATH'])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def rand_generator(length=8):
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(random.sample(chars, length))


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
        name = request.form.get("name")
        img_url_left = request.form.get("img_url_left"),
        img_url_right = request.form.get("img_url_right"),
        img_title_left = request.form.get("img_title_left"),
        img_title_right = request.form.get("img_title_left"),
        contents = request.form.get("contents")

        post = {
            "name": name,
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
        # /write 경로로 들어오면 GET으로 받아 입력창 보여줌
        return render_template("post.html")


# 게시글 수정 페이지 (Update)
@app.route("/api/edit", methods=["PATCH"])
def game_edit():
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
@app.route("/api/detail", methods=["DELETE"])
def game_delete():
    idx = request.args.get("idx")
    data = db.board.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        db.board.delete_one({"_id": ObjectId(idx)})
        flash("삭제 되었습니다.")
    else:
        flash("글 삭제 권한이 없습니다.")
    return redirect(url_for("board_lists"))


# 게시글 상세 페이지 (Read)
@app.route('/view', methods=['GET'])
def board_view():
    idx = request.args.get("idx")

    if idx is not None:
        data = db.board.find_one({"_id": ObjectId(idx)})
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)