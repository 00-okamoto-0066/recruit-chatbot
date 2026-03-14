// ボタンを押したらidを使って入力欄に文字を入れてフォームを送信する
function select_option(text){
    document.getElementById("user_questions").value = text;
    document.getElementById("chat_form").submit();
}


// チャットパネルを開く(吹き出し(#chat-bubble)をクリックしたときに呼ばれる)
function openChatPanel() {

    // id="chat-panel" の要素を取得する
    const chatPanel = document.getElementById("chat-panel");

    // chat-panelに "open" クラスを追加
    // CSSの #chat-panel.open { display: flex; } が適用されて表示される
    chatPanel.classList.add("open");
}


// チャットパネルを閉じる(✕ボタン(#close-btn)をクリックしたときに呼ばれる)
function closeChatPanel() {

    // idを取得する
    const chatPanel = document.getElementById("chat-panel");

    // "open" クラスを削除して、CSSの display: none; が適用されて非表示になる
    chatPanel.classList.remove("open");
}


//  ボットの回答を1文字ずつ表示する
function typeWriter(element) {

    // バブルの中のテキストを取得して一時的に空にする
    const text = element.textContent.trim();
    element.textContent = "";

    // 何文字目まで表示したか管理する変数
    let index = 0;

    // 一定間隔で1文字ずつ追加する
    const timer = setInterval(function() {

        // 1文字追加する
        element.textContent += text[index];


        index++;

        // 全文字表示したらタイマーを止める
        if (index === text.length) {
            clearInterval(timer);
        }

    }, 30); // 30ミリ秒ごとに1文字表示（数字を大きくすると遅くなる）
}


// ページが読み込まれたときに実行する
document.addEventListener("DOMContentLoaded", function() {

    // 最後のボットのバブルだけ取得する
    const botBubbles = document.querySelectorAll(".bot-bubble");
    const lastBubble = botBubbles[botBubbles.length - 1];

    // 最後のバブルだけアニメーションを実行する
    if (lastBubble) {
        typeWriter(lastBubble);
    }
});