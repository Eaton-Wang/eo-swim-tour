import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="EO Swim Tour 2025", page_icon="🏊", layout="centered")

# --- 2. 柔和護眼 CSS ---
st.markdown("""
    <style>
    /* 全局背景：柔和的灰白色，避免全白刺眼 */
    .stApp {
        background-color: #f4f6f9;
    }
    
    /* 頂部 Hero 區塊：深岩灰色，專業沈穩 */
    .hero-container {
        background-color: #2c3e50;
        padding: 30px 20px;
        border-radius: 0 0 20px 20px;
        color: #ecf0f1;
        margin: -60px -20px 20px -20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    .hero-subtitle {
        font-size: 0.9rem;
        color: #bdc3c7;
        margin-top: 5px;
        font-weight: 400;
    }

    /* 卡片設計：純白底 + 極輕微陰影 */
    .event-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03); /* 極淡陰影 */
        margin-bottom: 12px;
        border: 1px solid #e1e4e8; /* 增加細微邊框增加輪廓感 */
        position: relative;
    }
    
    /* 左側線條：使用低飽和度顏色 */
    .border-swim { border-left: 5px solid #5d9cec; } /* 柔和藍 */
    .border-travel { border-left: 5px solid #a0d468; } /* 柔和綠 */
    .border-sleep { border-left: 5px solid #ac92ec; } /* 柔和紫 */
    .border-default { border-left: 5px solid #ccd1d9; } /* 淺灰 */

    /* 內容排版 */
    .time-badge {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2c3e50; /* 深灰藍色，比純黑舒服 */
        font-family: 'Roboto', sans-serif;
    }
    
    /* 標籤優化：淺底深字 (護眼關鍵) */
    .note-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 8px;
        vertical-align: middle;
    }
    /* 不同類型的標籤配色 */
    .badge-swim { background-color: #eaf4fe; color: #2b6cb0; }
    .badge-travel { background-color: #f0fff4; color: #2f855a; }
    .badge-sleep { background-color: #faf5ff; color: #6b46c1; }
    .badge-default { background-color: #f7fafc; color: #4a5568; }

    .loc-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #34495e;
        margin-top: 10px;
        margin-bottom: 4px;
    }
    .addr-text {
        font-size: 0.9rem;
        color: #7f8c8d; /* 中灰色 */
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }

    /* 按鈕優化 */
    div[data-testid="stLinkButton"] > a {
        border-radius: 8px;
        font-weight: 600;
        box-shadow: none;
    }
    
    /* 隱藏 Footer */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. 資料區 ---
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
    # 回傳邊框 class 和 badge class
    return f"border-{event_type}", f"badge-{event_type}"

# --- 5. 主程式介面 ---

# [Hero 區塊]
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">EO Swim Tour 2025</div>
        <div class="hero-subtitle">環島檢測任務</div>
    </div>
""", unsafe_allow_html=True)

# [工具箱] (使用 st.expander)
with st.expander("🛠️ 快速檢查 & 數據"):
    c1, c2 = st.columns(2)
    with c1:
        st.caption("出發檢查")
        st.checkbox("eo 主機 / iPad")
        st.checkbox("三腳架 / 轉接頭")
    with c2:
        st.caption("其他")
        st.checkbox("錢包手機鑰匙")
        st.checkbox("延長線")
    
    st.markdown("---")
    # 數據表單連結
    st.link_button("📝 填寫檢測數據", "https://docs.google.com/forms/", use_container_width=True)

# [日期選擇]
st.write("") 
days_list = list(schedule_data.keys())
today_str = datetime.now().strftime("%m/%d")
default_idx = 0
for idx, day in enumerate(days_list):
    if today_str in day:
        default_idx = idx
        break

selected_day = st.selectbox("📅 選擇行程日期：", days_list, index=default_idx)
events = schedule_data[selected_day]

# [全程導航]
if len(events) > 1:
    st.write("")
    full_route = get_full_route_url(events)
    st.link_button(
        f"🗺️ {selected_day.split(' ')[2]} 全程導航", 
        full_route, 
        type="primary",
        use_container_width=True
    )

st.write("") 

# [卡片渲染]
for event in events:
    evt_type = event.get('type', 'default')
    border_class, badge_class = get_type_style(evt_type)
    
    icon = "📍"
    if evt_type == "swim": icon = "🏊"
    elif evt_type == "travel": icon = "🚗"
    elif evt_type == "sleep": icon = "🛌"

    st.markdown(f"""
    <div class="event-card {border_class}">
        <div>
            <span class="time-badge">{event['time']}</span>
            <span class="note-badge {badge_class}">{icon} {event['note']}</span>
        </div>
        <div class="loc-title">{event['loc']}</div>
        <div class="addr-text">🏠 {event['addr']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按鈕區
    col_main, col_sub1, col_sub2, col_sub3 = st.columns([3, 1, 1, 1])
    
    with col_main:
        st.link_button("📍 導航前往", get_google_maps_url(event['addr']), use_container_width=True)
    
    # 縮小版周邊按鈕
    with col_sub1:
        st.link_button("🅿️", get_nearby_url(event['addr'], "parking"), help="找停車場", use_container_width=True)
    with col_sub2:
        st.link_button("🍱", get_nearby_url(event['addr'], "food"), help="找美食", use_container_width=True)
    with col_sub3:
        st.link_button("☕", get_nearby_url(event['addr'], "coffee"), help="找咖啡", use_container_width=True)

st.markdown("<br><div style='text-align: center; color: #b0b0b0; font-size: 0.8rem;'>Have a safe trip!</div>", unsafe_allow_html=True)
