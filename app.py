import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Life Echo Ver.5", page_icon="🧬")

st.title("🧬 Life Echo: Reality Link")
st.write("リアルとバーチャル、2つのモードで音楽を生成します。")

# --- タブを作る（画面の切り替え） ---
tab1, tab2 = st.tabs(["🎮 育成ゲームモード", "📂 リアルデータ分析モード"])

# ==========================================
# 【タブ1】 今までの育成ゲーム（シミュレーション）
# ==========================================
with tab1:
    st.header("育成シミュレーション")
    
    # セッションの初期化
    if 'history' not in st.session_state:
        st.session_state['history'] = []
        st.session_state['history'].append({"day": 0, "tempo": 100, "power": 50})

    # 最新データの取得
    last_data = st.session_state['history'][-1]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tempo", last_data['tempo'])
    with col2:
        st.metric("Power", last_data['power'])

    if st.button("🌞 1日進める (Simulate)"):
        # 簡易シミュレーションロジック
        new_tempo = last_data['tempo'] + random.randint(-10, 10)
        new_power = last_data['power'] + random.randint(-10, 10)
        # 範囲制限
        new_tempo = max(60, min(200, new_tempo))
        new_power = max(0, min(100, new_power))
        
        st.session_state['history'].append({"day": last_data['day']+1, "tempo": new_tempo, "power": new_power})
        st.rerun()

    # グラフ表示
    st.line_chart(pd.DataFrame(st.session_state['history']), x="day", y=["tempo", "power"])


# ==========================================
# 【タブ2】 新機能：リアルデータ分析
# ==========================================
with tab2:
    st.header("📂 ライフログ解析")
    st.write("CSVファイル（date, steps, stress）をアップロードしてください。")
    
    # --- 1. ファイルアップロード ---
    uploaded_file = st.file_uploader("CSVファイルをドロップ", type="csv")
    
    if uploaded_file is not None:
        # CSVを読み込んで表（DataFrame）にする
        df = pd.read_csv(uploaded_file)
        
        st.success("✅ データ読み込み成功！")
        
        # データを表示
        with st.expander("詳細データを見る"):
            st.dataframe(df)
            
        # --- 2. 音楽への変換ロジック ---
        # 読み込んだデータの「最新の日（一番下の行）」を取得
        latest_log = df.iloc[-1]
        
        steps = latest_log['steps']
        stress = latest_log['stress']
        
        st.divider()
        st.subheader(f"📅 最新データ ({latest_log['date']}) の解析結果")
        
        # パラメータ変換: 歩数が多いとテンポUP、ストレスが高いとパワーUP
        music_tempo = int(60 + (steps / 200)) # 20000歩で+100BPM
        music_power = int(stress)
        
        # 範囲制限
        music_tempo = min(180, music_tempo)
        
        # 結果表示
        c1, c2, c3 = st.columns(3)
        c1.metric("歩数 (Steps)", steps)
        c2.metric("生成テンポ (BPM)", music_tempo)
        c3.metric("生成パワー", music_power)
        
        # --- 3. ビジュアルと音楽の判定 (Ver.4のロジックを流用) ---
        if music_power > 70:
            mood = "🔥 BURNING"
            audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3"
            img = "https://images.unsplash.com/photo-1485470733090-0aae1788d5af?w=600&q=80"
        elif music_tempo < 90:
            mood = "💧 CHILL"
            audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
            img = "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=600&q=80"
        else:
            mood = "🌿 NORMAL"
            audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            img = "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&q=80"
            
        st.image(img, caption=f"Mood: {mood}")
        
        st.write("🎵 Generated Track based on REAL DATA")
        st.audio(audio)
        
        # 全期間のグラフ
        st.subheader("📈 期間中の推移")
        st.line_chart(df, x="date", y=["steps", "stress"])