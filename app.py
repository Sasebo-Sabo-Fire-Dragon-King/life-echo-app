import streamlit as st
import requests
import json

# --- ページ設定 ---
st.set_page_config(page_title="Life Echo Ver.6.3", page_icon="🌍", layout="centered")

# CSSデザイン
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    div.stButton > button {
        width: 100%; background: linear-gradient(90deg, #FF4B4B, #FF914D);
        color: white; border: none; border-radius: 30px; padding: 15px;
        font-weight: bold; box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4);
    }
    [data-testid="stMetricValue"] { font-size: 2.5rem; color: #00FFC2; text-shadow: 0px 0px 10px rgba(0, 255, 194, 0.5); }
    /* セレクトボックスも見やすくする */
    .stSelectbox label { color: #FAFAFA; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Life Echo: World Sync")
st.caption("Music generated from the sky above you.")

# --- 都市の座標リスト ---
cities = {
    "Kumamoto": {"lat": 32.8031, "lon": 130.7079},
    "Oita": {"lat": 33.2382, "lon": 131.6126},
    "Tokyo": {"lat": 35.6895, "lon": 139.6917},
    "Osaka": {"lat": 34.6937, "lon": 135.5023},
    "Sapporo": {"lat": 43.0618, "lon": 141.3545},
    "Naha": {"lat": 26.2124, "lon": 127.6809},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "New York": {"lat": 40.7128, "lon": -74.0060}
}

# --- 変更点：サイドバーではなく、メイン画面に置く！ ---
st.write("▼ 場所を選んでください")
# st.sidebar.selectbox ではなく st.selectbox にしました
selected_city = st.selectbox("", list(cities.keys()))

lat = cities[selected_city]["lat"]
lon = cities[selected_city]["lon"]

# --- 関数: 天気取得 ---
def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    return response.json()['current_weather']

# --- スキャンボタン ---
st.write("") # 隙間
if st.button(f"📡 {selected_city} の空をスキャン"):
    
    with st.spinner(f"Connecting to {selected_city} sky..."):
        weather_data = get_weather(lat, lon)
        
        temp = weather_data['temperature']
        code = weather_data['weathercode']
        is_day = weather_data['is_day']
        
        # --- ロジック ---
        if code <= 3:
            weather_status = "Clear/Cloudy"
            mood_base = "Happy"
        elif code >= 51:
            weather_status = "Rain/Snow"
            mood_base = "Melancholy"
        else:
            weather_status = "Other"
            mood_base = "Neutral"

        bpm = int(60 + (temp * 2))
        bpm = max(60, min(180, bpm))
        
        if is_day == 0:
            time_label = "Night 🌙"
            mood_color = "purple"
        else:
            time_label = "Day ☀"
            mood_color = "orange" if mood_base == "Happy" else "blue"

        # --- 表示 ---
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Location", selected_city)
        c2.metric("Temp", f"{temp} °C")
        c3.metric("Weather", weather_status)
        
        st.markdown(f"### Generated Mood: :{mood_color}[{mood_base} {time_label}]")
        
        # 音楽URL
        if mood_base == "Happy":
            audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            img = "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=600&q=80"
        elif mood_base == "Melancholy":
            audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
            img = "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=600&q=80"
        else:
            audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3"
            img = "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=600&q=80"
            
        st.image(img, use_container_width=True)
        if st.button("▶ Play Track"):
            st.audio(audio)