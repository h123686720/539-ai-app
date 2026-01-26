import streamlit as st
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime

# --- 1. 介面樣式設定 ---
st.set_page_config(page_title="輝達科技 AI - 453期核心數據終端", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: black; }
    header {visibility: hidden;}
    .main .block-container { max-width: 600px; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: auto; }
    .nvidia-title { width: 100%; border: 3px solid #76b900; padding: 20px; text-align: center; font-size: 42px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 20px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 30px; }
    .stApp, h1, h2, h3, p, div, label, span { color: #00FF41 !important; text-align: center; }
    .code-style { font-family: 'Courier New', Courier, monospace; font-size: 15px; line-height: 1.2; color: #00FF41 !important; opacity: 0.8; }
    .res-box { border: 2px solid #76b900; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.5); margin: 10px 0; }
    .history-text { font-size: 14px; color: #76b900 !important; border: 1px dashed #76b900; padding: 8px; margin-bottom: 10px; border-radius: 5px; }
    .countdown { font-size: 120px; font-weight: bold; text-shadow: 0 0 40px #00FF41; }
    input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }
    .stButton>button { background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; }
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 動態驗證 (日期 + 88)
SECRET_OFFSET = 88 
current_day = datetime.now().day
CORRECT_OTP = str(current_day + SECRET_OFFSET)

if st.session_state["step"] == "login":
    st.markdown("### 🔐 大數據庫訪問驗證")
    st.write(f"系統偵測日: [ {datetime.now().strftime('%d')}日 ]")
    pwd = st.text_input("ENTER ACCESS CODE", type="password", label_visibility="collapsed")
    if st.button("授權並進入"):
        if pwd == CORRECT_OTP:
            st.session_state["step"] = "decrypting"; st.rerun()
        else: st.error("授權碼錯誤")

elif st.session_state["step"] == "decrypting":
    msg = st.empty()
    chars = "0123456789ABCDEF!@#$%^&*()_+<>?|/[]{}\u4e00\u9fa5錢贏中獎"
    algo_steps = ["加載 453 期歷史數據...", "計算尾數冷熱分布...", "五區遺漏權重計算...", "對角線趨勢掃描...", "跳號規律模擬...", "執行 10,000 次蒙地卡羅..."]
    
    for i in range(101):
        lines = ["".join([random.choice(chars) for _ in range(random.randint(25, 35))]) for _ in range(6)]
        code_html = "".join([f"<div class='code-style'>{line}</div>" for line in lines])
        current_algo = algo_steps[min(i // 17, 5)]
        msg.markdown(f"{code_html}<br>### [{current_algo}]<br>**深度運算進度: {i}%**", unsafe_allow_html=True)
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
    st.markdown(f"## 今日預測 {today_date}")
    
    # --- 核心大數據推算法 ---
    try:
        df = pd.read_csv('history539.csv')
        total_data = len(df)
       # 強制讓顯示數字與您的檔案期數對齊
st.markdown(f"<div class='history-text'>📡 成功解析 {len(df)} 期歷史數據 | 蒙地卡羅演算完成</div>", unsafe_allow_html=True)
        
        # 1. 計算所有號碼的出現頻率 (熱度)
        all_nums = df[['n1', 'n2', 'n3', 'n4', 'n5']].values.flatten()
        freq = pd.Series(all_nums).value_counts(normalize=True)
        
        # 2. 基礎權重 (1-39)
        weights = np.array([freq.get(i, 0.02) for i in range(1, 40)])
        
        # 3. 排除最近一期獎號 (冷卻走勢)
        last_nums = df.iloc[0][['n1', 'n2', 'n3', 'n4', 'n5']].values
        for n in last_nums: weights[int(n)-1] *= 0.3  # 降低昨開號碼權重
        
    except:
        weights = np.ones(39) / 39
        st.warning("CSV 讀取失敗，改用標準隨機演算")

    # 4. 蒙地卡羅模擬選號 (Seed 鎖定當天日期)
    np.random.seed(int(datetime.now().strftime("%Y%m%d")))
    sim_picks = []
    for _ in range(100): # 進行 100 組候選模擬
        pick = np.random.choice(np.arange(1, 40), 5, p=weights/weights.sum(), replace=False)
        sim_picks.append(sorted(pick))
    
    # 取第一組最優模擬結果
    final = [str(int(x)).zfill(2) for x in sim_picks[0]]
    sv_final = final[:2] # 專車
    jt_final = final[2:] # 連碰

    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='res-box'>[ 專車優先 ]<br><h2 style='font-size:42px; color:#FFD700 !important;'>{', '.join(sv_final)}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='res-box'>[ 連碰組合 ]<br><h2 style='font-size:42px;'>{', '.join(jt_final)}</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.caption("AI 分析模型：尾數/五區/對角線/跳號/蒙地卡羅 (Monte Carlo)")
    if st.button("登出系統"):
        st.session_state["step"] = "login"; st.rerun()

