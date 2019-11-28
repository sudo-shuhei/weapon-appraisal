import os
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, request, redirect, url_for,jsonify, render_template
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory
from base64 import b64encode
from sys import argv
import sys
import json
import requests
from judge import judge_picture

# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # print(filename, file=sys.stderr)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # アップロード後のページに転送
            descriptions = label_detection(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            print(descriptions, file = sys.stderr)
            # return redirect(url_for('uploaded_file', filename=filename))
            result = judge_picture(descriptions)
            print(result, file = sys.stderr)
            return render_template("result.html",
                attribution=result["attribution"],
                type = result["type"],
                atk = result["atk"],
                rarity = result["rarity"])

    return render_template("home.html")

@app.route('/uploads/<filename>')
# ファイルを表示する
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def label_detection(image_filenames):
    ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
    api_key = "AIzaSyCBE4RYR8Na5XC5Y5IHMwCy6D33k0J0oLk"
    print(image_filenames, file = sys.stderr)
    img_requests = []
    with open(image_filenames, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_requests.append({
                'image': {'content': ctxt},
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }]
        })

    response = requests.post(ENDPOINT_URL,
                             data=json.dumps({"requests": img_requests}).encode(),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})

    # for idx, resp in enumerate(response.json()['responses']):
    #     print(json.dumps(resp, indent=2))

    responses = response.json()['responses']
    descriptions = [d["description"] for d in responses[0]["labelAnnotations"]]
    print(descriptions, file = sys.stderr)
    return descriptions


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True, use_reloader = False)
