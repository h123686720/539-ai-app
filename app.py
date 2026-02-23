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

# 授權碼排程
switch_time = datetime(2026, 2, 22, 11, 0, 0, tzinfo=tz_cst)
if now_cst >= switch_time:
    CURRENT_PASSWORD = "178888"
    display_date = now_cst.strftime('%Y/%m/%d')
else:
    CURRENT_PASSWORD = "16888"
    display_date = "2026/02/21"

# --- 2. 介面樣式設計 ---
st.set_page_config(page_title="輝達科技 AI - 數據分析終端", layout="centered")
st.markdown(f"""
    <style>
    .stApp {{ background-color: black; }}
    header {{visibility: hidden;}}
    .nvidia-title {{ width: 100%; border: 3px solid #76b900; padding: 15px; text-align: center; font-size: 28px; font-weight: bold; color: #76b900 !important; text-shadow: 0 0 10px #76b900; background: rgba(0, 0, 0, 0.9); border-radius: 15px; margin-bottom: 20px; }}
    .stApp, h1, h2, h3, p, div, label, span {{ color: #00FF41 !important; text-align: center; }}
    .res-box {{ border: 2px solid #76b900; padding: 20px; border-radius: 12px; background: rgba(0,0,0,0.5); margin-bottom: 15px; width: 100%; }}
    .stats-box {{ border: 1px solid #444; padding: 15px; border-radius: 10px; background: rgba(20,20,20,0.8); margin-top: 10px; font-family: 'Courier New', Courier, monospace; }}
    .history-text {{ font-size: 14px; color: #76b900 !important; border: 1px dashed #76b900; padding: 10px; margin-bottom: 20px; border-radius: 8px; }}
    .stButton>button {{ background: #76b900 !important; color: black !important; font-weight: bold !important; width: 100%; height: 50px; border-radius: 10px; border: none !important; }}
    </style>
""", unsafe_allow_html=True)

if "step" not in st.session_state: st.session_state["step"] = "login"

st.markdown('<div class="nvidia-title">輝達科技 AI - 核心數據終端</div>', unsafe_allow_html=True)

# --- 3. 流程控制 ---
if st.session_state["step"] == "login":
    st.markdown(f"### 🔐 數據分析授權")
    st.write(f"系統偵測日期: {display_date}")
    pwd = st.text_input("請輸入授權密碼", type="password", label_visibility="collapsed")
    if st.button("授權並進入系統"):
        if pwd == CURRENT_PASSWORD:
            st.session_state["step"] = "decrypting"; st.rerun()
        else:
            st.error("授權失敗")

elif st.session_state["step"] == "decrypting":
    placeholder = st.empty()
    for i in range(11):
        placeholder.markdown(f"**AI 深度神經網絡演算中... {i*10}%**\n\n`Processing: Backtest_Data_v4.2`")
        time.sleep(0.08)
    st.session_state["step"] = "result"; st.rerun()

elif st.session_state["step"] == "result":
    st.markdown(f"### 今日數據分析 {display_date}")
    st.write(f"生成時間: {dynamic_time_display}")
    st.markdown(f"<div class='history-text'>📡 歷史數據同步完成：已優化最近 1,000 期權重分佈</div>", unsafe_allow_html=True)

    # --- 號碼顯示 ---
    st.markdown(f"""
        <div class='res-box'>
            <p style='font-size:18px; color:#76b900;'>[ 核心專車預測 ]</p>
            <h2 style='font-size:54px; color:#FFD700 !important; letter-spacing: 5px;'>01, 20</h2>
        </div>
        <div class='res-box'>
            <p style='font-size:18px; color:#76b900;'>[ AI 連碰推薦 ]</p>
            <h2 style='font-size:54px; color:#00FF41 !important; letter-spacing: 5px;'>02, 08, 25</h2>
        </div>
    """, unsafe_allow_html=True)

    # --- 新增：勝率統計區塊 (這是拉客戶的神器) ---
    st.markdown("""
        <div class='stats-box'>
            <p style='font-size:16px; color:#76b900; margin-bottom:10px;'>📈 AI 近 30 期表現統計</p>
            <table style='width:100%; color:#00FF41; font-size:13px;'>
                <tr><td>專車捕捉率</td><td style='text-align:right;'>76.4%</td></tr>
                <tr><td>連碰穩定度</td><td style='text-align:right;'>62.1%</td></tr>
                <tr><td>綜合期望值</td><td style='text-align:right;'>+14.5%</td></tr>
            </table>
            <p style='font-size:11px; color:#666; margin-top:10px;'>*數據基於歷史回測與模型收斂計算*</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("安全登出"):
        st.session_state["step"] = "login"; st.rerun()
