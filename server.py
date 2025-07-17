#render_template -> html load
from flask import render_template ,Flask, request, redirect, make_response
from aws import detect_labels_local_file as label
from aws import compare_faces as com
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index ():
    return render_template("home.html")

@app.route("/mbti", methods =["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]
            return f"당신의 MBTI는 {mbti}입니다."

    except:
        return "데이터 수신 실패"

@app.route("/detect", methods =["POST"])
def detect():
    try:
        if request.method == "POST" :
            f = request.files["file"]
            filename = secure_filename(f.filename)
            f.save("static/" + filename)
            r =label("static/" + filename)

            return r
    except:
        return"감지 실패"

@app.route("/compare", methods =["POST"])
def compare():
    try:
        if request.method == "POST" :
            f1 = request.files["file1"]
            f2 = request.files["file2"]
            filename1 = secure_filename(f1.filename)
            filename2 = secure_filename(f2.filename)
            f1.save("static/" + filename1)
            f2.save("static/" + filename2)
            r1 =com("static/" + filename1 , "static/" + filename2)
            return r1
    except:
        return"비교 실패"
    
@app.route("/login", methods = ["GET"])
def login():
    try:
        if request.method == "GET":
            login_id =request.args["login_id"]
            login_pw =request.args["login_pw"]

            if (login_id == "d") and (login_pw == "d"):

                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)
                return response
            else : 
                return redirect("/")

    except :
        return "로그인 실패"

@app.route("/login/success")
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"


if __name__ == "__main__":
    app.run(host="0.0.0.0")

