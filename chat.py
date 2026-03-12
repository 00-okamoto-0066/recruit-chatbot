
import anthropic
import time  
from dotenv import load_dotenv
import os
import database


# 会話履歴
conversation_history = [
    {"role": "assistant", "content": "ようこそ、どのようなことを知りたいか、選択してください！"}
]


# 質問に含まれるキーワードのリスト
keywords = ["募集職種","仕事","業務", "勤務地","給与", "服装", "事業内容", "応募"]


#  job_info.txt を読み込む
with open("job_info.txt","r",encoding="utf-8") as job_file:
    job_info = job_file.read()

#  読み込んだ内容を {job_info} でプロンプトに埋め込む
system_prompt = f"""\
あなたは仕事募集の問い合わせチャットボットです。
以下の募集内容をもとに、応募者からの質問に丁寧に対応して答えください。
回答できない内容の場合は「会社の問い合わせフォームから直接ご連絡ください（フォームURL：https://www.your-company.co.jp/recruit/contact）」と案内してください。


#募集内容
{job_info}
"""

# やりとりの回数をカウント
count = 0

def chat(user_questions):
    # .envファイルを読み込む
    load_dotenv()  
    # Claudeに接続する準備(API)
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # データベースを作成
    database.setup_database()


    # ユーザーの質問を受け取る
    user_input = user_questions

    # 履歴にユーザーの質問を追加 
    conversation_history.append({
        "role":"user",
        "content":user_input
    })
    # ユーザーの質問をデータベースに保存をする
    database.save_message("user",user_input)



    # キーワードがユーザーの入力に含まれているか確認
    is_keyword = any(word in user_questions for word in keywords)
    
    
    if len(conversation_history) >= 10:
        
        # Claudeの返答も履歴に追加 
        conversation_history.append({
            "role":"assistant",
            "content":"会社の問い合わせフォームから直接ご連絡ください"
        })
        # Claudeの返答をデータベースに保存をする
        database.save_message("assistant","会社の問い合わせフォームから直接ご連絡ください")
        
        return conversation_history

        
    # キーワードが含まれている場合はDBの定型文を返す
    elif is_keyword:
        
        # Claudeの返答も履歴に追加 
        conversation_history.append({
            "role":"assistant",
            "content":"定型文を送ります。"
        })
        # Claudeの返答をデータベースに保存をする
        database.save_message("assistant","定型文を送ります。")
        
        return conversation_history
        
        
    else:
        
        # Claudeに質問を送って1文字ずつ表示する
        full_response = ""

        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            temperature=0.5,
            system=system_prompt,
            # 会話履歴の直近10件だけ渡す
            messages=conversation_history[-10:]
        ) as stream:
            for text in stream.text_stream:
                full_response += text


        # Claudeの返答も履歴に追加 
        conversation_history.append({
            "role":"assistant",
            "content":full_response
        })
        # Claudeの返答をデータベースに保存をする
        database.save_message("assistant",full_response)


        return conversation_history



if __name__=="__main__":
    chat()