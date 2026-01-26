import streamlit as st
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime

# --- 1. 樣式優化 (解決排版分離問題) ---
st.set_page_config(page_title="輝達科技 AI", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: black; }
    header {visibility: hidden;}
    .main .block-container { max-width: 600px; padding: 1rem; }
    .nvidia-title { width: 100%; border: 2px solid #76b900; padding: 15px; text-align: center; font-size: 26px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 10px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 12px; margin-bottom: 20px; }
    .stApp, h1, h2, h3, p, div, label, span { color: #00FF41 !important; text-align: center; }
    
    /* 核心修復：強制並排且不換行 */
    div[data-testid="column"] { 
        width: 48% !important; 
        flex: 1 1 48% !important; 
        min-width: 45% !important; 
    }
    div[data-testid="stHorizontalBlock"] { 
        display: flex !important; 
        flex-direction: row !important; 
        flex-wrap: nowrap !important; 
        justify-content: space-between !important;
    }
    
    .res-box { border: 2px solid #76b900; padding: 10px; border-radius: 8px; background: rgba(0,0,0,0.5); min-height: 100px; }
    .history-text { font-size: 13px; color: #76b900 !important; border: 1px dashed #76b900; padding: 8px; margin-bottom: 10px; }
    input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }
    .stButton>button { background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 45px; }
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 驗證碼
CORRECT_OTP = str(datetime.now().day + 88)

if st.session_state["step"] == "login":
    st.markdown("### 🔐 數據庫驗證")
    st.write(f"系統偵測日: [ {datetime.now().strftime('%d')}日 ]")
    pwd = st.text_input("密碼", type="password", label_visibility="collapsed")
    if st.button("授權啟動"):
        if pwd.strip() == CORRECT_OTP:
            st.session_state["step"] = "hack_anim"; st.rerun()
        else: st.error("授權失敗")

elif st.session_state["step"] == "hack_anim":
    # 這裡就是你要的黑客動畫
    placeholder = st.empty()
    chars = "0123456789ABCDEF!@#$%^&*錢贏中獎"
    for i in range(20):
        # 模擬黑客流文字
        lines = ["".join([random.choice(chars) for _ in range(15)]) for _ in range(5)]
        hack_output = "\n".join([f"### {line}" for line in lines])
        placeholder.markdown(f"{hack_output}\n\n**AI 深度演算中: {i*5}%**")
        time.sleep(0.1)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    today_date = datetime.now().strftime('%Y/%m/%d')
    st.markdown(f"### 今日預測 {today_date}")
    
    try:
        df = pd.read_csv('history539.csv')
        # 確保顯示 453 期 (如果檔案有 453 筆)
        actual_count = len(df)
        st.markdown(f"<div class='history-text'>📡 成功解析 {actual_count} 期歷史數據</div>", unsafe_allow_html=True)
        
        # 鎖定日期的演算邏輯
        np.random.seed(int(datetime.now().strftime("%Y%m%d")))
        all_nums = sorted(random.sample(range(1, 40), 5))
        final = [str(n).zfill(2) for n in all_nums]
    except:
        final = ["07", "18", "22", "31", "39"]

    # 強制並排顯示
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='res-box'>[專車]<br><h2 style='color:#FFD700;'>{', '.join(final[:2])}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='res-box'>[連碰]<br><h2>{', '.join(final[2:])}</h2></div>", unsafe_allow_html=True)
    
    if st.button("登出"):
        st.session_state["step"] = "login"; st.rerun()
