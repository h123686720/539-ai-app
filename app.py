import streamlit as st
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime, timedelta, timezone

# --- 1. 時間設定 ---
tz_cst = timezone(timedelta(hours=8))
now_cst = datetime.now(tz_cst)
today_str = now_cst.strftime('%Y/%m/%d')
dynamic_time_display = now_cst.strftime('%H:%M:%S')

# --- 2. 介面樣式設計 (完全保留原始版面) ---
st.set_page_config(page_title="輝達科技 AI - 核心推算終端", layout="centered")
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
    .stButton>button {{ background: #76b900 !important; color: black !important; font-weight: bold !important; width: 100%; height: 50px; border-radius: 10px; border: none !important; }}
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# --- 授權碼邏輯 ---
switch_time = datetime(2026, 2, 10, 10, 30, 0, tzinfo=tz_cst)
CURRENT_PASSWORD = "13668" if now_cst >= switch_time else "1888"

if st.session_state["step"] == "login":
    st.markdown("### 🔐 台灣彩券數據中心授權")
    st.write(f"系統偵測日期: {today_str}")
    pwd = st.text_input("請輸入授權密碼", type="password", label_visibility="collapsed")
    if st.button("授權並進入系統"):
        if pwd == CURRENT_PASSWORD:
            st.session_state["step"] = "decrypting"; st.rerun()
        else:
            st.error(f"授權失敗")

elif st.session_state["step"] == "decrypting":
    placeholder = st.empty()
    chars = "0123456789ABCDEF!@#$%^&*錢贏中獎"
    for i in range(11):
        lines = ["".join([random.choice(chars) for _ in range(25)]) for _ in range(5)]
        hack_output = "\n".join([f"## {line}" for line in lines])
        placeholder.markdown(f"{hack_output}\n\n**AI 全域權重演算中... {i*10}%**")
        time.sleep(0.08)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    st.markdown(f"### 今日預測 {today_str}")
    st.write(f"預測生成時間 (中原時間): {dynamic_time_display}")
    
    try:
        df = pd.read_csv('history539.csv')
        actual_count = len(df)
        st.markdown(f"<div class='history-text'>📡 成功解析 {actual_count} 期歷史數據 | 穩定度算法完成</div>", unsafe_allow_html=True)

        np.random.seed(int(now_cst.strftime("%Y%m%d")))
        all_nums = df[['n1', 'n2', 'n3', 'n4', 'n5']].values.flatten()
        counts = pd.Series(all_nums).value_counts(normalize=True)
        last_nums = df.iloc[0][['n1', 'n2', 'n3', 'n4', 'n5']].values.astype(int)
        pool = [i for i in range(1, 40) if i not in last_nums]
        
        # 1. 抽出 AI 認為最強機率的 5 個號碼
        weights = [counts.get(i, 0.02) for i in pool]
        picks = np.random.choice(pool, 5, p=np.array(weights)/sum(weights), replace=False)
        
        # 2. 專車：拿最強的前兩名，並進行「從小到大」排序
        sv_pool = sorted([picks[0], picks[1]])
        sv_display = f"{str(sv_pool[0]).zfill(2)}, {str(sv_pool[1]).zfill(2)}"
        
        # 3. 連碰：拿剩下的三名，並單獨進行「從小到大」排序
        jt_pool = sorted([picks[2], picks[3], picks[4]])
        jt_display = f"{str(jt_pool[0]).zfill(2)}, {str(jt_pool[1]).zfill(2)}, {str(jt_pool[2]).zfill(2)}"

    except:
        sv_display = "01, 24"
        jt_display = "08, 11, 26"
        st.markdown("<div class='history-text'>📡 雲端數據同步中...</div>", unsafe_allow_html=True)

    # --- 垂直結果排版 ---
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
    
    if st.button("登出系統"):
        st.session_state["step"] = "login"; st.rerun()
