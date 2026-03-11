// ボタンを押したらidを使って入力欄に文字を入れてフォームを送信する
function select_option(text){
    document.getElementById("user_questions").value = text;
    document.getElementById("chat_form").submit();
}
