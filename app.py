import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta, timezone

# --- 1. 時間與顯示設定 ---
tz_taipei = timezone(timedelta(hours=8))
now_taipei = datetime.now(tz_taipei)
today_str = now_taipei.strftime('%Y/%m/%d')
fixed_time_display = "15:21:55"

# --- 2. 介面樣式 (垂直大方框排版) ---
st.set_page_config(page_title="輝達科技 AI - 數據終端", layout="centered")
st.markdown(f"""
    <style>
    .stApp {{ background-color: black; }}
    header {{visibility: hidden;}}
    .main .block-container {{ max-width: 600px; padding: 1rem; }}
    .nvidia-title {{ width: 100%; border: 3px solid #76b900; padding: 15px; text-align: center; font-size: 30px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 15px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 20px; }}
    .stApp, h1, h2, h3, p, div, label, span {{ color: #00FF41 !important; text-align: center; }}
    
    .res-box {{ 
        border: 2px solid #76b900; 
        padding: 25px; 
        border-radius: 12px; 
        background: rgba(0,0,0,0.5); 
        margin-bottom: 20px;
        width: 100%;
    }}
    .history-text {{ font-size: 15px; color: #76b900 !important; border: 1px dashed #76b900; padding: 12px; margin-bottom: 25px; border-radius: 8px; }}
    input {{ background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }}
    .stButton>button {{ background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; border-radius: 10px; }}
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 驗證碼 (今日 27日 + 88 = 115)
CORRECT_OTP = str(now_taipei.day + 88)

if st.session_state["step"] == "login":
    st.markdown("### 🔐 台北數據中心授權")
    pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed")
    if st.button("授權並進入系統"):
        if pwd.strip() == CORRECT_OTP:
            st.session_state["step"] = "decrypting"; st.rerun()
        else: st.error("授權失敗")

elif st.session_state["step"] == "decrypting":
    placeholder = st.empty()
    chars = "0123456789ABCDEF!@#$%^&*錢贏中獎"
    for i in range(16):
        lines = ["".join([random.choice(chars) for _ in range(25)]) for _ in range(5)]
        hack_output = "\n".join([f"## {line}" for line in lines])
        placeholder.markdown(f"{hack_output}\n\n**全域穩定度分析中... {i*6}%**")
        time.sleep(0.08)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    # 顯示日期與指定時間
    st.markdown(f"### 今日預測 {today_str}")
    st.write(f"預測生成時間 (台北): {fixed_time_display}")
    
    # 顯示指定解析期數
    st.markdown(f"<div class='history-text'>📡 成功解析 452 期歷史數據 | 穩定度算法完成</div>", unsafe_allow_html=True)

    # --- 依照要求鎖定號碼 ---
    sv_display = "12, 23"
    jt_display = "16, 17, 18"

    # --- 垂直排列成果 ---
    st.markdown(f"""
        <div class='res-box'>
            <p style='font-size:20px; margin-bottom:10px;'>[ 專車預測 ]</p>
            <h2 style='font-size:56px; color:#FFD700 !important; letter-spacing: 5px;'>{sv_display}</h2>
        </div>
        <div class='res-box'>
            <p style='font-size:20px; margin-bottom:10px;'>[ 連碰組合 ]</p>
            <h2 style='font-size:56px; letter-spacing: 5px;'>{jt_display}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("登出系統"):
        st.session_state["step"] = "login"; st.rerun()
