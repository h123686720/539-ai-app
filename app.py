import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# --- 1. 樣式設定 (保持原本的帥氣風格) ---
st.set_page_config(page_title="輝達科技 AI - 密鑰驗證系統", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: black; }
    header {visibility: hidden;}
    .main .block-container { max-width: 600px; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: auto; }
    .nvidia-title { width: 100%; border: 3px solid #76b900; padding: 20px; text-align: center; font-size: 42px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 20px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 50px; }
    .stApp, h1, h2, h3, p, div, label, span { color: #00FF41 !important; text-align: center; }
    .countdown { font-size: 150px; font-weight: bold; text-shadow: 0 0 50px #00FF41; }
    .res-box { border: 2px solid #76b900; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.5); margin: 10px 0; }
    input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }
    .stButton>button { background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; }
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# --- 2. 一次性密碼 (OTP) 邏輯設定 ---
# 這裡設定一個只有你知道的「加數」。
# 比如今天 23 號，密碼就是 23 + 88 = 111。每天都會變！
SECRET_OFFSET = 88 
current_day = datetime.now().day
CORRECT_OTP = str(current_day + SECRET_OFFSET)

# 步驟 A: 登入 (動態密鑰)
if st.session_state["step"] == "login":
    st.markdown("### 🔐 數據訪問驗證")
    st.write(f"請聯絡管理員獲取今日 [ {datetime.now().strftime('%d')}日 ] 臨時授權碼")
    pwd = st.text_input("ENTER OTP", type="password", label_visibility="collapsed")
    if st.button("啟動身份驗證"):
        if pwd == CORRECT_OTP:
            st.session_state["step"] = "decrypting"; st.rerun()
        else:
            st.error("授權碼無效或已過期")

# 步驟 B: 解密動畫
elif st.session_state["step"] == "decrypting":
    msg = st.empty()
    for i in range(50):
        code = "".join([ "錢贏中獎!@#$"[random.randint(0,7)] for _ in range(10)])
        msg.markdown(f"### [AI 核心運算中]\n## {code}\n進度: {i*2}%")
        time.sleep(0.06)
    st.session_state["step"] = "countdown"; st.rerun()

# 步驟 C: 倒數
elif st.session_state["step"] == "countdown":
    num = st.empty()
    for i in range(3, 0, -1):
        num.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.session_state["step"] = "result"; st.rerun()

# 步驟 D: 結果 (號碼從小到大排序)
elif st.session_state["step"] == "result":
    today_str = datetime.now().strftime("%Y%m%d")
    random.seed(int(today_str)) 
    
    # 產生號碼並排序
    pool = list(range(1, 40))
    recommend = random.sample(pool, 6)
    
    # 分組並排序 [從小到大]
    sv = sorted(recommend[:2])  # 專車 2 碼排序
    jt = sorted(recommend[2:])  # 連碰 4 碼排序
    
    # 轉為字串格式 (補 0)
    sv_str = [str(n).zfill(2) for n in sv]
    jt_str = [str(n).zfill(2) for n in jt]

    st.markdown(f"## 今日預測: {datetime.now().strftime('%Y/%m/%d')}")
    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='res-box'>[ 專車 ]<br><h2>{', '.join(sv_str)}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='res-box'>[ 連碰 ]<br><h2>{', '.join(jt_str)}</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("💡 系統已鎖定今日數據，登出後需重新驗證。")
    
    if st.button("登出"): st.session_state["step"] = "login"; st.rerun()
