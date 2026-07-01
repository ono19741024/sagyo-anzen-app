import streamlit as st
import os

# ページの設定（白と水色を基調にした見やすいデザイン）
st.set_page_config(layout="wide", page_title="安全支援アプリ")

# --- ⚙️ 法令データの読み込み（キャッシュ機能付き） ---
@st.cache_data
def load_all_laws(data_dir="data"):
    laws_data = {}
    if not os.path.exists(data_dir):
        return laws_data
    
    # フォルダ内のすべてのテキストファイルを読み込む
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
st.title("👷 安全衛生管理システム")

# 画面を3つのタブに分割
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
# 【タブ2】4大リスク特化型チェックリスト
# ==========================================
with tab2:
    st.subheader("⚠️ 現場の危険作業チェック（自動法規判定）")
    st.write("本日の作業に該当する項目にチェックを入れてください。必須の安全対策と資格が表示されます。")
    
    # 4大リスクの選択
    st.markdown("#### 🔍 本日の該当作業を選択（複数選択可）")
    c_high = st.checkbox("🚩 1. 高所作業（法面、2m以上の足場、昇降、ロープ高所作業など）")
    c_rotate = st.checkbox("🚩 2. 回転部のある機械（ボーリングマシン、研削盤などの使用）")
    c_unic = st.checkbox("🚩 3. 2tユニック車（移動式クレーン・つり上げ荷重5t未満）の使用")
    c_oxygen = st.checkbox("🚩 4. 酸欠危険作業（たて坑、井戸、ピット、暗渠、槽内への立ち入り）")
    
    st.markdown("---")
    current_site_title = f"### 💡 {site_name} の安全対策基準" if site_name else "### 💡 本日の安全対策基準"
    st.markdown(current_site_title)
    
    any_selected = False

    # 1. 高所作業
    if c_high:
        any_selected = True
        with st.container():
            st.error("### 🧗 高所作業・墜落防止基準（安衛則 第518条〜）")
            st.markdown("""
            * **【足場の設置】** 高さ2m以上の箇所で作業を行う場合は作業床（足場）を設ける必要があります。困難な場合は防網を張り、フルハーネス型墜落制止用器具を正しく着用させてください。
            * **【ロープ高所作業・法面】** ロープ高所作業を行う場合は、メインロープとは別に**『ライフライン（命綱）』**をそれぞれ異なる堅固な支持物に緊結してください。
            * **【昇降設備】** 高さ又は深さが1.5mを超える箇所で作業を行うときは、労働者が安全に昇降するための設備（はしご等）が必要です。
            """)
            st.info("💡 関連チェック：ヘルメット（保護帽）の着用必須 / 悪天候時（強風・大雨等）の作業中止判断基準の確認")

    # 2. 回転部への巻き込まれ
    if c_rotate:
        any_selected = True
        with st.container():
            st.error("### 🔄 ボーリングマシン・回転部巻き込まれ防止基準（安衛則 第101条、第194条の2〜）")
            st.markdown("""
            * **【動力の確実な遮断】** ロッドやビット等を取り付け・取り外すときは、クラッチレバーをストッパーで固定するなど、**回転させる動力を確実に遮断**してください。
            * **【確実な保持】** ロッドを取り外すとき、ビットを取り付け・取り外すときは、ロッドホルダー等により確実に保持してください。
            * **【ホースの固定】** ウォータースイベルに接続するホースは、ロッド等の回転部分に巻き込まれないよう、やぐら等に確実に固定してください。
            * **【服装の制限】** 回転する刃物や軸に巻き込まれるおそれがあるため、作業員に**手袋（軍手など）を使用させてはなりません**。作業帽・袖口の締まった作業服を正しく着用させてください。
            """)

    # 3. 2tユニック（移動式クレーン）の使用
    if c_unic:
        any_selected = True
        with st.container():
            st.error("### 🏗️ 2tユニック（小型移動式クレーン・玉掛け）就業制限基準（クレーン則・安衛則）")
            st.markdown("""
            * **【ユニックの運転資格】** つり上げ荷重1トン以上5トン未満の移動式クレーンの運転には、**『小型移動式クレーン運転技能講習修了証』**の携帯が必要です（道路上の走行を除く）。
            * **【玉掛けの資格】** つり上げ荷重1トン以上のクレーン等の玉掛け作業には、**『玉掛け技能講習修了証』**が必要です。
            * **【地盤の確認とアウトリガー】** 地盤の軟弱な場所での転倒を防ぐため、鉄板等を敷いた上で、**アウトリガーを最大限に張り出して**設置してください。
            * **【立ち入り禁止】** つり上げられている荷の下、および上部旋回体と接触する危険のある箇所への立ち入りを確実に禁止（表示等）してください。
            """)

    # 4. 酸欠作業
    if c_oxygen:
        any_selected = True
        with st.container():
            st.error("### 🌀 酸素欠乏危険作業基準（高圧則・酸欠則・安衛則）")
            st.markdown("""
            * **【作業主任者の選任】** 酸素欠乏危険場所（たて坑、長期間使用されていない井戸、ピット等）における作業では、必ず**『酸素欠乏危険作業主任者』**を選任し、直接指揮させてください。
            * **【事前の濃度測定】** 当日の作業を開始する前に、必ず**酸素濃度（18%以上必須）**および硫化水素等のガス濃度を測定し、記録してください。
            * **【換気の実施】** 換気設備を設け、必要な量の空気を常時送り込んでください（測定で安全が確認されるまで入室禁止）。
            * **【救護用具の備付け】** 非常時に備え、空気呼吸器等、携帯用照明器具、引き上げ用の繊維ロープなどの救護用具を必ず現場に常備してください。
            """)

    if not any_selected:
        st.info("上のチェックボックスを選択すると、御社の地質調査・点検業務に直結する労働安全衛生法上のルールがここに自動表示されます。")

# ==========================================
# 【タブ3】全法令 全文検索システム
# ==========================================
with tab3:
    st.subheader("🔍 搭載法令 全文検索エンジン")
    st.write("dataフォルダ内の全法令テキストから、キーワードが含まれる条文を一瞬で検索します。")
    
    # 御社の業務に合わせた特化キーワードボタン
    st.markdown("**💡 現場キーワードで一発検索：**")
    shortcut_cols = st.columns(5)
    keywords_buttons = ["ボーリング", "ロープ高所作業", "移動式クレーン", "玉掛け", "酸素欠乏"]
    
    selected_kw = ""
    for i, kw in enumerate(keywords_buttons):
        if shortcut_cols[i].button(kw, key=f"btn_{kw}"):
            selected_kw = kw

    # 検索窓
    search_query = st.text_input("🔍 検索キーワードを入力（例：手袋、アウトリガー、支持物、測定）：", value=selected_kw)

    if search_query:
        st.markdown("---")
        if not laws_dict:
            st.warning("⚠️ `data` フォルダに法令テキスト（.txt）が配置されていないか、読み込めていません。")
        else:
            total_hit = 0
            for law_name, lines in laws_dict.items():
                law_hits = []
                for line in lines:
                    if search_query in line:
                        law_hits.append(line.strip())
                        total_hit += 1
                
                # 該当があった法令だけを折りたたみで表示
                if law_hits:
                    with st.expander(f"📘 {law_name}（該当: {len(law_hits)}件）", expanded=False):
                        for hit in law_hits:
                            # キーワードを太字にする
                            highlighted_text = hit.replace(search_query, f"**{search_query}**")
                            st.write(f"・ {highlighted_text}")
            
            if total_hit > 0:
                st.success(f"🎉 すべての法令から、合計 {total_hit} 件の関連記述が見つかりました！")
            else:
                st.warning("該当する記述が見つかりませんでした。別のキーワードに変えてみてください。")