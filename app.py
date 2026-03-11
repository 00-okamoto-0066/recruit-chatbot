from flask import Flask, request, render_template, redirect, url_for
import chat

app = Flask(__name__)

# URLを使ったときにトップページ
@app.route("/")
def home():

    return render_template("chat.html",conversation_history=chat.conversation_history)

# ユーザーの質問に関する回答を取得する
@app.route("/chat",methods=["POST"])
def chat_conversation():
    user_questions = request.form.get("user_questions")
    
    if user_questions:
        conversation_history = chat.chat(user_questions)
        return render_template("chat.html",conversation_history=conversation_history)
    
    else:
        return redirect(url_for('home'))


# アプリを起動
if __name__=="__main__":
    app.run(debug=True)