import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="EO Swim Tour", page_icon="🏊", layout="centered")

# --- 2. 絕對色彩鎖定 CSS (修復下拉選單黑底問題) ---
st.markdown("""
    <style>
    /* =========================================
       1. 全域強制設定 (Root Overrides)
       ========================================= */
    :root {
        --primary-color: #0066cc;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #000000;
        --font: sans-serif;
    }
    
    /* 強制 App 背景為淺灰 */
    .stApp {
        background-color: #f2f4f8 !important;
    }
    
    /* 強制主要文字為黑色 */
    p, h1, h2, h3, div, span, label, li {
        color: #000000 !important;
    }

    /* =========================================
       2. 下拉選單 (Selectbox) 深度修復
       這是針對您第二張截圖「全黑選單」的解法
       ========================================= */
    
    /* 選單還沒點開時的框框 */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #000000 !important; /* 改成黑色邊框更明顯 */
        color: #000000 !important;
    }
    
    /* 選單內的文字 (選中後) */
    div[data-baseweb="select"] span {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
    }

    /* !!! 關鍵修復：下拉出來的清單容器 !!! */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background-color: #ffffff !important; /* 強制白底 */
    }

    /* !!! 關鍵修復：清單裡的每一個選項 !!! */
    li[role="option"] {
        background-color: #ffffff !important; /* 強制白底 */
        color: #000000 !important;            /* 強制黑字 */
        border-bottom: 1px solid #eeeeee !important; /* 加個分隔線 */
    }
    
    /* 滑鼠滑過選項時 */
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #e6f7ff !important; /* 淺藍底 */
        color: #000000 !important;
    }
    
    /* 選單內的小文字 (如描述) */
    div[data-baseweb="menu"] div {
        color: #000000 !important;
    }

    /* =========================================
       3. 按鈕 (Link Button) 深度修復
       這是針對您第一張截圖「右側按鈕變黑」的解法
       ========================================= */
    
    /* 強制所有連結按鈕 (包含導航、停車、美食...) 變成白底黑字 */
    div[data-testid="stLinkButton"] > a {
        background-color: #ffffff !important;   /* 絕對白底 */
        color: #000000 !important;              /* 絕對黑字 */
        border: 2px solid #0066cc !important;   /* 深藍邊框 */
        font-weight: 800 !important;
        text-decoration: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15) !important;
        
        /* 確保字體在任何瀏覽器都不會變色 */
        -webkit-text-fill-color: #000000 !important; 
    }

    /* 滑鼠滑過按鈕 */
    div[data-testid="stLinkButton"] > a:hover {
        background-color: #f0f8ff !important;
        border-color: #004d99 !important;
    }
    
    /* 特別針對右側三個小按鈕的容器微調 (若需要) */
    /* 這裡只要上面的規則生效，三個小按鈕也會變白 */

    /* =========================================
       4. 任務工具箱 (Expander)
       ========================================= */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border-radius: 8px;
    }
    div[data-testid="stExpander"] summary {
        color: #000000 !important;
        font-weight: bold;
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #fafafa !important;
        color: #000000 !important;
    }

    /* =========================================
       5. 卡片設計 (保持不變，因為這部分顯示正常)
       ========================================= */
    .event-card {
        background-color: #ffffff !important;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border: 1px solid #ddd;
    }
    .time-text { font-size: 1.5rem; font-weight: 900; color: #000 !important; margin-right: 8px;}
    .loc-text { font-size: 1.2rem; font-weight: 800; color: #0056b3 !important; margin-top: 5px;}
    .addr-text { font-size: 1rem; color: #333 !important; margin-bottom: 10px;}
    .tag { background: #eee !important; color: #000 !important; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;}
    
    /* 隱藏 Footer */
    footer {display: none !important;}
    header {display: none !important;}
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
    <div style="background-color: #004d99; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; border: 2px solid white;">
        <div style="color: white; font-size: 1.5rem; font-weight: 900;">EO Swim Tour 2025</div>
        <div style="color: #ddd; font-size: 0.9rem;">環島檢測任務助手</div>
    </div>
""", unsafe_allow_html=True)

# [任務工具箱] (使用 Expander)
with st.expander("🛠️ 任務工具箱 (Checklist & Data)"):
    st.markdown("**離場前確認：**")
    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("eo 感測器")
        st.checkbox("三腳架")
    with c2:
        st.checkbox("個人錢包")
        st.checkbox("延長線")
    
    st.markdown("---")
    data_link = "https://docs.google.com/forms/" 
    # 使用 container_width 讓按鈕填滿
    st.link_button("📝 開啟數據紀錄表", data_link, use_container_width=True)

# [日期選擇器]
st.write("") 
days_list = list(schedule_data.keys())
today_str = datetime.now().strftime("%m/%d")
default_idx = 0
for idx, day in enumerate(days_list):
    if today_str in day:
        default_idx = idx
        break

# 下拉選單
selected_day = st.selectbox("📅 請選擇日期：", days_list, index=default_idx)
events = schedule_data[selected_day]

# [全程導航按鈕]
if len(events) > 1:
    st.write("")
    full_route = get_full_route_url(events)
    # 這裡不使用 type="primary"，強制使用我們自定義的 CSS
    st.link_button(
        f"🗺️ 啟動 Day {selected_day.split(' ')[2]} 全程導航", 
        full_route, 
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

    # 渲染卡片 (HTML)
    st.markdown(f"""
    <div class="event-card">
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <span class="time-text">{event['time']}</span>
            <span class="tag">{icon} {event['note']}</span>
        </div>
        <div class="loc-text">{event['loc']}</div>
        <div class="addr-text">🏠 {event['addr']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按鈕區
    col_main, col_sub1, col_sub2, col_sub3 = st.columns([3, 1, 1, 1])
    
    with col_main:
        st.link_button("📍 導航", get_google_maps_url(event['addr']), use_container_width=True)
    
    with col_sub1:
        st.link_button("🅿️", get_nearby_url(event['addr'], "parking"), help="找停車", use_container_width=True)
    with col_sub2:
        st.link_button("🍱", get_nearby_url(event['addr'], "food"), help="找美食", use_container_width=True)
    with col_sub3:
        st.link_button("☕", get_nearby_url(event['addr'], "coffee"), help="找咖啡", use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
