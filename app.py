import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Life Echo Ver.4", page_icon="🎨")

# --- 1. タイトルと現在のムード ---
st.title("🎨 Life Echo: Visualizer")

# セッションの初期化（前回のまま）
if 'history' not in st.session_state:
    st.session_state['history'] = []
    st.session_state['history'].append({"day": 0, "tempo": 100, "power": 50, "mood": "Neutral"})

# 最新データの取得
last_data = st.session_state['history'][-1]
current_tempo = last_data['tempo']
current_power = last_data['power']

# --- 2. ムード判定ロジック (色・画像・そして「音」を決める) ---
if current_power > 80:
    display_mood = "🔥 BURNING (激しい)"
    display_color = "red"
    image_url = "https://images.unsplash.com/photo-1485470733090-0aae1788d5af?w=600&q=80"
    # 激しい曲 (SoundHelix-Song-15)
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3"
    message = "エネルギー限界突破！脳汁が出るような轟音が鳴り響きます。"
    
elif current_tempo < 80:
    display_mood = "💧 CHILL (穏やか)"
    display_color = "blue"
    image_url = "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=600&q=80"
    # 静かな曲 (SoundHelix-Song-8)
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
    message = "深い青の世界。心拍数を下げるアンビエント・ノイズです。"

else:
    display_mood = "🌿 NORMAL (通常)"
    display_color = "green"
    image_url = "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&q=80"
    # 普通の曲 (SoundHelix-Song-1)
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    message = "平常運転モード。作業用BGMとして最適なリズムです。"
    
# --- 3. UI表示エリア ---

# カラム分け: 左に画像、右に操作ボタン
col1, col2 = st.columns([1, 1.5])

with col1:
    # ムードに合わせて画像を表示
    st.image(image_url, caption=f"Current Mood: {display_mood}")

with col2:
    # ステータスを色付きで表示
    st.markdown(f"### 状態: :{display_color}[{display_mood}]")
    st.write(message)
    
    st.metric("Tempo (BPM)", current_tempo)
    st.metric("Power", current_power)

    st.divider()

    # シミュレーション関数（前回と同じ）
    def simulate_day(current_data, day_count):
        new_tempo = current_data['tempo']
        new_power = current_data['power']
        event = random.choice(["Run", "Sleep", "Party", "Work", "Stress"])
        
        log_text = ""
        if event == "Run":
            new_tempo += 10; new_power += 5; log_text = "🏃 走った"
        elif event == "Sleep":
            new_tempo -= 5; new_power -= 10; log_text = "🛌 寝た"
        elif event == "Party":
            new_tempo += 15; new_power += 20; log_text = "🎉 騒いだ"
        elif event == "Stress":
            new_power += 30; log_text = "💢 イライラした" # パワーが一気に上がる！
        elif event == "Work":
            new_power += 5; log_text = "💼 働いた"

        # 0未満や200以上にならないように制限
        new_tempo = max(60, min(200, new_tempo))
        new_power = max(0, min(100, new_power))

        return {"day": day_count, "tempo": new_tempo, "power": new_power, "event": log_text}

    # ボタン
    if st.button("📅 次の日へ (Evolve)", type="primary"):
        next_day = last_data['day'] + 1
        new_day_data = simulate_day(last_data, next_day)
        st.session_state['history'].append(new_day_data)
        st.rerun()
        
    if st.button("🗑️ リセット"):
        st.session_state['history'] = []
        st.session_state['history'].append({"day": 0, "tempo": 100, "power": 50, "mood": "Neutral"})
        st.rerun()

    # ▼▼▼ 追加した部分 ▼▼▼
    st.divider() 
    st.write("🎵 Sound Check")
    if st.button("▶ 今の音を聴く"):
        st.audio(audio_url)
    # ▲▲▲ ここまで ▲▲▲

# --- 4. グラフエリア (下部) ---
st.subheader("📊 成長の軌跡")
df = pd.DataFrame(st.session_state['history'])
st.line_chart(df, x="day", y=["tempo", "power"])