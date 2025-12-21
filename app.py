import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="EO Swim Tour", page_icon="🏊", layout="centered")

# --- 2. 核彈級 CSS 強制覆蓋 (針對截圖問題修復) ---
st.markdown("""
    <style>
    /* =========================================
       1. 全域強制亮色 (Force Light Theme)
       這會告訴瀏覽器：此網頁不支援深色模式
       ========================================= */
    :root {
        color-scheme: light !important;
    }
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f6f9 !important; /* 淺灰白背景 */
        color: #000000 !important;
    }
    
    /* 強制所有文字顏色為深黑 */
    p, h1, h2, h3, h4, h5, h6, span, div, label, li, a {
        color: #000000 !important;
    }

    /* =========================================
       2. 下拉選單 (Selectbox) 深度修復 (圖2問題)
       ========================================= */
    /* 輸入框本體 */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
        color: #000000 !important;
    }
    
    /* 關鍵：下拉後的清單容器 (Popover) */
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        border: 1px solid #ccc !important;
    }
    
    /* 關鍵：清單內的選項列表 */
    div[data-baseweb="menu"], ul {
        background-color: #ffffff !important;
    }
    
    /* 關鍵：單一選項 (Option) */
    li[role="option"] {
        background-color: #ffffff !important; /* 強制白底 */
        color: #000000 !important;            /* 強制黑字 */
        border-bottom: 1px solid #f0f0f0 !important;
    }
    
    /* 選項文字 */
    div[data-baseweb="menu"] span {
        color: #000000 !important;
    }

    /* 滑鼠滑過 / 手指按下的反白效果 */
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #e6f7ff !important; /* 淺藍色高亮 */
        color: #000000 !important;
    }

    /* =========================================
       3. 按鈕 (Link Button) 深度修復 (圖1問題)
       包含：導航、找停車、找美食、找咖啡
       ========================================= */
    
    /* 針對所有 stLinkButton 內的 <a> 標籤 */
    div[data-testid="stLinkButton"] a {
        background-color: #ffffff !important;   /* 絕對白底 */
        color: #000000 !important;              /* 絕對黑字 */
        border: 2px solid #0066cc !important;   /* 深藍邊框 */
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        font-weight: 800 !important;
        
        /* 確保 Safari/iPhone 不會反轉顏色 */
        -webkit-text-fill-color: #000000 !important; 
    }

    /* 針對「欄位 (Column)」內的小按鈕特別加強權重 */
    div[data-testid="column"] div[data-testid="stLinkButton"] a {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #333333 !important; /* 小按鈕用深灰框，區分層級 */
    }

    /* 按下效果 */
    div[data-testid="stLinkButton"] a:active {
        background-color: #ddd !important;
    }

    /* =========================================
       4. 任務工具箱 (Expander)
       ========================================= */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #ccc !important;
        color: #000000 !important;
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    div[data-testid="stExpander"] summary {
        color: #000000 !important; 
    }
    /* Checkbox 文字 */
    div[data-testid="stCheckbox"] label span {
        color: #000000 !important;
    }

    /* =========================================
       5. 卡片樣式 (維持清晰)
       ========================================= */
    .event-card {
        background-color: #ffffff !important;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border: 1px solid #bbb; /* 加深邊框 */
    }
    .time-text { font-size: 1.4rem; font-weight: 900; color: #000 !important; margin-right: 8px;}
    .loc-text { font-size: 1.2rem; font-weight: 800; color: #0056b3 !important; margin-top: 5px;}
    .addr-text { font-size: 1rem; color: #333 !important; margin-bottom: 10px;}
    .tag { background: #eee !important; color: #000 !important; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;}

    /* 隱藏 Footer */
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
    # 不使用 type='primary'，確保使用我們的 CSS
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
    
    # 按鈕區 (使用 Streamlit 原生 Columns)
    col_main, col_sub1, col_sub2, col_sub3 = st.columns([3, 1, 1, 1])
    
    with col_main:
        st.link_button("📍 導航", get_google_maps_url(event['addr']), use_container_width=True)
    
    # 這三個小按鈕現在應該會是白底黑字了
    with col_sub1:
        st.link_button("🅿️", get_nearby_url(event['addr'], "parking"), help="找停車", use_container_width=True)
    with col_sub2:
        st.link_button("🍱", get_nearby_url(event['addr'], "food"), help="找美食", use_container_width=True)
    with col_sub3:
        st.link_button("☕", get_nearby_url(event['addr'], "coffee"), help="找咖啡", use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
