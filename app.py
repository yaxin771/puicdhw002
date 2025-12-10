import streamlit as st
from openai import OpenAI

# 1. 頁面設定 (必須是第一個執行的指令)
st.set_page_config(page_title="AI 辯論軍師", layout="wide", page_icon="⚔️")

# 2. 隱藏 Streamlit 預設標示 (CSS 魔法)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* 調整頂部留白 */
            .block-container {
                padding-top: 1rem;
            }
            /* 讓按鈕更好看 */
            .stButton>button {
                width: 100%; 
                border-radius: 8px; 
                font-weight: bold;
                background-color: #f0f2f6; 
                border: 1px solid #d1d5db;
                transition: all 0.2s; /* 增加過渡效果 */
            }
            .stButton>button:hover {
                border-color: #1E3A8A;
                color: #1E3A8A;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 增加陰影 */
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. 初始化 OpenAI Client (直接寫入 Key)
# ==========================================
# 👇 請在這裡填入您的 API Key (務必修改)
my_secret_key = "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" 
# ==========================================

try:
    client = OpenAI(api_key=my_secret_key)
except Exception as e:
    st.error(f"API Key 設定有誤，請檢查代碼：{e}")
    st.stop()

# 4. 側邊欄：功能選擇
with st.sidebar:
    st.title("🛡️ 辯論軍師控制台")
    mode = st.radio("選擇功能模式", 
        ["📝 生成辯論稿", "🔥 改寫攻辯問題", "🛡️ 偵測謬誤", "🎯 弱點分析(強)", "⚔️ 交互詰問策略"])
    
    st.markdown("---")
    st.markdown("### 💡 使用提示")
    if mode == "🎯 弱點分析(強)":
        st.caption("深層邏輯解構，找出論點『死穴』。")
    elif mode == "🛡️ 偵測謬誤":
        st.caption("快速分析對方語句中的邏輯漏洞。")
    elif mode == "⚔️ 交互詰問策略":
        st.caption("自動產出決策樹狀的攻防劇本。")

# 5. 主畫面邏輯
st.markdown(f"## {mode}") 

# --- 核心功能區塊 ---

# 🎯 弱點分析 (保持不變)
if mode == "🎯 弱點分析(強)":
    # (此處代碼與上次一致，省略以保持代碼簡潔性，請使用原代碼)
    st.info("此模式將進行深度的邏輯解構，找出對方論點的『死穴』。")
    opponent_arg = st.text_area("請輸入對方論點/講稿：", height=200, placeholder="在此貼上對方的立論...")
    
    if st.button("🚀 開始毀滅性分析"):
        if not opponent_arg:
            st.warning("請先輸入對方的論點。")
        else:
            with st.spinner("AI 正在尋找邏輯漏洞..."):
                system_prompt = """
                你是一個冷酷無情的邏輯學家與辯論教練。你的任務是使用 Chain-of-Thought 思維鏈，
                對使用者的輸入進行『致命的』弱點分析。
                輸出格式必須包含：
                1. **核心矛盾**：用一句話點破其立論最深層的內在衝突。
                2. **邏輯斷鏈**：具體指出其論證中，從數據到結論的連接（Warrant）失敗在哪裡。
                3. **隱藏假設反駁**：找出對方沒有說出來、但偷偷使用的假設，並提出反例。
                4. **必殺追問**：提供三個讓對方無法圓場的連環質詢問題。
                """
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o", 
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": opponent_arg}
                        ]
                    )
                    st.markdown("### 📊 分析報告")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"發生錯誤：{e}")


# 🛡️ 偵測謬誤 (新增內容)
elif mode == "🛡️ 偵測謬誤":
    st.info("貼上對方的語句，AI 將列出其中包含的邏輯謬誤並提供反擊建議。")
    opponent_text = st.text_area("輸入對方的一段關鍵發言或論證：", height=150, placeholder="例如：你這個觀點根本就是想讓社會倒退！所以不對。")

    if st.button("🚨 偵測並反擊謬誤"):
        if not opponent_text:
            st.warning("請輸入文本進行分析。")
        else:
            with st.spinner("AI 正在比對常見謬誤類型..."):
                # 專門針對謬誤的 System Prompt
                fallacy_prompt = """
                你是一名嚴格的邏輯審查員。請分析以下文本，並以表格形式清晰輸出：
                
                表格標題：
                | 偵測到的原文 | 邏輯謬誤類型 | 謬誤簡析 | 建議的反擊話術 |
                
                常見謬誤包括但不限於：人身攻擊(Ad Hominem)、稻草人(Straw Man)、滑坡謬誤(Slippery Slope)、訴諸權威、訴諸情感、非黑即白、偷換概念、循環論證。
                
                請務必指出對方的論證是如何違反邏輯的。
                """
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o", 
                        messages=[
                            {"role": "system", "content": fallacy_prompt},
                            {"role": "user", "content": opponent_text}
                        ]
                    )
                    st.markdown("### 📝 謬誤分析與反擊建議")
                    # 使用 Markdown 渲染表格
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"偵測發生錯誤：{e}")


# ⚔️ 交互詰問策略 (新增內容)
elif mode == "⚔️ 交互詰問策略":
    st.info("輸入您想攻擊的對方核心論點，AI 將生成一套樹狀的詰問劇本。")
    target_claim = st.text_area("您想質詢的對方核心主張或數據：", height=100, placeholder="例如：對方說『我國死刑能有效嚇阻犯罪』")
    target_goal = st.text_input("您的質詢目標", placeholder="例如：迫使對方承認嚇阻力缺乏實證數據支持")

    if st.button("⚔️ 生成詰問劇本"):
        if not target_claim or not target_goal:
            st.warning("請輸入攻擊對象和您的目標。")
        else:
            with st.spinner("正在為您設計一擊必殺的詰問流程..."):
                # 專門針對交互詰問的 System Prompt (決策樹結構)
                strategy_prompt = f"""
                你是一名擅長設計劇本的頂尖質詢辯手。
                目標：針對對方的主張『{target_claim}』，達成『{target_goal}』這個質詢目標。
                請設計一套包含 5-7 個問題的**樹狀**交互詰問劇本。
                
                輸出格式必須為清晰的流程圖/大綱，包含對方的『可能回應』以及您的『追擊話術』：

                **質詢劇本 (目標：{target_goal})**
                
                I. 基礎鋪墊 (確認定義或數據來源)
                Q1: [您的第一個問題，必須是封閉式 Yes/No 問題]
                    A. 若對方回答 Yes (承認): [追擊問題 1A - 鎖定矛盾點]
                    B. 若對方回答 No (否認): [追擊問題 1B - 質疑其定義或來源]
                    C. 若對方閃避 (解釋): [拉回話術 - 例如：請您直接回答『是』或『否』。]

                II. 核心質疑 (攻擊數據或鏈接)
                Q2: ... (依此類推，至少設計兩層次的追問)
                
                III. 結論收束 (達成目標)
                Q Final: [一個總結性問題，用來將前面的回答串聯起來，達到您的最終目標]
                """
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o", 
                        messages=[
                            {"role": "system", "content": strategy_prompt},
                            {"role": "user", "content": f"目標：{target_goal}"}
                        ]
                    )
                    st.markdown("### 📝 詰問策略劇本")
                    # 使用 Markdown 呈現流程圖效果
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"生成策略時發生錯誤：{e}")

# --- 其他功能 (如生成辯論稿、改寫攻辯問題) (保持不變，省略代碼)
elif mode == "📝 生成辯論稿":
    # ... (請沿用您上次的程式碼)
    st.info("輸入辯題與持方，自動生成結構嚴謹的申論稿。")
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("辯題", placeholder="例如：我國應廢除死刑")
    with col2:
        side = st.selectbox("持方", ["正方 (支持)", "反方 (反對)"])
    
    details = st.text_area("補充觀點 (可選)", placeholder="如果您有特定的論點想要 AI 擴寫，請填在此處...")

    if st.button("📝 生成申論稿"):
        if not topic:
            st.warning("請輸入辯題。")
        else:
            with st.spinner("正在撰寫高說服力的稿件..."):
                draft_prompt = f"""
                你是一位專業的辯論寫手。請針對辯題『{topic}』，為『{side}』撰寫一份一辯申論稿。
                要求：
                1. 採用圖爾敏論證模式 (Toulmin Model)。
                2. 結構清晰：包含定義、三個核心論點、結尾昇華。
                3. 語氣堅定、邏輯嚴密。
                4. 如果使用者有提供補充觀點：『{details}』，請務必融入其中。
                """
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": draft_prompt},
                            {"role": "user", "content": f"辯題：{topic}"}
                        ]
                    )
                    st.markdown("### 📝 申論初稿")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"發生錯誤：{e}")


elif mode == "🔥 改寫攻辯問題":
    # ... (請沿用您上次的程式碼)
    st.info("將您的問題轉化為具有壓迫性的封閉式陷阱題！")
    raw_question = st.text_area("輸入您想問的草稿問題：", height=100, placeholder="例如：我想問他為什麼覺得廢死比較好？")
    
    if st.button("✨ 優化問題"):
        if not raw_question:
            st.warning("請輸入問題草稿。")
        else:
            with st.spinner("正在進行修辭與邏輯優化..."):
                rewrite_prompt = f"""
                請扮演頂尖辯論賽質詢手。將以下問題：『{raw_question}』改寫為：
                1. **封閉式 Yes/No 問題**：迫使對方只能用『是』或『否』回答，並且回答『是』時會落入您的陷阱。
                2. **具有強烈引導性的修辭**：使用『難道...』、『請問您是否承認...』等語氣。
                3. **提供一句追擊語句**：如果對方閃避或試圖解釋，您可以用這句語句拉回主軸。
                """
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": rewrite_prompt},
                            {"role": "user", "content": raw_question}
                        ]
                    )
                    st.markdown("### ✨ 優化結果")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"發生錯誤：{e}")