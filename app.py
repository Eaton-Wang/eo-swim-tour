import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="EO Swim Tour 2025", page_icon="🏊", layout="centered")

# --- 2. 專業級 CSS 美化 ---
st.markdown("""
    <style>
    /* 全局字體與背景 */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* 頂部 Hero 區塊 */
    .hero-container {
        background: linear-gradient(135deg, #0062cc 0%, #00a8e8 100%);
        padding: 25px 20px;
        border-radius: 0 0 25px 25px;
        color: white;
        margin: -60px -20px 20px -20px; /* 抵銷 Streamlit 預設邊距 */
        box-shadow: 0 4px 15px rgba(0, 100, 200, 0.2);
        text-align: center;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 1px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .hero-subtitle {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 5px;
        font-weight: 300;
    }

    /* 行程卡片設計 */
    .event-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        position: relative;
        border: 1px solid #f0f0f0;
        transition: transform 0.2s;
    }
    
    /* 左側跳色條 (依照類型) */
    .border-swim { border-left: 6px solid #0062cc; }
    .border-travel { border-left: 6px solid #27ae60; }
    .border-sleep { border-left: 6px solid #8e44ad; }
    .border-default { border-left: 6px solid #95a5a6; }

    /* 卡片內容排版 */
    .time-badge {
        font-size: 1.4rem;
        font-weight: 800;
        color: #2c3e50;
        font-family: 'Roboto', sans-serif;
    }
    .note-badge {
        display: inline-block;
        background: #eef2f7;
        color: #555;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        vertical-align: middle;
        margin-left: 8px;
    }
    .loc-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #333;
        margin-top: 8px;
        margin-bottom: 2px;
    }
    .addr-text {
        font-size: 0.85rem;
        color: #888;
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }

    /* 按鈕優化 */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: all 0.2s;
    }
    /* 主要按鈕微調 */
    div[data-testid="stLinkButton"] > a {
        border-radius: 12px;
        font-weight: bold;
    }
    
    /* 隱藏 Streamlit footer */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. 資料區 (您的完整行程) ---
schedule_data = {
    "12/22 (一) Day 1": [
        {"time": "07:30", "loc": "台南出發", "addr": "台南市", "note": "出發", "type": "travel"},
        {"time": "09:00", "loc": "高雄苓雅 (英明國中)", "addr": "高雄市苓雅區英明路166號", "note": "檢測點 1", "type": "swim"},
        {"time": "14:30", "loc": "屏東萬巒 (萬巒國中)", "addr": "屏東縣萬巒鄉褒忠路5號", "note": "檢測點 2", "type": "swim"},
        {"time": "16:30", "loc": "屏東東港 (東港高中)", "addr": "屏東縣東港鎮東新路1-1號", "note": "檢測點 3", "type": "swim"},
    ],
    "12/23 (二) Day 2": [
        {"time": "Morning", "loc": "屏東出發", "addr": "屏東縣", "note": "移動日 (南迴)", "type": "travel"},
        {"time": "16:00", "loc": "花蓮市區 (中正路)", "addr": "花蓮縣花蓮市中正路210號", "note": "檢測點 1", "type": "swim"},
        {"time": "19:00", "loc": "花蓮市區 (國盛二街)", "addr": "花蓮縣花蓮市國盛二街22號", "note": "檢測點 2", "type": "swim"},
        {"time": "Night", "loc": "花蓮住宿 (林政街)", "addr": "花蓮縣花蓮市林政街88巷29號", "note": "休息住宿", "type": "sleep"},
    ],
    "12/24 (三) Day 3": [
        {"time": "Morning", "loc": "花蓮出發", "addr": "花蓮縣", "note": "前往宜蘭", "type": "travel"},
        {"time": "15:00", "loc": "宜蘭市區", "addr": "宜蘭縣宜蘭市校舍路1號", "note": "檢測點", "type": "swim"},
        {"time": "18:00", "loc": "新北中和 (中和國小)", "addr": "新北市中和區中和路100號", "note": "新增檢測點", "type": "swim"},
        {"time": "Night", "loc": "返回永和", "addr": "新北市永和區永平路205號", "note": "住宿", "type": "sleep"},
    ],
    "12/25 (四) Day 4": [
        {"time": "06:30", "loc": "永和出發", "addr": "新北市永和區永平路205號", "note": "早起", "type": "travel"},
        {"time": "09:00", "loc": "北市士林", "addr": "臺北市士林區福志路75號", "note": "檢測點", "type": "swim"},
        {"time": "13:30", "loc": "北市松山 (八德路)", "addr": "台北市八德路四段746號", "note": "檢測點", "type": "swim"},
        {"time": "19:00", "loc": "新北永和 (永利路)", "addr": "新北市永和區永利路71號", "note": "終點", "type": "sleep"},
    ],
    "12/26 (五) Day 5": [
        {"time": "Morning", "loc": "新北出發", "addr": "新北市", "note": "前往桃園", "type": "travel"},
        {"time": "08:00", "loc": "桃園中壢 (元智大學)", "addr": "桃園市中壢區遠東路135號", "note": "檢測點", "type": "swim"},
        {"time": "13:00", "loc": "新竹東區 (光復路)", "addr": "新竹市東區光復路二段101號", "note": "檢測點", "type": "swim"},
        {"time": "17:30", "loc": "新竹竹北 (福興東路)", "addr": "新竹縣竹北市福興東路一段199號", "note": "檢測點", "type": "swim"},
    ],
    "12/27 (六) Day 6": [
        {"time": "Morning", "loc": "苗栗出發", "addr": "苗栗縣", "note": "前往台中", "type": "travel"},
        {"time": "11:00", "loc": "台中霧峰 (成功路)", "addr": "台中市霧峰區成功路200號", "note": "檢測點", "type": "swim"},
        {"time": "15:00", "loc": "台中北區 (雙十路)", "addr": "臺中市北區雙十路一段16號", "note": "檢測點", "type": "swim"},
    ],
    "12/28 (日) Day 7": [
        {"time": "08:00", "loc": "彰化市 (建國東路)", "addr": "彰化縣彰化市建國東路2號", "note": "檢測點", "type": "swim"},
        {"time": "10:00", "loc": "彰化員林 (員林大道)", "addr": "彰化縣員林市員林大道二段235號", "note": "檢測點", "type": "swim"},
        {"time": "15:00", "loc": "南投埔里 (暨南大學)", "addr": "南投縣埔里鎮大學路1號", "note": "檢測點", "type": "swim"},
    ],
    "12/29 (一) Day 8": [
        {"time": "Morning", "loc": "南投出發", "addr": "南投縣", "note": "前往雲嘉", "type": "travel"},
        {"time": "15:30", "loc": "雲林虎尾 (北平路)", "addr": "雲林縣虎尾鎮北平路380號", "note": "檢測點", "type": "swim"},
        {"time": "17:00", "loc": "嘉義西區 (南京路)", "addr": "嘉義市西區南京路272號", "note": "最終站", "type": "swim"},
    ],
}

# --- 4. 輔助函式 ---
def get_google_maps_url(address):
    return f"http://googleusercontent.com/maps.google.com/maps?daddr={urllib.parse.quote(address)}"

def get_full_route_url(events):
    base = "https://www.google.com/maps/dir/"
    addrs = [urllib.parse.quote(e['addr']) for e in events]
    return base + "/".join(addrs)

def get_nearby_url(address, query):
    return f"https://www.google.com/maps/search/{query}+near+{urllib.parse.quote(address)}"

def get_type_style(event_type):
    # 回傳對應的 CSS class
    return f"border-{event_type}" if event_type else "border-default"

# --- 5. 主程式介面 ---

# [Hero 區塊]
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">EO Swim Tour</div>
        <div class="hero-subtitle">2025 台灣環島檢測之旅</div>
    </div>
""", unsafe_allow_html=True)

# [檢查清單 & 數據連結] (摺疊以保持整潔)
with st.expander("🛠️ 工具箱 (檢查清單 / 數據紀錄)"):
    st.markdown("**設備檢查：**")
    c_check1, c_check2 = st.columns(2)
    with c_check1:
        st.checkbox("eo 主機 & iPad")
        st.checkbox("三腳架 & 快拆")
    with c_check2:
        st.checkbox("延長線 & 轉接頭")
        st.checkbox("個人錢包手機")
    
    st.markdown("---")
    # 請替換成您的 Google Form 連結
    data_link = "https://docs.google.com/forms/" 
    st.link_button("📝 開啟數據紀錄表 (Google Form)", data_link, use_container_width=True)

# [日期選擇器]
st.write("") # Spacer
days_list = list(schedule_data.keys())
# 嘗試自動選取今日
today_str = datetime.now().strftime("%m/%d")
default_idx = 0
for idx, day in enumerate(days_list):
    if today_str in day:
        default_idx = idx
        break

selected_day = st.selectbox("📅 選擇行程日期：", days_list, index=default_idx)
events = schedule_data[selected_day]

# [全程導航按鈕]
if len(events) > 1:
    st.write("")
    full_route = get_full_route_url(events)
    st.link_button(
        f"🗺️ 啟動 Day {selected_day.split(' ')[2]} 全程導航", 
        full_route, 
        type="primary",
        use_container_width=True
    )

st.write("") # Spacer

# [行程卡片渲染 Loop]
for event in events:
    # 判斷類型樣式 (若資料沒有標註 type，預設 default)
    evt_type = event.get('type', 'default')
    border_class = get_type_style(evt_type)
    
    # 決定 icon
    icon = "📍"
    if evt_type == "swim": icon = "🏊"
    elif evt_type == "travel": icon = "🚗"
    elif evt_type == "sleep": icon = "🛌"

    # 渲染卡片 HTML
    st.markdown(f"""
    <div class="event-card {border_class}">
        <div>
            <span class="time-badge">{event['time']}</span>
            <span class="note-badge">{icon} {event['note']}</span>
        </div>
        <div class="loc-title">{event['loc']}</div>
        <div class="addr-text">🏠 {event['addr']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能按鈕區 (使用 Streamlit 原生 Columns 排版)
    col_main, col_sub1, col_sub2, col_sub3 = st.columns([3, 1, 1, 1])
    
    with col_main:
        st.link_button("📍 導航前往", get_google_maps_url(event['addr']), use_container_width=True)
    
    # 小圖示按鈕
    with col_sub1:
        st.link_button("🅿️", get_nearby_url(event['addr'], "parking"), help="找停車場", use_container_width=True)
    with col_sub2:
        st.link_button("🍱", get_nearby_url(event['addr'], "food"), help="找美食", use_container_width=True)
    with col_sub3:
        st.link_button("☕", get_nearby_url(event['addr'], "coffee"), help="找咖啡", use_container_width=True)

st.markdown("<br><br><div style='text-align: center; color: #ccc; font-size: 0.8rem;'>Drive Safe. Swim Fast.</div>", unsafe_allow_html=True)
