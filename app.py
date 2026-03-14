from flask import Flask, request, render_template, redirect, url_for
import chat

app = Flask(__name__)

# クイック選択ボタンの選択肢リスト（ここを変えるだけでボタンが増減できる）
options = [
    '募集職種について',
    '仕事内容・業務詳細について',
    '勤務地について',
    '給与について',
    '服装について',
    '事業内容について'
]

# URLを使ったときにトップページ
@app.route("/")
def home():

    return render_template(
        "chat.html",conversation_history=chat.conversation_history,
        options=options    
    )

# ユーザーの質問に関する回答を取得する
@app.route("/chat",methods=["POST"])
def chat_conversation():
    user_questions = request.form.get("user_questions")
    
    if user_questions:
        conversation_history = chat.chat(user_questions)
        return render_template(
            "chat.html",conversation_history=conversation_history,
            options=options,
            chat_open=True)
    
    else:
        return redirect(url_for('home'))


# アプリを起動
if __name__=="__main__":
    app.run(debug=True)