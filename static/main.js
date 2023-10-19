const IP = "http://10.124.51.128:8080"

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
          xhr.open('GET', IP+'/touch', true)
          xhr.send();
          xhr.onload = function(e) {}
        }
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
            state = "scroll";
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
