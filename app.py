import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# --- 1. 樣式設定 ---
st.set_page_config(page_title="輝達科技 AI - 數據終端", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: black; }
    header {visibility: hidden;}
    .main .block-container { max-width: 600px; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: auto; }
    .nvidia-title { width: 100%; border: 3px solid #76b900; padding: 20px; text-align: center; font-size: 42px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 20px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 30px; }
    .stApp, h1, h2, h3, p, div, label, span { color: #00FF41 !important; text-align: center; }
    .countdown { font-size: 150px; font-weight: bold; text-shadow: 0 0 50px #00FF41; }
    .res-box { border: 2px solid #76b900; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.5); margin: 10px 0; }
    .history-text { font-size: 16px; color: #76b900 !important; border: 1px dashed #76b900; padding: 10px; margin-bottom: 15px; border-radius: 5px; }
    .code-style { font-family: 'Courier New', Courier, monospace; font-size: 18px; line-height: 1.2; color: #00FF41 !important; }
    input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }
    .stButton>button { background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; }
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 動態密碼 (日期 + 88)
SECRET_OFFSET = 88 
current_day = datetime.now().day
CORRECT_OTP = str(current_day + SECRET_OFFSET)

if st.session_state["step"] == "login":
    st.markdown("### 🔐 數據訪問驗證")
    st.write(f"請獲取今日 [ {datetime.now().strftime('%d')}日 ] 臨時授權碼")
    pwd = st.text_input("ENTER OTP", type="password", label_visibility="collapsed")
    if st.button("啟動身份驗證"):
        if pwd == CORRECT_OTP:
            st.session_state["step"] = "decrypting"; st.rerun()
        else:
            st.error("授權碼無效")

elif st.session_state["step"] == "decrypting":
    msg = st.empty()
    chars = "0123456789ABCDEF!@#$%^&*()_+<>?|/[]{}\u4e00\u9fa5" 
    for i in range(101):
        lines = ["".join([random.choice(chars) for _ in range(random.randint(20, 35))]) for _ in range(6)]
        code_html = "".join([f"<div class='code-style'>{line}</div>" for line in lines])
        msg.markdown(f"{code_html}<br>### [AI 核心數據提取中...]<br>**系統進度: {i}%**", unsafe_allow_html=True)
        time.sleep(0.04)
    st.session_state["step"] = "countdown"; st.rerun()

elif st.session_state["step"] == "countdown":
    num = st.empty()
    for i in range(3, 0, -1):
        num.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    today_date = datetime.now().strftime('%Y/%m/%d')
    st.markdown(f"## 今日預測 {today_date}")
    st.markdown(f"<div class='history-text'>📡 系統已偵測最新獎號並完成 AI 推算</div>", unsafe_allow_html=True)

    # --- 隨機推算邏輯 ---
    try:
        df = pd.read_csv('history539.csv')
        h_nums = [str(df.iloc[0][c]).zfill(2) for c in ['n1', 'n2', 'n3', 'n4', 'n5']]
    except:
        h_nums = [] # 若無 CSV 則不避開號碼

    # 以日期為種子，確保同一天內號碼固定，但每天都不同
    random.seed(int(datetime.now().strftime("%Y%m%d")))
    
    # 從 1-39 中排除掉昨天的號碼
    pool = [str(i).zfill(2) for i in range(1, 40) if str(i).zfill(2) not in h_nums]
    
    # 隨機抽取 5 個號碼 (2個給專車，3個給連碰)
    lucky_draw = sorted(random.sample(pool, 5))
    
    sv_final = lucky_draw[:2] # 前兩碼為專車
    jt_final = lucky_draw[2:] # 後三碼為連碰

    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='res-box'>[ 專車 ]<br><h2 style='font-size:38px;'>{', '.join(sv_final)}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='res-box'>[ 連碰 ]<br><h2 style='font-size:38px;'>{', '.join(jt_final)}</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("登出系統"):
        st.session_state["step"] = "login"; st.rerun()
