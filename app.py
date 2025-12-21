import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="EO Swim Tour", page_icon="🏊", layout="centered")

# --- 2. 品牌色彩 CSS 與 LOGO 配置 ---
st.markdown("""
    <style>
    /* =========================================
       1. 品牌色彩定義 (源自勝競運動文化 LOGO)
       ========================================= */
    :root {
        --brand-blue: #0072CE;    /* Pantone 7688 C */
        --brand-red: #D03027;     /* Pantone 7597 C */
        --brand-yellow: #EACE2B;  /* Pantone 610 C */
        --brand-green: #009B48;   /* Pantone 7738 C */
        --text-black: #000000;
        --bg-light: #F8F9FA;      /* 淺灰白背景 */
    }

    /* =========================================
       2. 全域強制亮色設定
       ========================================= */
    html, body, [data-testid="stAppViewContainer"] {
        color-scheme: light !important;
        background-color: var(--bg-light) !important;
        color: var(--text-black) !important;
    }
    p, h1, h2, h3, h4, h5, h6, span, div, label, li, a {
        color: var(--text-black) !important;
    }

    /* =========================================
       3. 下拉選單 (Selectbox) 修復
       ========================================= */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid var(--brand-blue) !important;
        color: var(--text-black) !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul {
        background-color: #ffffff !important;
    }
    li[role="option"] {
        background-color: #ffffff !important;
        color: var(--text-black) !important;
        border-bottom: 1px solid #f0f0f0 !important;
    }
    div[data-baseweb="menu"] span {
        color: var(--text-black) !important;
    }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #E6F0FF !important;
        color: var(--brand-blue) !important;
    }

    /* =========================================
       4. 按鈕 (Link Button) 品牌化
       ========================================= */
    /* 通用按鈕樣式：強制亮色、品牌藍框、黑字 */
    div[data-testid="stLinkButton"] a {
        color-scheme: light !important;
        background-color: #ffffff !important;
        color: var(--text-black) !important;
        border: 2px solid var(--brand-blue) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        font-weight: 800 !important;
        -webkit-text-fill-color: var(--text-black) !important;
        text-decoration: none !important;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stLinkButton"] a:active {
        background-color: #eee !important;
        transform: scale(0.98);
    }

    /* --- 針對不同功能按鈕的色彩客製化 --- */
    
    /* [全程導航] & [單點導航]：使用品牌藍 */
    /* 這裡使用 CSS 選擇器技巧，預設所有按鈕都是藍色 */

    /* [找停車 🅿️]：使用品牌藍 (與導航一致) */
    div[data-testid="column"]:nth-child(2) div[data-testid="stLinkButton"] a {
        border-color: var(--brand-blue) !important;
        color: var(--brand-blue) !important;
        -webkit-text-fill-color: var(--brand-blue) !important;
    }

    /* [找美食 🍱]：使用品牌紅 */
    div[data-testid="column"]:nth-child(3) div[data-testid="stLinkButton"] a {
        border-color: var(--brand-red) !important;
        color: var(--brand-red) !important;
        -webkit-text-fill-color: var(--brand-red) !important;
    }

    /* [找咖啡 ☕]：使用品牌黃 */
    div[data-testid="column"]:nth-child(4) div[data-testid="stLinkButton"] a {
        border-color: var(--brand-yellow) !important;
        color: #9A8B1F !important; /* 黃色文字稍微調深一點，增加閱讀性 */
        -webkit-text-fill-color: #9A8B1F !important;
    }

    /* [開啟數據紀錄表]：使用品牌綠 */
    /* 透過上一層的 div 來定位這個單獨的按鈕 */
    .st-emotion-cache-13ln4jf div[data-testid="stLinkButton"] a {
        border-color: var(--brand-green) !important;
        color: var(--brand-green) !important;
        -webkit-text-fill-color: var(--brand-green) !important;
    }

    /* =========================================
       5. 卡片與標籤樣式
       ========================================= */
    .event-card {
        background-color: #ffffff !important;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        border: 1px solid #eee;
        border-left: 5px solid var(--brand-blue); /* 預設藍色側邊條 */
    }
    .time-text { font-size: 1.4rem; font-weight: 900; color: var(--text-black) !important; margin-right: 8px;}
    .loc-text { font-size: 1.2rem; font-weight: 800; color: var(--text-black) !important; margin-top: 5px;}
    .addr-text { font-size: 1rem; color: #555 !important; margin-bottom: 10px; display: flex; align-items: center;}
    
    /* 標籤 (Tag) - 根據類型變色 */
    .tag { padding: 3px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; color: #fff !important; -webkit-text-fill-color: #fff !important;}
    .tag-swim { background-color: var(--brand-blue) !important; }
    .tag-travel { background-color: var(--brand-red) !important; }
    .tag-sleep { background-color: var(--brand-green) !important; }

    /* =========================================
       6. 頂部 Logo 橫幅
       ========================================= */
    .logo-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #fff;
        padding: 10px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .logo-img {
        height: 60px; /* 調整 Logo 高度 */
        width: auto;
        object-fit: contain;
    }

    /* 隱藏 Footer/Header */
    footer, header {display: none !important;}
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

# --- 4. 輔助函式 (連結產生器) ---
def get_google_maps_url(address):
    return f"http://googleusercontent.com/maps.google.com/maps?daddr={urllib.parse.quote(address)}"

def get_full_route_url(events):
    base = "https://www.google.com/maps/dir/"
    addrs = [urllib.parse.quote(e['addr']) for e in events]
    return base + "/".join(addrs)

def get_nearby_url(address, query):
    return f"https://www.google.com/maps/search/{query}+near+{urllib.parse.quote(address)}"

# --- 5. 主程式介面 ---

# [Hero 區塊 - 品牌 Logo 橫幅]
# 請注意：這裡使用網路上的圖片連結作為範例，實際部署時建議將圖片上傳到 GitHub 並使用相對路徑
logo_sj_swim = "https://i.imgur.com/8Q5Xq9r.png" # 假設的 SJ Swim Logo 連結
logo_s_sport = "https://i.imgur.com/0a3X6Q1.png" # 假設的勝競 Logo 連結

st.markdown(f"""
    <div class="logo-banner">
        <img src="{logo_s_sport}" class="logo-img" alt="勝競運動文化">
        <div style="text-align: center;">
            <div style="font-size: 1.4rem; font-weight: 900; color: var(--brand-blue);">EO Swim Tour 2025</div>
            <div style="font-size: 0.9rem; color: #666;">環島檢測任務助手</div>
        </div>
        <img src="{logo_sj_swim}" class="logo-img" alt="SJ Swim Training">
    </div>
""", unsafe_allow_html=True)

# [數據紀錄表按鈕]
data_link = "https://docs.google.com/forms/" 
st.link_button("📝 開啟數據紀錄表 (Google Form)", data_link, use_container_width=True)

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
    st.link_button(
        f"🗺️ 啟動 Day {selected_day.split(' ')[2]} 全程導航", 
        full_route, 
        use_container_width=True
    )

st.write("") 

# [行程卡片 Loop]
for event in events:
    # 決定 icon 與 tag 顏色
    icon = "📍"
    tag_class = "tag-swim" # 預設
    if event.get('type') == "swim": 
        icon = "🏊"
        tag_class = "tag-swim"
    elif event.get('type') == "travel": 
        icon = "🚗"
        tag_class = "tag-travel"
    elif event.get('type') == "sleep": 
        icon = "🛌"
        tag_class = "tag-sleep"

    # 渲染卡片 (HTML)
    st.markdown(f"""
    <div class="event-card" style="border-left-color: var(--brand-{tag_class.split('-')[1]});">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span class="time-text">{event['time']}</span>
            <span class="tag {tag_class}">{icon} {event['note']}</span>
        </div>
        <div class="loc-text">{event['loc']}</div>
        <div class="addr-text">🏠 {event['addr']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按鈕區
    col_main, col_sub1, col_sub2, col_sub3 = st.columns([3, 1, 1, 1])
    
    with col_main:
        # 導航按鈕 (品牌藍)
        st.link_button("📍 導航", get_google_maps_url(event['addr']), use_container_width=True)
    
    with col_sub1:
        # 找停車 (品牌藍)
        st.link_button("🅿️", get_nearby_url(event['addr'], "parking"), help="找停車", use_container_width=True)
    with col_sub2:
        # 找美食 (品牌紅)
        st.link_button("🍱", get_nearby_url(event['addr'], "restaurants"), help="找美食", use_container_width=True)
    with col_sub3:
        # 找咖啡 (品牌黃)
        st.link_button("☕", get_nearby_url(event['addr'], "coffee"), help="找咖啡", use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
