import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="EO Swim Tour", page_icon="🏊", layout="centered")

# --- 2. 介面優化 CSS (修正輸入框白屏問題) ---
st.markdown("""
    <style>
    /* 頂部 Hero 標題區塊 */
    .hero-container {
        background: #0066cc;
        padding: 15px 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 5px;
    }

    /* 修正下拉選單 (Selectbox) 的顯示問題 */
    /* 強制給予選單區域一個淺灰背景與邊框，避免「全白」 */
    div[data-testid="stSelectbox"] > div > div {
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        color: #333;
    }
    /* 確保選單內的文字顏色夠深 */
    div[data-testid="stSelectbox"] label {
        font-weight: bold;
        color: #1f2937;
        font-size: 1rem;
    }

    /* 行程卡片設計 */
    .event-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        margin-bottom: 12px;
        border: 1px solid #e5e7eb; /* 增加邊框以利辨識 */
    }

    /* 時間與標籤 */
    .time-row {
        display: flex;
        align-items: center;
        margin-bottom: 5px;
    }
    .time-text {
        font-size: 1.25rem;
        font-weight: 800;
        color: #111827; /* 深黑色 */
        margin-right: 10px;
    }
    .tag {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        background-color: #e5e7eb;
        color: #374151;
    }
    
    /* 地點文字 */
    .loc-text {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0056b3; /* 連結藍 */
        margin-bottom: 2px;
    }
    .addr-text {
        font-size: 0.9rem;
        color: #4b5563;
        margin-bottom: 12px;
    }

    /* 按鈕優化 */
    /* 主要連結按鈕 (導航) */
    .stLinkButton a {
        font-weight: bold !important;
    }
    
    /* 隱藏 Footer */
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

# --- 5. 主程式介面 ---

# [Hero 區塊]
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">EO Swim Tour 2025</div>
        <div class="hero-subtitle">環島檢測任務助手</div>
    </div>
""", unsafe_allow_html=True)

# [任務工具箱] (摺疊選單)
with st.expander("🛠️ 任務工具箱 (Checklist & Data)"):
    st.caption("📍 離場前確認：")
    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("eo 感測器 & iPad")
        st.checkbox("三腳架 & 配件")
    with c2:
        st.checkbox("個人錢包 / 鑰匙")
        st.checkbox("延長線 / 電源")
    
    st.markdown("---")
    # 數據表單連結
    data_link = "https://docs.google.com/forms/" 
    st.link_button("📝 開啟數據紀錄表 (Google Form)", data_link, use_container_width=True)

# [日期選擇器 - 強制樣式修正]
st.write("") 
days_list = list(schedule_data.keys())
today_str = datetime.now().strftime("%m/%d")
default_idx = 0
for idx, day in enumerate(days_list):
    if today_str in day:
        default_idx = idx
        break

# 這裡的 Selectbox 會受到上方 CSS 保護，不會再變成全白
selected_day = st.selectbox("📅 請選擇日期：", days_list, index=default_idx)
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

st.write("") 

# [行程卡片 Loop]
for event in events:
    # 決定 icon
    icon = "📍"
    if event.get('type') == "swim": icon = "🏊"
    elif event.get('type') == "travel": icon = "🚗"
    elif event.get('type') == "sleep": icon = "🛌"

    # 渲染卡片 (最純粹的 HTML 結構，避免 CSS 衝突)
    st.markdown(f"""
    <div class="event-card">
        <div class="time-row">
            <span class="time-text">{event['time']}</span>
            <span class="tag">{icon} {event['note']}</span>
        </div>
        <div class="loc-text">{event['loc']}</div>
        <div class="addr-text">🏠 {event['addr']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按鈕區 (使用 Streamlit 原生 Columns 確保可點擊性)
    col_main, col_sub1, col_sub2, col_sub3 = st.columns([3, 1, 1, 1])
    
    with col_main:
        st.link_button("📍 導航前往", get_google_maps_url(event['addr']), use_container_width=True)
    
    with col_sub1:
        st.link_button("🅿️", get_nearby_url(event['addr'], "parking"), help="找停車場", use_container_width=True)
    with col_sub2:
        st.link_button("🍱", get_nearby_url(event['addr'], "food"), help="找美食", use_container_width=True)
    with col_sub3:
        st.link_button("☕", get_nearby_url(event['addr'], "coffee"), help="找咖啡", use_container_width=True)

st.markdown("<br><br><div style='text-align: center; color: #999; font-size: 0.8rem;'>EO Swim Better</div>", unsafe_allow_html=True)
