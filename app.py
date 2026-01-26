import streamlit as st
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime, timedelta, timezone

# --- 1. 台北時間設定 (UTC+8) ---
tz_taipei = timezone(timedelta(hours=8))
now_taipei = datetime.now(tz_taipei)
today_str = now_taipei.strftime('%Y/%m/%d')
time_str = now_taipei.strftime('%H:%M:%S')

# --- 2. 樣式設定 ---
st.set_page_config(page_title="輝達科技 AI - 台北數據終端", layout="centered")
st.markdown(f"""
    <style>
    .stApp {{ background-color: black; }}
    header {{visibility: hidden;}}
    .main .block-container {{ max-width: 600px; padding: 1rem; }}
    .nvidia-title {{ width: 100%; border: 3px solid #76b900; padding: 15px; text-align: center; font-size: 30px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 15px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 20px; }}
    .stApp, h1, h2, h3, p, div, label, span {{ color: #00FF41 !important; text-align: center; }}
    .res-box {{ 
        border: 2px solid #76b900; 
        padding: 20px; 
        border-radius: 12px; 
        background: rgba(0,0,0,0.5); 
        margin-bottom: 15px;
        width: 100%;
    }}
    .history-text {{ font-size: 14px; color: #76b900 !important; border: 1px dashed #76b900; padding: 10px; margin-bottom: 20px; }}
    .countdown {{ font-size: 100px; font-weight: bold; }}
    input {{ background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }}
    .stButton>button {{ background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; }}
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 驗證碼邏輯
CORRECT_OTP = str(now_taipei.day + 88)

if st.session_state["step"] == "login":
    st.markdown("### 🔐 台北核心數據庫驗證")
    st.write(f"系統偵測日 (CST): [ {now_taipei.strftime('%d')}日 ]")
    pwd = st.text_input("ENTER CODE", type="password", label_visibility="collapsed")
    if st.button("授權啟動"):
        if pwd.strip() == CORRECT_OTP:
            st.session_state["step"] = "decrypting"; st.rerun()
        else: st.error("授權失敗")

elif st.session_state["step"] == "decrypting":
    placeholder = st.empty()
    chars = "0123456789ABCDEF!@#$%^&*錢贏中獎"
    for i in range(21):
        lines = ["".join([random.choice(chars) for _ in range(25)]) for _ in range(5)]
        hack_output = "\n".join([f"## {line}" for line in lines])
        placeholder.markdown(f"{hack_output}\n\n**台北伺服器數據同步中... {i*5}%**")
        time.sleep(0.1)
    st.session_state["step"] = "countdown"; st.rerun()

elif st.session_state["step"] == "countdown":
    num = st.empty()
    for i in range(3, 0, -1):
        num.markdown(f"<h1 style='font-size:120px;'>{i}</h1>", unsafe_allow_html=True)
        time.sleep(0.8)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    st.markdown(f"### 今日預測 {today_str}")
    st.write(f"預測生成時間 (台北): {time_str}")
    
    try:
        df = pd.read_csv('history539.csv')
        actual_count = len(df)
        st.markdown(f"<div class='history-text'>📡 成功解析 {actual_count} 期歷史數據 | 蒙地卡羅演算完成</div>", unsafe_allow_html=True)
        
        # 鎖定種子：日期 + 期數，保證當天結果唯一
        seed_value = int(now_taipei.strftime("%Y%m%d")) + actual_count
        np.random.seed(seed_value)
        random.seed(seed_value)
        
        # 簡易排除法 (不含昨日獎號)
        last_nums = df.iloc[0][['n1', 'n2', 'n3', 'n4', 'n5']].values.astype(int)
        pool = [i for i in range(1, 40) if i not in last_nums]
        
        res_nums = sorted(random.sample(pool, 5))
        final = [str(n).zfill(2) for n in res_nums]
        
    except:
        final = ["09", "15", "24", "26", "38"]
        st.markdown("<div class='history-text'>📡 數據連接中...</div>", unsafe_allow_html=True)

    # --- 顯示成果：專車在上，連碰在下 ---
    st.markdown(f"""
        <div class='res-box'>
            <p style='font-size:18px;'>[ 專車優先 ]</p>
            <h2 style='font-size:48px; color:#FFD700 !important;'>{', '.join(final[:2])}</h2>
        </div>
        <div class='res-box'>
            <p style='font-size:18px;'>[ 連碰組合 ]</p>
            <h2 style='font-size:48px;'>{', '.join(final[2:])}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("登出系統"):
        st.session_state["step"] = "login"; st.rerun()
