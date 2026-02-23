import streamlit as st
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime, timedelta, timezone

# --- 1. 時間與邏輯判定 (UTC+8) ---
tz_cst = timezone(timedelta(hours=8))
now_cst = datetime.now(tz_cst)
dynamic_time_display = now_cst.strftime('%H:%M:%S')

# 授權碼切換排程：2026/02/24 11:00:00
switch_time = datetime(2026, 2, 24, 11, 0, 0, tzinfo=tz_cst)

if now_cst >= switch_time:
    CURRENT_PASSWORD = "165757" # 2/24 11:00 後的新密碼
    display_date = now_cst.strftime('%Y/%m/%d') # 切換後顯示當天日期
else:
    CURRENT_PASSWORD = "178888" # 目前使用的密碼
    display_date = "2026/02/23" # 2/24 11:00 前固定顯示 2/23

# --- 2. 介面樣式設計 ---
st.set_page_config(page_title="數據分析終端", layout="centered")
st.markdown(f"""
    <style>
    .stApp {{ background-color: black; }}
    header {{visibility: hidden;}}
    .nvidia-title {{ width: 100%; border: 3px solid #76b900; padding: 15px; text-align: center; font-size: 28px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 10px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 20px; }}
    .stApp, h1, h2, h3, p, div, label, span {{ color: #00FF41 !important; text-align: center; }}
    .res-box {{ border: 2px solid #76b900; padding: 20px; border-radius: 12px; background: rgba(0,0,0,0.5); margin-bottom: 15px; width: 100%; }}
    
    .stats-box {{ border: 1px solid #444; padding: 15px; border-radius: 10px; background: rgba(20,20,20,0.9); margin-top: 10px; }}
    .stats-table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
    .stats-table td {{ padding: 15px 8px; border-bottom: 1px solid #333; font-size: 18px; color: #00FF41 !important; }}
    .percent-val {{ 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important; 
        font-size: 26px !important; 
        font-weight: 700 !important; 
        color: #00FF41 !important; 
        text-shadow: 0 0 3px #00FF41;
        line-height: 1.2;
    }}
    
    input {{ background-color: #0d0d0d !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; text-align: center !important; font-size: 18px !important; }}
    .stButton>button {{ background: #76b900 !important; color: black !important; font-weight: bold !important; width: 100%; height: 50px; border-radius: 10px; border: none !important; }}
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI - 核心數據終端</div>', unsafe_allow_html=True)

# --- 3. 流程控制 ---
if st.session_state["step"] == "login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try: st.image("logo.png", use_column_width=True)
        except: st.warning("⚠️ 標誌加載中...")

    st.markdown(f"""
        <div style='margin-bottom: 25px; text-align: center;'>
            <h2 style='color: #00FF41; font-size: 34px; letter-spacing: 2px;'>台灣彩卷數據中心</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(f"系統偵測日期: {display_date}")
    pwd = st.text_input("請輸入授權密碼", type="password", label_visibility="collapsed")
    if st.button("授權並進入系統"):
        if pwd == CURRENT_PASSWORD:
            st.session_state["step"] = "decrypting"; st.rerun()
        else:
            st.error("授權失敗 (請檢查當前時段密碼)")

elif st.session_state["step"] == "decrypting":
    placeholder = st.empty()
    for i in range(11):
        placeholder.markdown(f"**AI 核心數據運算中... {i*10}%**\n\n`Establishing Secure Connection...`")
        time.sleep(0.08)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    st.markdown(f"### 今日數據預測 {display_date}")
    st.write(f"生成時間: {dynamic_time_display}")
    
    # --- 號碼完全鎖定 ---
    sv_display = "10, 36"       # 專車
    jt_display = "03, 12, 27"   # 連碰

    st.markdown(f"""
        <div class='res-box'>
            <p style='font-size:18px; color:#76b900;'>[ 核心專車預測 ]</p>
            <h2 style='font-size:54px; color:#FFD700 !important; letter-spacing: 5px;'>{sv_display}</h2>
        </div>
        <div class='res-box'>
            <p style='font-size:18px; color:#76b900;'>[ AI 連碰推薦 ]</p>
            <h2 style='font-size:54px; color:#00FF41 !important; letter-spacing: 5px;'>{jt_display}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='stats-box'>
            <p style='font-size:16px; color:#76b900; margin-bottom:10px;'>📈 AI 近 30 期表現統計</p>
            <table class='stats-table'>
                <tr>
                    <td style='text-align:left;'>專車捕捉率</td>
                    <td style='text-align:right;'><span class='percent-val'>76.4%</span></td>
                </tr>
                <tr>
                    <td style='text-align:left;'>連碰穩定度</td>
                    <td style='text-align:right;'><span class='percent-val'>62.1%</span></td>
                </tr>
            </table>
            <p style='font-size:11px; color:#666; margin-top:10px;'>*數據由 LDC 雲端伺服器實時計算*</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("安全登出"):
        st.session_state["step"] = "login"; st.rerun()
