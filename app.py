import streamlit as st
import pandas as pd
from collections import Counter
import time
from datetime import datetime

# --- 1. 頁面配置與駭客背景 ---
st.set_page_config(page_title="輝達科技 AI", layout="centered")

st.markdown("""
    <style>
    /* 1. 背景全黑，隱藏所有原廠裝飾 */
    .stApp { background-color: black; }
    header {visibility: hidden;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    
    /* 2. 移除所有內容外框 (關鍵點) */
    .stAppViewBlockContainer { padding-top: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }

    /* 3. 強制置中容器 */
    .main .block-container {
        max-width: 600px;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: auto;
    }

    /* 4. 輝達科技 AI 標題 (保留這個框) */
    .nvidia-title {
        width: 100%;
        border: 3px solid #76b900;
        padding: 20px;
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #76b900 !important;
        text-shadow: 0 0 20px #76b900;
        background: rgba(0, 0, 0, 0.9);
        border-radius: 15px;
        margin-bottom: 40px;
    }

    /* 5. 駭客動畫畫布 */
    #matrix-canvas {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
    }

    /* 文字樣式 */
    .stApp, h1, h2, h3, p, div, label, span { 
        color: #00FF41 !important; 
        font-family: 'Microsoft JhengHei', sans-serif; 
        text-align: center;
    }
    .countdown { font-size: 150px; font-weight: bold; text-shadow: 0 0 50px #00FF41; margin: 30px 0; }
    .decrypt-text { font-size: 24px; font-family: 'Courier New', monospace; margin: 20px 0; }
    .res-box { border: 2px solid #76b900; padding: 20px; border-radius: 10px; background: rgba(0,0,0,0.5); }

    /* 輸入框與按鈕自訂 (無外框感) */
    input { 
        background-color: #0d0d0d !important; 
        color: #00FF41 !important; 
        border: 1px solid #00FF41 !important; 
        text-align: center !important; 
        font-size: 20px !important;
    }
    .stButton>button { 
        background: transparent !important; 
        color: #00FF41 !important; 
        border: 1px solid #00FF41 !important; 
        height: 60px; font-size: 24px; width: 100%;
        margin-top: 20px;
    }
    .stButton>button:hover { background: #00FF41 !important; color: black !important; }
    </style>
    
    <canvas id="matrix-canvas"></canvas>
    <script>
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.onresize = resize; resize();
        const alphabet = "錢贏中獎發財539密碼$#@!*&%0123456789".split("");
        const fontSize = 19;
        const columns = Math.floor(canvas.width / fontSize);
        const drops = [];
        for (let x = 0; x < columns; x++) drops[x] = 1;
        function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.1)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0"; ctx.font = fontSize + "px monospace";
            for (let i = 0; i < drops.length; i++) {
                const text = alphabet[Math.floor(Math.random() * alphabet.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 35);
    </script>
    """, unsafe_allow_html=True)

# --- 2. 邏輯處理 ---
if "step" not in st.session_state:
    st.session_state["step"] = "login"

# 固定的輝達標題
st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 步驟區分
if st.session_state["step"] == "login":
    st.markdown("### 🔐 數據訪問驗證")
    pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed")
    if st.button("啟動身份驗證"):
        if pwd == "539":
            st.session_state["step"] = "decrypting"
            st.rerun()
        else:
            st.error("驗證失敗")

elif st.session_state["step"] == "decrypting":
    st.markdown("### 📡 雲端數據計算中...")
    msg = st.empty()
    symbols = "!@#$%^&*錢贏中獎"
    for i in range(50):
        code = "".join([symbols[int(time.time()*100+j)%len(symbols)] for j in range(12)])
        msg.markdown(f"<div class='decrypt-text'>[AI_ANALYSIS]: {code}<br>PROGRESS: {i*2}%</div>", unsafe_allow_html=True)
        time.sleep(0.1)
    st.session_state["step"] = "countdown"
    st.rerun()

elif st.session_state["step"] == "countdown":
    num_area = st.empty()
    for i in range(3, 0, -1):
        num_area.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.session_state["step"] = "result"
    st.rerun()

elif st.session_state["step"] == "result":
    today = datetime.now().strftime("%Y / %m / %d")
    st.markdown(f"## 預測日期：{today}")
    try:
        df = pd.read_csv('history539.csv')
        all_nums = []
        for _, row in df.iterrows():
            all_nums.extend([str(row[c]).zfill(2) for c in ['n1', 'n2', 'n3', 'n4', 'n5']])
        counts = Counter(all_nums)
        sv = [n for n, c in counts.most_common(2)]
        jt = [n for n, c in counts.most_common(6)][2:]

        st.write("")
        c1, c2 = st.columns(2)
        with c1: st.markdown(f"<div class='res-box'>[ 專車 ]<br><h2>{', '.join(sv)}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='res-box'>[ 連碰 ]<br><h2>{', '.join(jt)}</h2></div>", unsafe_allow_html=True)
        
        if st.button("登出系統"):
            st.session_state["step"] = "login"
            st.rerun()
    except:
        st.error("找不到歷史數據")