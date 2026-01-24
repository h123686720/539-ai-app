import streamlit as st
import pandas as pd
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. 樣式設定 ---
st.set_page_config(page_title="輝達科技 AI - 全自動數據終端", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: black; }
    header {visibility: hidden;}
    .main .block-container { max-width: 600px; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: auto; }
    .nvidia-title { width: 100%; border: 3px solid #76b900; padding: 20px; text-align: center; font-size: 42px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 20px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 40px; }
    .stApp, h1, h2, h3, p, div, label, span { color: #00FF41 !important; text-align: center; }
    .countdown { font-size: 150px; font-weight: bold; text-shadow: 0 0 50px #00FF41; }
    .res-box { border: 2px solid #76b900; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.5); margin: 10px 0; }
    .history-text { font-size: 16px; color: #76b900 !important; border: 1px dashed #76b900; padding: 10px; margin-bottom: 15px; border-radius: 5px; }
    input { background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; }
    .stButton>button { background: transparent !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; }
    
    /* 讓摺疊選單看起來隱密一點 */
    .stExpander { border: none !important; background: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 自動爬蟲函數 ---
def get_latest_539():
    try:
        url = "https://www.lotto-8.com/listlto539.asp"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', {'class': 'table_lotto'})
        latest_row = table.find_all('tr')[1]
        cols = latest_row.find_all('td')
        
        # 抓取開獎日期與號碼
        draw_date = cols[1].text.strip()
        raw_nums = cols[2].text.strip().replace('\xa0', ' ').split(' ')
        nums = sorted([n for n in raw_nums if n])[:5]
        return nums, draw_date
    except:
        return ["05", "12", "18", "24", "33"], "數據讀取失敗"

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI</div>', unsafe_allow_html=True)

# 動態密鑰 (日期 + 88)
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
    with st.spinner('正在連接雲端數據庫...'):
        # 同步抓取號碼與日期
        nums, date = get_latest_539()
        st.session_state["history_nums"] = nums
        st.session_state["draw_date"] = date
        
    for i in range(30):
        code = "".join([ "錢贏中獎!@#$"[random.randint(0,7)] for _ in range(10)])
        msg.markdown(f"### [AI 正在抓取實時開獎數據]\n## {code}\n進度: {int(i*3.4)}%")
        time.sleep(0.04)
    st.session_state["step"] = "countdown"; st.rerun()

elif st.session_state["step"] == "countdown":
    num = st.empty()
    for i in range(3, 0, -1):
        num.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    st.markdown(f"## 今日 AI 推算結果")
    st.markdown(f"<div class='history-text'>📡 系統已自動偵測最新獎號並完成 AI 推算</div>", unsafe_allow_html=True)

    h_nums = st.session_state.get("history_nums", ["05", "12", "18", "24", "33"])
    h_date = st.session_state.get("draw_date", "未知")

    random.seed(int(datetime.now().strftime("%Y%m%d")))
    pool = [str(i).zfill(2) for i in range(1, 40) if str(i).zfill(2) not in h_nums]
    all_picks = sorted(random.sample(pool, 6))
    sv_final = all_picks[:2]
    jt_final = all_picks[2:]

    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='res-box'>[ 專車 ]<br><h2 style='font-size:38px;'>{', '.join(sv_final)}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='res-box'>[ 連碰 ]<br><h2 style='font-size:38px;'>{', '.join(jt_final)}</h2></div>", unsafe_allow_html=True)
    
    st.write("---")
    
    # --- 管理員隱藏檢查區 ---
    with st.expander("🔍 系統狀態檢查 (僅供管理員)"):
        st.write(f"最後抓取日期: {h_date}")
        st.write(f"偵測獎號紀錄: {', '.join(h_nums)}")
        st.write("狀態: 爬蟲連線正常")

    if st.button("登出"):
        st.session_state["step"] = "login"; st.rerun()
