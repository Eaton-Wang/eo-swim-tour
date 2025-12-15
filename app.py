import streamlit as st
import pandas as pd
from datetime import datetime

# 設定網頁標題與配置
st.set_page_config(page_title="EO Swim 環島檢測", page_icon="🏊", layout="centered")

# CSS 優化手機顯示 (加大按鈕、優化卡片間距)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        height: 3em;
    }
    .event-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #0068c9;
    }
    .time-label {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

# === 資料建立 ===
# 這裡將您提供的行程轉換為結構化數據
schedule_data = {
    "Day 1 (12/22 週一)": [
        {"time": "08:00", "action": "出發", "loc": "台南出發", "addr": "台南市", "note": "前往高雄"},
        {"time": "09:00", "action": "抵達", "loc": "高雄苓雅 (英明國中周邊)", "addr": "高雄市苓雅區英明路166號", "note": "檢測點 1"},
        {"time": "14:30", "action": "抵達", "loc": "屏東萬巒 (萬巒國中周邊)", "addr": "屏東縣萬巒鄉褒忠路5號", "note": "檢測點 2"},
        {"time": "16:30", "action": "抵達", "loc": "屏東東港 (東港高中周邊)", "addr": "屏東縣東港鎮東新路1-1號", "note": "檢測點 3"},
    ],
    "Day 2 (12/23 週二)": [
        {"time": "Morning", "action": "出發", "loc": "屏東出發", "addr": "屏東縣", "note": "長途車程預警 (南迴改)"},
        {"time": "19:00", "action": "抵達", "loc": "花蓮市區", "addr": "花蓮縣花蓮市國盛二街22號", "note": "住宿/晚間行程"},
    ],
    "Day 3 (12/24 週三)": [
        {"time": "Morning", "action": "出發", "loc": "花蓮出發", "addr": "花蓮市", "note": "前往宜蘭"},
        {"time": "15:00", "action": "抵達", "loc": "宜蘭市區", "addr": "宜蘭縣宜蘭市校舍路1號", "note": "檢測點 1"},
        {"time": "19:00", "action": "抵達", "loc": "基隆暖暖", "addr": "基隆市暖暖區暖暖街350號", "note": "檢測點 2"},
        {"time": "Night", "action": "結束", "loc": "返回新北永和", "addr": "新北市永和區永平路205號", "note": "住宿"},
    ],
    "Day 4 (12/25 週四)": [
        {"time": "06:30", "action": "集合", "loc": "新北永和", "addr": "新北市永和區永平路205號", "note": "早晨出發"},
        {"time": "09:00", "action": "抵達", "loc": "北市士林", "addr": "臺北市士林區福志路75號", "note": "檢測點 1"},
        {"time": "13:30", "action": "抵達", "loc": "北市松山", "addr": "台北市八德路四段746號", "note": "檢測點 2"},
        {"time": "19:00", "action": "抵達", "loc": "新北永和 (不同地點)", "addr": "新北市永和區永利路71號", "note": "晚間行程"},
    ],
    "Day 5 (12/26 週五)": [
        {"time": "Morning", "action": "出發", "loc": "新北出發", "addr": "新北市", "note": "前往桃園"},
        {"time": "08:00", "action": "抵達", "loc": "桃園中壢 (元智大學)", "addr": "桃園市中壢區遠東路135號", "note": "健康休閒中心"}, # 修正了元智大學地址以確保導航準確
        {"time": "13:00", "action": "抵達", "loc": "新竹東區 (清大周邊)", "addr": "新竹市東區光復路二段101號", "note": "檢測點 2"},
        {"time": "17:30", "action": "抵達", "loc": "新竹竹北", "addr": "新竹縣竹北市福興東路一段199號", "note": "檢測點 3"},
    ],
    "Day 6 (12/27 週六)": [
        {"time": "Morning", "action": "出發", "loc": "苗栗出發", "addr": "苗栗縣", "note": "前往台中"},
        {"time": "11:00", "action": "抵達", "loc": "台中北屯", "addr": "臺中市北屯區河北西街17號", "note": "檢測點 1"},
        {"time": "13:00", "action": "抵達", "loc": "台中北區 (台體大周邊)", "addr": "臺中市北區雙十路一段16號", "note": "檢測點 2"},
    ],
    "Day 7 (12/28 週日)": [
        {"time": "08:00", "action": "抵達", "loc": "彰化市", "addr": "彰化縣彰化市建國東路2號", "note": "檢測點 1"},
        {"time": "10:00", "action": "抵達", "loc": "彰化員林", "addr": "彰化縣員林市員林大道二段235號", "note": "檢測點 2"},
        {"time": "15:00", "action": "抵達", "loc": "南投埔里 (暨南大學)", "addr": "南投縣埔里鎮大學路1號", "note": "檢測點 3"},
    ],
    "Day 8 (12/29 週一)": [
        {"time": "Morning", "action": "出發", "loc": "南投出發", "addr": "南投縣", "note": "前往雲林"},
        {"time": "15:30", "action": "抵達", "loc": "雲林虎尾", "addr": "雲林縣虎尾鎮北平路380號", "note": "檢測點 1"},
        {"time": "17:00", "action": "抵達", "loc": "嘉義西區", "addr": "嘉義市西區南京路272號", "note": "最終站"},
    ]
}

# 輔助函式：產生 Google Maps 連結
def get_gmaps_link(address):
    base_url = "https://www.google.com/maps/dir/?api=1&destination="
    return base_url + address.replace(" ", "+")

# === 介面邏輯 ===

st.title("🏊 eo Swim 台灣環島儀表板")
st.markdown("### 行程助手 (12/22 - 12/29)")

# 選擇日期 (預設選第一天，或根據當前日期判斷)
day_options = list(schedule_data.keys())
selected_day = st.selectbox("📅 請選擇日期查看行程：", day_options)

# 顯示該日行程
st.divider()
st.header(f"{selected_day}")

events = schedule_data[selected_day]

for i, event in enumerate(events):
    # 建立卡片式佈局
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"<div style='padding-top:10px;'><span class='time-label'>{event['time']}</span></div>", unsafe_allow_html=True)
            st.caption(event['action'])
            
        with col2:
            st.subheader(event['loc'])
            st.write(f"🏠 {event['addr']}")
            if event['note']:
                st.info(f"📝 {event['note']}")
            
            # 導航按鈕
            nav_link = get_gmaps_link(event['addr'])
            st.link_button(f"📍 導航到：{event['loc']}", nav_link, type="primary")
            
    if i < len(events) - 1:
        st.markdown("⬇️ *車程移動*")

# 底部資訊
st.divider()
st.caption("Developed for eo Swim Tour 2025. Drive Safe! 🚗")