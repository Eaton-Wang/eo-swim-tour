import streamlit as st
import urllib.parse

# --- 設定頁面 ---
st.set_page_config(page_title="EO Swim 環島", page_icon="🏊", layout="centered")

# --- CSS 優化 (手機版面調整) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
    }
    .event-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 5px solid #0066cc;
    }
    .time-text { font-size: 1.2rem; font-weight: 800; color: #333; }
    .note-tag { background: #eee; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; color: #555; margin-left: 10px; }
    .loc-text { font-size: 1.1rem; font-weight: bold; color: #0066cc; margin-top: 5px; }
    .addr-text { font-size: 0.9rem; color: #666; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 資料區 (行程與地址) ---
schedule_data = {
    "12/22 (一) Day 1": [
        {"time": "07:30", "loc": "台南出發", "addr": "台南市", "note": "檢查設備"},
        {"time": "09:00", "loc": "高雄苓雅 (英明國中)", "addr": "高雄市苓雅區英明路166號", "note": "檢測點 1"},
        {"time": "14:30", "loc": "屏東萬巒 (萬巒國中)", "addr": "屏東縣萬巒鄉褒忠路5號", "note": "檢測點 2"},
        {"time": "16:30", "loc": "屏東東港 (東港高中)", "addr": "屏東縣東港鎮東新路1-1號", "note": "檢測點 3"},
    ],
    "12/23 (二) Day 2": [
        {"time": "Morning", "loc": "屏東出發", "addr": "屏東縣", "note": "移動日 (南迴)"},
        {"time": "19:00", "loc": "花蓮市區住宿", "addr": "花蓮縣花蓮市國盛二街22號", "note": "Check-in"},
    ],
    "12/24 (三) Day 3": [
        {"time": "Morning", "loc": "花蓮出發", "addr": "花蓮縣", "note": "前往宜蘭"},
        {"time": "15:00", "loc": "宜蘭市區", "addr": "宜蘭縣宜蘭市校舍路1號", "note": "檢測點"},
        {"time": "19:00", "loc": "基隆暖暖", "addr": "基隆市暖暖區暖暖街350號", "note": "檢測點"},
        {"time": "Night", "loc": "返回永和", "addr": "新北市永和區永平路205號", "note": "住宿"},
    ],
    "12/25 (四) Day 4": [
        {"time": "06:30", "loc": "永和出發", "addr": "新北市永和區永平路205號", "note": "早起"},
        {"time": "09:00", "loc": "北市士林", "addr": "臺北市士林區福志路75號", "note": "檢測點"},
        {"time": "13:30", "loc": "北市松山 (八德路)", "addr": "台北市八德路四段746號", "note": "檢測點"},
        {"time": "19:00", "loc": "新北永和 (永利路)", "addr": "新北市永和區永利路71號", "note": "終點"},
    ],
    "12/26 (五) Day 5": [
        {"time": "Morning", "loc": "新北出發", "addr": "新北市", "note": "前往桃園"},
        {"time": "08:00", "loc": "桃園中壢 (元智大學)", "addr": "桃園市中壢區遠東路135號", "note": "檢測點"},
        {"time": "13:00", "loc": "新竹東區 (光復路)", "addr": "新竹市東區光復路二段101號", "note": "檢測點"},
        {"time": "17:30", "loc": "新竹竹北 (福興東路)", "addr": "新竹縣竹北市福興東路一段199號", "note": "檢測點"},
    ],
    "12/27 (六) Day 6": [
        {"time": "Morning", "loc": "苗栗出發", "addr": "苗栗縣", "note": "前往台中"},
        {"time": "11:00", "loc": "霧峰健體中心", "addr": "臺中市霧峰區成功路200號對面", "note": "檢測點"},
        {"time": "13:00", "loc": "台中北區 (雙十路)", "addr": "臺中市北區雙十路一段16號", "note": "檢測點"},
    ],
    "12/28 (日) Day 7": [
        {"time": "08:00", "loc": "彰化市 (建國東路)", "addr": "彰化縣彰化市建國東路2號", "note": "檢測點"},
        {"time": "10:00", "loc": "彰化員林 (員林大道)", "addr": "彰化縣員林市員林大道二段235號", "note": "檢測點"},
        {"time": "15:00", "loc": "南投埔里 (暨南大學)", "addr": "南投縣埔里鎮大學路1號", "note": "檢測點"},
    ],
    "12/29 (一) Day 8": [
        {"time": "Morning", "loc": "南投出發", "addr": "南投縣", "note": "前往雲嘉"},
        {"time": "15:30", "loc": "雲林虎尾 (北平路)", "addr": "雲林縣虎尾鎮北平路380號", "note": "檢測點"},
        {"time": "17:00", "loc": "嘉義西區 (南京路)", "addr": "嘉義市西區南京路272號", "note": "最終站"},
    ],
}

# --- 輔助函式 ---
def get_google_maps_url(address):
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(address)}"

def get_full_route_url(events):
    # 產生多點導航連結: https://www.google.com/maps/dir/起點/點1/點2...
    base = "https://www.google.com/maps/dir/"
    addrs = [urllib.parse.quote(e['addr']) for e in events]
    return base + "/".join(addrs)

# --- 主程式邏輯 ---
st.title("🏊 EO Swim 環島任務")

# 自動判斷今天日期 (簡單版)
days_list = list(schedule_data.keys())
# 可以加入自動選擇當日的邏輯，這裡先預設選單
selected_day = st.selectbox("請選擇日期：", days_list)

events = schedule_data[selected_day]

st.divider()

# [功能] 今日全程路線按鈕
if len(events) > 1:
    full_route = get_full_route_url(events)
    st.link_button(
        f"🗺️ 開啟 Day {selected_day.split(' ')[2]} 全程導航 ({len(events)}站)", 
        full_route, 
        type="primary"
    )
    st.caption("☝️ 點擊上方按鈕，一次排好整天 Google Maps 路線")

st.markdown("---")

# [功能] 顯示單點卡片
for event in events:
    # 使用 Container 包裝卡片
    with st.container():
        # 自定義 HTML 渲染卡片外觀
        st.markdown(f"""
        <div class="event-card">
            <div>
                <span class="time-text">{event['time']}</span>
                <span class="note-tag">{event['note']}</span>
            </div>
            <div class="loc-text">{event['loc']}</div>
            <div class="addr-text">{event['addr']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 單點導航按鈕
        col1, col2 = st.columns([1, 1])
        with col1:
            st.link_button("📍 單點導航", get_google_maps_url(event['addr']))
        with col2:
            # 這裡預留電話按鈕，若有電話資料可動態生成
            st.button("📞 聯絡場館", disabled=True, key=f"call_{event['time']}")
