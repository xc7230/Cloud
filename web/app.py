from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ai", methods=['POST'])
def ai():
    message = request.form['message']
    image = request.files['image']
    image.save('static/upload/test.jpg')
    # 인공지능으로 이미지 처리

    # 처리한 이미지를 저장

    message = message + " 잘 받았다."
    return render_template("result.html", data=message, image_path=image.filename )

@app.route("/image", methods=['POST'])
def get_image():
    image = request.files['data']
    image.save('static/upload/test.jpg')
    # 인공지능으로 이미지 처리

    # 처리한 이미지를 저장

    return "test"

if __name__ == "__main__":
    # 모델을 불러오는 부분
    app.run(host='0.0.0.0', port=5000)
