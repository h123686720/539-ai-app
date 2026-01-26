import streamlit as st
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime

# --- 1. 介面樣式設定 (特別針對手機優化) ---
st.set_page_config(page_title="輝達科技 AI - 演算終端", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: black; }
    header {visibility: hidden;}
    .main .block-container { max-width: 600px; padding-top: 2rem; display: flex; flex-direction: column; align-items: center; }
    .nvidia-title { width: 100%; border: 3px solid #76b900; padding: 15px; text-align: center; font-size: 32px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 15px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 20px; }
    .stApp, h1, h2, h3, p, div, label, span { color: #00FF41 !important; text-align: center; }
    .code-style { font-family: 'Courier New', monospace; font-size: 14px; color: #00FF41 !important; opacity: 0.8; line-height: 1.2; }
    /* 強制手機端並排 */
    [data-testid="column"] { width: 48% !important; flex: 1 1 48% !important; min-width: 48% !important; }
    div[data-testid="stHorizontalBlock"] { display: flex; flex-wrap: nowrap !important; justify-content: space-between; gap: 10px; }
    .res-box { border: 2px solid #76b900; padding: 10px; border-radius: 10px; background: rgba(0,0,0,0.5); width: 100%; }
    .history-text { font-size: 13px; color: #76b900 !important; border: 1px dashed #76b900; padding: 8px; margin-bottom: 10px; border-radius: 5px; width: 100%; }
    .countdown { font-size: 80px; font-weight: bold; text-shadow: 0 0 30px #00FF41; }
    input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }
    .stButton>button { background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 45px; }
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 動態密碼
SECRET_OFFSET = 88 
current_day = datetime.now().day
CORRECT_OTP = str(current_day + SECRET_OFFSET)

if st.session_state["step"] == "login":
    st.markdown("### 🔐 大數據庫訪問驗證")
    st.write(f"系統偵測日: [ {datetime.now().strftime('%d')}日 ]")
    # 手機端使用 text 模式避免瀏覽器干擾
    pwd = st.text_input("ENTER ACCESS CODE", type="password", label_visibility="collapsed")
    if st.button("授權並進入"):
        if pwd.strip() == CORRECT_OTP: # 使用 strip() 去除不可見空白
            st.session_state["step"] = "decrypting"; st.rerun()
        else: st.error("授權碼錯誤")

elif st.session_state["step"] == "decrypting":
    msg = st.empty()
    chars = "0123456789ABCDEF!@#$%^&*()_+<>?錢贏中獎"
    algo_steps = ["加載歷史數據...", "尾數分布演算...", "五區遺漏掃描...", "對角趨勢分析...", "跳號機率模擬...", "蒙地卡羅模擬..."]
    for i in range(101):
        lines = ["".join([random.choice(chars) for _ in range(25)]) for _ in range(4)]
        # 修正語法錯誤
        code_html = "".join([f'<div class="code-style">{line}</div>' for line in lines])
        current_algo = algo_steps[min(i // 17, 5)]
        msg.markdown(f"{code_html}<br>### [{current_algo}]<br>**深度演算進度: {i}%**", unsafe_allow_html=True)
        time.sleep(0.04)
    st.session_state["step"] = "countdown"; st.rerun()

elif st.session_state["step"] == "countdown":
    num = st.empty()
    for i in range(3, 0, -1):
        num.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(0.8)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    today_date = datetime.now().strftime('%Y/%m/%d')
    st.markdown(f"### 今日預測 {today_date}")
    
    try:
        # 強制指定期數顯示 (處理 453 期誤差)
        df = pd.read_csv('history539.csv')
        actual_count = len(df)
        st.markdown(f"<div class='history-text'>📡 成功解析 {actual_count} 期歷史數據 | 演算完成</div>", unsafe_allow_html=True)
        
        # 權重計算
        all_nums = df[['n1', 'n2', 'n3', 'n4', 'n5']].values.flatten()
        freq = pd.Series(all_nums).value_counts(normalize=True)
        weights = np.array([freq.get(i, 0.02) for i in range(1, 40)])
        
        # 排除昨日
        last_nums = df.iloc[0][['n1', 'n2', 'n3', 'n4', 'n5']].values
        for n in last_nums: weights[int(n)-1] *= 0.1
    except:
        weights = np.ones(39) / 39
        st.warning("數據讀取中...")

    np.random.seed(int(datetime.now().strftime("%Y%m%d")))
    pick = np.random.choice(np.arange(1, 40), 5, p=weights/weights.sum(), replace=False)
    final = [str(int(x)).zfill(2) for x in sorted(pick)]

    st.write("")
    # 使用特殊的 HTML 結構強制手機並排
    col1, col2 = st.columns(2)
    with col1: st.markdown(f"<div class='res-box'>[ 專車 ]<br><h2 style='font-size:28px; color:#FFD700 !important;'>{', '.join(final[:2])}</h2></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='res-box'>[ 連碰 ]<br><h2 style='font-size:28px;'>{', '.join(final[2:])}</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("登出系統"):
        st.session_state["step"] = "login"; st.rerun()
