import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# --- 1. 樣式設定 (保持輝達綠與駭客風格) ---
st.set_page_config(page_title="輝達科技 AI - 核心數據系統", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: black; }
    header {visibility: hidden;}
    .main .block-container { max-width: 600px; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: auto; }
    .nvidia-title { width: 100%; border: 3px solid #76b900; padding: 20px; text-align: center; font-size: 42px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 20px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 50px; }
    .stApp, h1, h2, h3, p, div, label, span { color: #00FF41 !important; text-align: center; }
    .countdown { font-size: 150px; font-weight: bold; text-shadow: 0 0 50px #00FF41; }
    .res-box { border: 2px solid #76b900; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.5); margin: 10px 0; }
    input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; font-size: 20px !important; }
    .stButton>button { background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; }
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# --- 2. 密鑰邏輯 (今日日期 + 88) ---
SECRET_OFFSET = 88 
current_day = datetime.now().day
CORRECT_OTP = str(current_day + SECRET_OFFSET)

# 步驟 A: 登入
if st.session_state["step"] == "login":
    st.markdown("### 🔐 數據訪問驗證")
    st.write(f"請聯絡管理員獲取今日 [ {datetime.now().strftime('%d')}日 ] 臨時授權碼")
    pwd = st.text_input("ENTER OTP", type="password", label_visibility="collapsed")
    if st.button("啟動身份驗證"):
        if pwd == CORRECT_OTP:
            st.session_state["step"] = "decrypting"; st.rerun()
        else:
            st.error("授權碼無效")

# 步驟 B: 解密動畫 (5秒亂碼)
elif st.session_state["step"] == "decrypting":
    msg = st.empty()
    for i in range(50):
        code = "".join([ "錢贏中獎!@#$"[random.randint(0,7)] for _ in range(10)])
        msg.markdown(f"### [AI 核心分析中]\n## {code}\n進度: {i*2}%")
        time.sleep(0.06)
    st.session_state["step"] = "countdown"; st.rerun()

# 步驟 C: 321 倒數
elif st.session_state["step"] == "countdown":
    num = st.empty()
    for i in range(3, 0, -1):
        num.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.session_state["step"] = "result"; st.rerun()

# 步驟 D: 結果顯示 (固定號碼且從小到大排序)
elif st.session_state["step"] == "result":
    # 專車號碼設定與排序
    sv_numbers = ["07", "31"]
    sv_numbers.sort()
    
    # 連碰號碼設定與排序
    jt_numbers = ["03", "11", "12"]
    jt_numbers.sort()

    st.markdown(f"## 今日預測: {datetime.now().strftime('%Y/%m/%d')}")
    st.write("")
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown(f"<div class='res-box'>[ 專車 ]<br><h2 style='font-size:40px;'>{', '.join(sv_numbers)}</h2></div>", unsafe_allow_html=True)
    with c2: 
        st.markdown(f"<div class='res-box'>[ 連碰 ]<br><h2 style='font-size:40px;'>{', '.join(jt_numbers)}</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("登出系統"):
        st.session_state["step"] = "login"; st.rerun()
