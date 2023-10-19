import pyautogui
from flask import Flask, render_template, request
import socket
from string import Template

app = Flask(__name__)
size = pyautogui.size()
height, width = size.height, size.width
lastX, lastY = 0, 0
position = pyautogui.position

def return_HTML(IP):
    html = """<!DOCTYPE html>
    <html lang="ja">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="shortcut icon" href="https://cdn.discordapp.com/attachments/828286173700816947/976693328487792651/3_20220519125016.png">
    <style>
        html, body{
            overflow: hidden;
            display: block;
            width: 100%%;
            height: 100%%;
            margin: 0;
            padding: 0;
        }
        #canvas {
        display: block;
        width: 100%%;
        height: 100%%;
        margin: 0;
        padding: 0;
        }
        #wrapper {
        height: 100%%;
        width: 100%%;
        }
    </style>
    </head>
    <body>
    <div id="wrapper">

    <canvas id="draw-area" style="border: 1px solid #000000;"></canvas>
    </div>

    <script>
    const IP = "http://%s:8080"

    // ページの読み込みが完了したらコールバック関数が呼ばれる
    // ※コールバック: 第2引数の無名関数(=関数名が省略された関数)
    window.addEventListener('load', () => {
    const canvas = document.querySelector('#draw-area');
    // contextを使ってcanvasに絵を書いていく
    const context = canvas.getContext('2d');

    const t = document.getElementById("pos");

    // 直前のマウスのcanvas上のx座標とy座標を記録する
    const lastPosition = { x: 0, y: 0 };
    const lastPositionx2y2 = { x1: 0, y1: 0 , x2: 0, y2: 0};

    var state = null;

    // マウスがドラッグされているか(クリックされたままか)判断するためのフラグ56
    let isDrag = false;
    let xhr = new XMLHttpRequest();

    // 絵を書く
    function draw(x, y) {
        // マウスがドラッグされていなかったら処理を中断する。
        // ドラッグしながらしか絵を書くことが出来ない。
        var sendX = (x-lastPosition.x)
        var sendY = (lastPosition.y-y)

        if (!(sendX > 50 || sendY > 50 || sendX < -50 || sendY < -50)) {
        xhr.open('GET', IP+'/get?x='+sendX+'&y='+sendY, true)
        xhr.send();
        xhr.onload = function(e) {
            if (xhr.readyState == 4) {}
        }
        }
        lastPosition.x = x;
        lastPosition.y = y;      
    }

    function scroll(event) {

        var x1 = event.touches[0].clientX;
        var y1 = event.touches[0].clientY;
        var x2 = event.touches[1].clientX;
        var y2 = event.touches[1].clientY;

        // console.log(x1, y1, x2, y2);
        if (lastPositionx2y2.y1-y1>lastPositionx2y2.y2-y2) {
        var data = lastPositionx2y2.y1 - y1;
        }
        else {
        var data = lastPositionx2y2.y2 - y2;
        }

        xhr.open('GET', IP+'/scroll?data='+data, true)
        xhr.send();
        xhr.onload = function(e) {}
    }

    // マウス操作やボタンクリック時のイベント処理を定義する
    function initEventHandler() {  
        canvas.addEventListener('touchstart', (event) => {
        state = "start"
        });
        canvas.addEventListener("touchend", (event) => {
        if (state == "start") {
            if (event.touches.length == 1) {
                xhr.open('GET', IP+'/left_click', true)
                xhr.send();
                xhr.onload = function(e) {}
            }
            state = "touchend"
        }ß
        });

        canvas.addEventListener("touchmove", (event) => {
            if (event.touches.length == 1) {
            state = "move";
            if (state != "start") {
                draw(event.layerX, event.layerY);
            }
            }
            else if (event.touches.length == 2) {
            if (state == "scroll") {
                scroll(event);
            }
            state = "scrol]l";
            lastPositionx2y2.y1 = event.touches[0].clientY;;
            lastPositionx2y2.y2 = event.touches[1].clientY;;
            }
        })
    }

    // イベント処理を初期化する
    initEventHandler();
    });

    function disableScroll(event) {
    event.preventDefault();
    }


    // イベントと関数を紐付け
    document.addEventListener('touchmove', disableScroll, { passive: false });



    let wrapper = null;				// キャンバスの親要素
    let canvas = null;					// キャンバス
    let g = null;						// コンテキスト
    let $id = function(id){ return document.getElementById(id); };	// DOM取得用
    let img = new Image();			//画像用

    /*
    * 定数
    */

    /*
    * キャンバスのサイズをウインドウに合わせて変更
    */
    function getSize(){
    // キャンバスのサイズを再設定
    canvas.width = wrapper.offsetWidth;
    canvas.height =  wrapper.offsetHeight;
    }

    /*
    * リサイズ時
    */
    window.addEventListener("resize", function(){
    getSize();
    });

    /*
    * 起動処理
    */
    window.addEventListener("load", function(){
    // キャンバスの親要素情報取得（親要素が無いとキャンバスのサイズが画面いっぱいに表示できないため）
    wrapper = $id("wrapper");
    // キャンバス情報取得
    canvas = $id("draw-area");
    g = canvas.getContext("2d");

    // キャンバスをウインドウサイズにする
    getSize();

    });

    </script>
    </body>
    </html>""" % (IP)
    return html

@app.route("/")
def main():
    global ip
    return return_HTML(IP=ip)

@app.route("/get", methods=["GET"])
def get():
    global lastX, lastY
    x = int(request.args.get("x"))*3
    y = int(request.args.get("y"))*3
    pX, pY = position().x, position().y
    if pX > width:
        pX = width
    if pY > height:
        pY = height
    if pX < 0:
        pX = 0
    if pY < 0:
        pY = 0
    pyautogui.move(x, -y)
    print(x, -y)
    return "yes"

@app.route("/right_click")
def right_click():
    pyautogui.rightClick()
    return ""

@app.route("/left_click")
def left_click():
    pyautogui.click()
    return ""

@app.route("/scroll", methods=["GET"])
def scroll():
    # x1 = request.args.get("x1")
    # y1 = request.args.get("y1")
    # x2 = request.args.get("x2")
    # y2 = request.args.get("y2")
    data = int(request.args.get("data"))
    print(data)
    # print(x1, y1, x2, y2)
    print(data)
    pyautogui.scroll(data/-5)

    return ""


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(ip)
    app.run(host="0.0.0.0", port=8080, debug=True)