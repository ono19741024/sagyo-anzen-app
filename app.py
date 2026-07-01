import streamlit as st
import os

# ページの設定
st.set_page_config(layout="wide", page_title="地質調査・点検 安全支援アプリ")

# --- ⚙️ 法令データの読み込み ---
@st.cache_data
def load_all_laws(data_dir="data"):
    laws_data = {}
    if not os.path.exists(data_dir):
        return laws_data
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    laws_data[filename.replace(".txt", "")] = f.readlines()
            except Exception:
                pass
    return laws_data

laws_dict = load_all_laws()

# --- 🖥️ アプリ画面の構築 ---
st.title("👷 地質調査・点検専門 安全衛生管理システム")

tab1, tab2, tab3 = st.tabs(["📝 現場基本情報", "✅ 特化型安全チェック", "🔍 関連法令・条文検索"])

# ==========================================
# 【タブ1】基本情報入力
# ==========================================
with tab1:
    st.subheader("📋 調査・点検現場の概要")
    col1, col2 = st.columns(2)
    with col1:
        site_name = st.text_input("業務名・現場名", placeholder="例：〇〇地区 地質調査業務")
        location = st.text_input("調査・点検場所", placeholder="例：〇〇川沿い斜面、〇〇ピット内")
    with col2:
        patrol_date = st.date_input("安全巡視・点検日")
        manager = st.text_input("現場責任者（職長）", placeholder="例：山田 太郎")

# ==========================================
# 【タブ2】6大リスク特化型チェックリスト
# ==========================================
with tab2:
    st.subheader("⚠️ 現場の危険作業チェック（自動法規判定）")
    st.write("本日の作業に該当する項目にチェックを入れてください。必須の安全対策と資格が表示されます。")
    
    st.markdown("#### 🔍 本日の該当作業を選択（複数選択可）")
    c_high = st.checkbox("🚩 1. 高所作業（法面、2m以上の足場、昇降、ロープ高所作業など）")
    c_rotate = st.checkbox("🚩 2. 回転部のある機械（ボーリングマシン、研削盤などの使用）")
    c_unic = st.checkbox("🚩 3. 2tユニック車（移動式クレーン・つり上げ荷重5t未満）の使用")
    c_oxygen = st.checkbox("🚩 4. 酸欠危険作業（たて坑、井戸、ピット、暗渠、槽内への立ち入り）")
    c_heat = st.checkbox("🚩 5. 暑熱環境での作業（気温が高い、直射日光下など熱中症の危険がある作業）")
    c_aerial = st.checkbox("🚩 6. 高所作業車の使用")
    
    st.markdown("---")
    current_site_title = f"### 💡 {site_name} の安全対策基準" if site_name else "### 💡 本日の安全対策基準"
    st.markdown(current_site_title)
    
    any_selected = False

    if c_high:
        any_selected = True
        with st.container():
            st.error("### 🧗 高所作業・墜落防止基準（安衛則 第518条〜）")
            st.markdown("""
            * **【足場の設置】** 高さ2m以上の箇所で作業を行う場合は作業床を設けること。困難な場合は防網を張り、フルハーネス型墜落制止用器具を使用させること。
            * **【ロープ高所作業】** ライフライン（命綱）をメインロープとは別の堅固な支持物に緊結すること。
            * **【昇降設備】** 高さ又は深さが1.5mを超える箇所は、安全に昇降するための設備（はしご等）を設けること。
            """)

    if c_rotate:
        any_selected = True
        with st.container():
            st.error("### 🔄 ボーリングマシン等・巻き込まれ防止基準（安衛則 第101条、第194条の2〜）")
            st.markdown("""
            * **【動力の確実な遮断】** ロッドやビット等の着脱時は、動力を確実に遮断すること。
            * **【確実な保持】** ロッドやビット等の着脱時は、ロッドホルダー等により確実に保持すること。
            * **【服装の制限】** 回転部に巻き込まれるおそれがあるため、作業員に**手袋（軍手など）を使用させてはならない**。
            """)

    if c_unic:
        any_selected = True
        with st.container():
            st.error("### 🏗️ 2tユニック（小型移動式クレーン）就業制限基準（クレーン則・安衛則）")
            st.markdown("""
            * **【運転資格】** つり上げ荷重1t以上5t未満は**『小型移動式クレーン運転技能講習修了証』**が必要。
            * **【玉掛け資格】** 1t以上のクレーン等の玉掛け作業には、**『玉掛け技能講習修了証』**が必要。
            * **【アウトリガー】** 軟弱地盤での転倒を防ぐため、鉄板等を敷き、アウトリガーを最大限張り出すこと。
            """)

    if c_oxygen:
        any_selected = True
        with st.container():
            st.error("### 🌀 酸素欠乏危険作業基準（高圧則・酸欠則・安衛則）")
            st.markdown("""
            * **【作業主任者】** 必ず**『酸素欠乏危険作業主任者』**等を選任し、直接指揮させること。
            * **【濃度測定】** 作業開始前に、酸素濃度（18%以上必須）および硫化水素等の濃度を測定し記録すること。
            * **【換気と救護用具】** 必要な空気の送気と、空気呼吸器・安全帯等の救護用具を現場に常備すること。
            """)

    if c_heat:
        any_selected = True
        with st.container():
            st.error("### 🥵 熱中症予防・緊急対応基準（安衛則 第612条の2、最新ガイドライン等）")
            st.markdown("""
            * **【連絡体制の義務化】** 異常者の早期発見のため、**報告体制（連絡先・担当者）を事前に定め、全員に周知**すること。
            * **【緊急時の手順の義務化】** 作業からの離脱、身体の冷却、緊急連絡網、緊急搬送先など、**症状悪化を防ぐ手順を定め周知**すること。
            * **【環境・作業管理】** 暑さ指数（WBGT値）の把握、こまめな休憩・水分塩分補給、日陰（クーリングシェルター等）の確保を徹底すること。
            * **【健康管理】** 睡眠不足や体調不良者の把握と、必要に応じた配置転換などを行うこと。
            """)

    if c_aerial:
        any_selected = True
        with st.container():
            st.error("### 🚙 高所作業車の使用基準（安衛則 第36条、第194条の9〜）")
            st.markdown("""
            * **【運転資格】** 作業床の高さが**10m以上**の場合は**『高所作業車運転技能講習修了証』**が、**10m未満**の場合は**『特別教育』**の受講が必要。
            * **【要求性能墜落制止用器具の使用】** 作業床上の労働者には、必ず**墜落制止用器具（フルハーネス等）**を使用させること。
            * **【転落・逸走防止】** アウトリガーを張り出すこと。運転者が運転位置から離れるときは、作業床を最低降下位置に置き、ブレーキを確実にかけること。
            """)

    if not any_selected:
        st.info("上のチェックボックスを選択すると、該当作業の安全法規ルールがここに自動表示されます。")

# ==========================================
# 【タブ3】全法令 全文検索システム
# ==========================================
with tab3:
    st.subheader("🔍 搭載法令 全文検索エンジン")
    
    st.markdown("**💡 現場キーワードで一発検索：**")
    shortcut_cols = st.columns(6)
    
    # ボタンに「熱中症」を追加しました！
    keywords_buttons = ["ボーリング", "ロープ高所作業", "熱中症", "高所作業車", "移動式クレーン", "酸素欠乏"]
    
    selected_kw = ""
    for i, kw in enumerate(keywords_buttons):
        if shortcut_cols[i].button(kw, key=f"btn_{kw}"):
            selected_kw = kw

    search_query = st.text_input("🔍 検索キーワードを入力：", value=selected_kw)

    if search_query:
        st.markdown("---")
        if not laws_dict:
            st.warning("⚠️ `data` フォルダに法令テキストが配置されていません。")
        else:
            total_hit = 0
            for law_name, lines in laws_dict.items():
                law_hits = []
                for line in lines:
                    if search_query in line:
                        law_hits.append(line.strip())
                        total_hit += 1
                
                if law_hits:
                    with st.expander(f"📘 {law_name}（該当: {len(law_hits)}件）", expanded=False):
                        for hit in law_hits:
                            highlighted_text = hit.replace(search_query, f"**{search_query}**")
                            st.write(f"・ {highlighted_text}")
            
            if total_hit > 0:
                st.success(f"🎉 合計 {total_hit} 件の関連記述が見つかりました！")
            else:
                st.warning("該当する記述が見つかりませんでした。")