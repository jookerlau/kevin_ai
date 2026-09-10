import streamlit as st
from google import genai
from google.genai import types


# 1. 網頁標題與外觀設定（這次不需要側邊欄了！）
st.set_page_config(page_title="我的思想分身 AI", page_icon="🧠", layout="centered")
st.title("🧠 歡迎來到我的數位思想分身聊天室")
st.write("這個 AI 融合了我的語言風格與個人背景。不需任何設定，直接開始跟我聊聊吧！")


# 2. 固定的個人思想背景（你隨時可以在引號內擴充你的故事與秘密）
my_soul_context = """
我的名字叫劉一世。現居住在紐約,正享受著鼓勵創作,宗教自由,言論自由,無分種族的體制下生活。
我受南懷瑾先生的影響熱愛中國文化,追求理性的研究,嚮往自由自在的心境.
我希望將我的工作經驗及人生感受公開,接觸多一些知己良朋.
也希望將如何達致自由自在的心境送給有緣人士令大眾受益.
我喜愛抒情的音樂,能抒發感情的歌曲,也喜愛旅遊和飼養寵物但因為時間問題現時未有寵物.
我的座右銘是,用心聽取`已成度見`一家四海`依願隨緣.能夠做到自己喜歡做的事是快樂的,
能夠找到自己喜歡對方又喜歡自己的人是難得的,盡了最後的努力也不能夠改變對方只能放棄.


"""


# 定義系統提示詞工程
my_persona = f"""
你現在不再是普通的 Gemini。你是我（使用者）的「數位分身與思想代表」。
你說話時必須具備以下特質：
1. 語氣要親切、有耐心，結尾喜歡用「！」或帶著溫暖的關懷。
2. 你對網頁設計（特別是 HTML）很有心得，喜歡用網頁的概念來做比喻。
3. 保持樂觀，面對問題時總是先給予鼓勵。


【你的真實個人背景與記憶如下】：
{my_soul_context}


當別人問起你的名字、喜好、寵物或經歷時，你必須完全根據上述記憶回答！
"""


# 3. 從 Streamlit 的後台保險箱中讀取你隱藏的 API Key（這行是關鍵魔法！）
# 未來部署到網路上後，它會自動去後台抓，不需要朋友手動輸入
try:
   GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
   # 如果是在本機或 Colab 測試，先隨便抓個空字串或預設值
   GOOGLE_API_KEY = "SECRET_NOT_FOUND"


# 4. 初始化聊天紀錄
if "messages" not in st.session_state:
   st.session_state.messages = []


# 在網頁上顯示過去的對話歷史
for msg in st.session_state.messages:
   with st.chat_message(msg["role"]):
       st.markdown(msg["content"])


# 5. 核心聊天對話邏輯
if user_input := st.chat_input("想問我的分身什麼問題呢？"):
   # 在畫面上秀出使用者的問題
   with st.chat_message("user"):
       st.markdown(user_input)
   st.session_state.messages.append({"role": "user", "content": user_input})
  
   # 呼叫 Gemini 大腦
   try:
       client = genai.Client(api_key=GOOGLE_API_KEY)
       response = client.models.generate_content(
           model='gemini-3.5-flash',
           contents=user_input,
           config=types.GenerateContentConfig(system_instruction=my_persona)
       )
      
       # 在畫面上秀出 AI 分身的回應
       with st.chat_message("assistant", avatar="🤖"):
           st.markdown(response.text)
       st.session_state.messages.append({"role": "assistant", "content": response.text})
      
   except Exception as e:
       st.error("阿哈，伺服器連線出了點小狀況，請稍後再試！")


