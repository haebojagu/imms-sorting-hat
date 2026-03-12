import streamlit as st
from openai import OpenAI

# ──────────────────────────────────────────────────────────
# 1. 페이지 기본 설정
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🪄 KAIST IMMS AI Sorting Hat",
    page_icon="🪄",
    layout="centered",
)

# ──────────────────────────────────────────────────────────
# 2. 전체 스타일링 (해리포터 다크 테마 + 골드 포인트)
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Noto+Serif+KR:wght@400;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css');

:root {
    --gold:        #f5c518;
    --gold-light:  #ffd700;
    --gold-dark:   #c9a227;
    --deep-bg:     #080b14;
    --card-bg:     rgba(14, 20, 40, 0.85);
    --card-border: rgba(197, 165, 49, 0.3);
    --text-primary:   #e8dcc8;
    --text-secondary: #a89880;
}

.stApp {
    background-color: var(--deep-bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(116,0,1,0.08)    0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(14,26,64,0.15)   0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(26,71,42,0.08)   0%, transparent 50%);
    color: var(--text-primary) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

.sorting-header { text-align: center; padding: 2rem 1rem 1.5rem; }
.hat-icon {
    font-size: 4rem; display: block; margin-bottom: 0.4rem;
    filter: drop-shadow(0 0 20px rgba(197,165,49,0.7));
    animation: floatHat 3s ease-in-out infinite;
}
@keyframes floatHat {
    0%,100% { transform: translateY(0) rotate(-3deg); }
    50%      { transform: translateY(-10px) rotate(3deg); }
}
.main-title {
    font-family: 'Cinzel', serif !important;
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #ffd700 0%, #c9a227 50%, #ffd700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.sub-title {
    font-family: 'Cinzel', serif;
    font-size: 0.9rem; color: var(--gold-dark);
    letter-spacing: 3px; text-transform: uppercase;
    margin-top: 0.4rem; opacity: 0.9;
}
.desc-text { font-size: 1rem; color: var(--text-secondary); margin-top: 0.6rem; }
.desc-text span { color: var(--gold); font-weight: 600; }

.magic-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px; padding: 1.6rem 1.8rem; margin-bottom: 1.4rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 30px rgba(197,165,49,0.1), inset 0 1px 0 rgba(197,165,49,0.1);
    position: relative; overflow: hidden;
}
.magic-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0.6;
}
.card-title {
    font-family: 'Cinzel', serif; font-size: 1rem; font-weight: 600;
    color: var(--gold); letter-spacing: 1px; margin-bottom: 1rem;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(197,165,49,0.3) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.3s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    background: rgba(255,255,255,0.08) !important;
    box-shadow: 0 0 0 3px rgba(197,165,49,0.12) !important;
}
label[data-testid="stWidgetLabel"] > div > p {
    color: var(--gold-dark) !important; font-weight: 600 !important; font-size: 0.9rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #74151a 0%, #a01d24 50%, #74151a 100%) !important;
    color: #fff !important;
    border: 1px solid rgba(197,165,49,0.5) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.5rem !important;
    font-family: 'Cinzel', serif !important;
    font-size: 1rem !important; font-weight: 700 !important;
    letter-spacing: 1px !important; width: 100% !important;
    height: 3.2em !important; transition: all 0.3s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #9b1c23 0%, #c02030 100%) !important;
    border-color: var(--gold) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(116,21,26,0.6) !important;
}

.result-box {
    background: var(--card-bg);
    border: 1px solid rgba(197,165,49,0.5);
    border-radius: 16px; padding: 2rem; margin-top: 1.5rem;
    position: relative; overflow: hidden;
}
.result-box::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
.result-header {
    text-align: center; margin-bottom: 1.5rem; padding-bottom: 1.2rem;
    border-bottom: 1px solid rgba(197,165,49,0.2);
}
.crystal-ball { font-size: 2.5rem; display: block; }
.result-title-text {
    font-family: 'Cinzel', serif; font-size: 1.4rem; font-weight: 700;
    color: var(--gold); letter-spacing: 2px; margin-top: 0.4rem;
}

.houses-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;
}
.house-card {
    border-radius: 14px; padding: 1.2rem; border: 1px solid; transition: transform 0.3s;
}
.house-card:hover { transform: translateY(-4px); }
.house-gryffindor {
    background: linear-gradient(135deg, rgba(116,0,1,0.4), rgba(211,166,37,0.15));
    border-color: rgba(211,166,37,0.4);
}
.house-ravenclaw {
    background: linear-gradient(135deg, rgba(14,26,64,0.6), rgba(148,107,45,0.2));
    border-color: rgba(148,107,45,0.4);
}
.house-slytherin {
    background: linear-gradient(135deg, rgba(26,71,42,0.5), rgba(170,170,170,0.1));
    border-color: rgba(100,180,120,0.3);
}
.house-hufflepuff {
    background: linear-gradient(135deg, rgba(55,46,41,0.5), rgba(240,199,94,0.2));
    border-color: rgba(240,199,94,0.4);
}
.house-name-g { color: #d3a625; font-family:'Cinzel',serif; font-weight:700; font-size:1rem; }
.house-name-r { color: #a8b4d8; font-family:'Cinzel',serif; font-weight:700; font-size:1rem; }
.house-name-s { color: #7fbf8a; font-family:'Cinzel',serif; font-weight:700; font-size:1rem; }
.house-name-h { color: #f0c75e; font-family:'Cinzel',serif; font-weight:700; font-size:1rem; }
.house-sub  { font-size:0.75rem; font-style:italic; opacity:0.7; margin:0.15rem 0 0.5rem; }
.house-desc { font-size:0.82rem; color:var(--text-secondary); line-height:1.5; margin-bottom:0.6rem; }
.house-badge {
    display:inline-block; font-size:0.72rem; font-weight:600;
    padding:0.2rem 0.65rem; border-radius:20px; letter-spacing:0.5px;
}
.badge-g { background:rgba(211,166,37,0.2);  color:#d3a625; border:1px solid rgba(211,166,37,0.3); }
.badge-r { background:rgba(168,180,216,0.15); color:#a8b4d8; border:1px solid rgba(148,107,45,0.3); }
.badge-s { background:rgba(100,180,120,0.15); color:#7fbf8a; border:1px solid rgba(100,180,120,0.3); }
.badge-h { background:rgba(240,199,94,0.2);   color:#f0c75e; border:1px solid rgba(240,199,94,0.3); }

.api-ok {
    display:inline-flex; align-items:center; gap:0.5rem;
    background:rgba(26,71,42,0.3); border:1px solid rgba(46,160,67,0.3);
    border-radius:8px; padding:0.5rem 0.9rem;
    font-size:0.82rem; color:#57ab6e; margin-bottom:1rem;
}
.api-dot { width:8px; height:8px; background:#4CAF50; border-radius:50%; flex-shrink:0; }

.gold-divider { border:none; border-top:1px solid rgba(197,165,49,0.2); margin:2rem 0 1.5rem; }

.site-footer {
    text-align:center; padding:1.5rem 0 0.5rem;
    color:var(--text-secondary); font-size:0.82rem;
    opacity:0.65; border-top:1px solid rgba(197,165,49,0.12); margin-top:2rem;
}

section[data-testid="stSidebar"] {
    background: rgba(10,14,28,0.97) !important;
    border-right: 1px solid rgba(197,165,49,0.2) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 860px !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# 3. 사이드바 — 모델 정보만 표시
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 모델 설정")
    st.markdown(
        "<small style='color:#a89880;'>**모델:** gpt-4o-mini<br>**온도:** 0.85<br>**최대 토큰:** 1,200</small>",
        unsafe_allow_html=True,
    )

# ── session_state로 API Key 유지 ──
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.session_state.api_key


# ──────────────────────────────────────────────────────────
# 4. 헤더
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="sorting-header">
    <span class="hat-icon">🪄</span>
    <p class="main-title">AI 마법 분류 모자</p>
    <p class="sub-title">KAIST IMMS : AI-Driven Business Evolution</p>
    <p class="desc-text">당신의 키워드를 분석하여 최적의 <span>커리어 기숙사</span>를 배정합니다.</p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# 5. 메인 로직
# ──────────────────────────────────────────────────────────
if not api_key:
    # ── 중앙 API Key 입력 카드 ──
    st.markdown('<div class="magic-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">🔑 마법의 열쇠 입력</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:1.2rem;">'
        'OpenAI API Key를 입력하면 마법이 시작됩니다!</p>',
        unsafe_allow_html=True,
    )

    input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
    with input_col2:
        key_input = st.text_input(
            "",
            type="password",
            placeholder="OpenAI API Key를 입력하세요 (sk-...)",
            label_visibility="collapsed",
        )
        btn_activate = st.button("🪄 마법 활성화", use_container_width=True)
        st.markdown(
            "<p style='text-align:center;font-size:0.78rem;color:#a89880;opacity:0.7;margin-top:0.5rem;'>"
            "🛡️ API Key는 이 세션에서만 사용되며 서버에 저장되지 않습니다.</p>",
            unsafe_allow_html=True,
        )

    if btn_activate:
        if not key_input:
            st.error("⚠️ API Key를 입력해주세요.")
        elif not key_input.startswith("sk-"):
            st.error("❌ 올바른 API Key 형식이 아닙니다. (sk-... 로 시작해야 합니다)")
        else:
            st.session_state.api_key = key_input
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

else:
    client = OpenAI(api_key=api_key)

    # ── API 상태 표시 + 변경 버튼 ──
    truncated = f"{api_key[:7]}...{api_key[-4:]}"
    col_status, col_btn = st.columns([4, 1])
    with col_status:
        st.markdown(
            f'<div class="api-ok"><span class="api-dot"></span>'
            f'API Key 활성화됨 &nbsp;({truncated})</div>',
            unsafe_allow_html=True,
        )
    with col_btn:
        if st.button("🔄 변경", use_container_width=True):
            st.session_state.api_key = ""
            st.rerun()

    # ── 입력 폼 카드 ──
    st.markdown('<div class="magic-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">🎩 당신의 이야기를 들려주세요</p>', unsafe_allow_html=True)

    with st.form("sorting_form"):
        col1, col2 = st.columns(2)
        with col1:
            career = st.text_input(
                "💼 경력",
                value="9년차 마케팅 기획자",
                placeholder="예: 9년차 마케팅 기획자",
            )
            personality = st.text_input(
                "⭐ 나를 표현하는 키워드",
                value="패스트 러너, 엄청난 열정, 적용력",
                placeholder="예: 패스트 러너, 열정, 적응력",
            )
        with col2:
            strength = st.text_area(
                "⚡ 강점 및 스킬",
                value="PPT 시각화, 아이디어 기획, 파이썬 기초",
                placeholder="예: PPT 시각화, 아이디어 기획, 파이썬 기초",
                height=100,
            )
            goal = st.text_input(
                "🎯 이번 수업의 목표",
                value="AI를 비즈니스에 실제 적용하기",
                placeholder="예: AI를 비즈니스에 실제 적용하기",
            )

        submitted = st.form_submit_button("🪄 분류 모자 쓰기")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if not all([career, personality, strength, goal]):
            st.error("⚠️ 모든 항목을 입력해주세요.")
        else:
            sorting_hat_prompt = f"""너는 호그와트의 '분류 모자'이면서 동시에 냉철한 비즈니스 전략가야.
아래 사용자의 정보를 바탕으로 4개 기숙사 중 하나를 배정해줘.

[기숙사별 정의]
1. 그리핀도르 (The Bold Builder): 'Building is the method'를 실천하는 용감한 실행가. 기술이 서툴러도 일단 부딪히는 패스트 러너.
2. 래번클로 (The Strategic Analyst): 논리적이고 분석적이며, AI의 원리를 비즈니스 전략(Means-Ends Analysis)으로 풀어내는 지혜로운 자.
3. 슬리데린 (The Business Closer): 기술을 도구로 삼아 압도적인 수익과 ROI를 만들어내는 야심찬 성과주의자.
4. 후플푸프 (The Agile Supporter): 팀의 결속을 돕고, 유저의 피드백을 성실히 반영하여 제품을 다듬는 헌신적인 협업자.

[사용자 정보]
- 경력: {career}
- 강점: {strength}
- 성격/태도: {personality}
- 목표: {goal}

[출력 양식 - 아래 형식을 정확히 따를 것]
## 🏰 [배정된 기숙사 이름] — [영문 별칭]

[호그와트 분류 모자 특유의 위엄 있고 극적인 선언 문구, 2~3줄]

---

### 📜 배정 이유
[사용자의 실제 키워드를 직접 언급하며 배정 이유를 칭찬하는 방식으로 3~4문장 설명]

---

### 🪄 AI 마법 지팡이 (추천 AI 툴)
[이 사람의 역할과 목표에 맞는 AI 툴 3가지를 구체적인 활용 방법과 함께 추천. 각 툴마다 한 줄씩]

---

### ⚡ 팀원을 향한 자기소개 문구
> "[강렬하고 임팩트 있는 자기소개 한 문장. 경력과 목표를 녹여낼 것]"
"""

            with st.spinner("흐음... 아주 흥미롭군... 당신의 커리어 DNA를 분석하는 중..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "system", "content": sorting_hat_prompt}],
                        temperature=0.85,
                        max_tokens=1200,
                    )
                    result = response.choices[0].message.content

                    st.balloons()

                    st.markdown("""
                    <div class="result-box">
                        <div class="result-header">
                            <span class="crystal-ball">🔮</span>
                            <p class="result-title-text">분류 모자의 판결</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(result)

                except Exception as e:
                    err = str(e)
                    if "401" in err or "Unauthorized" in err or "Incorrect API key" in err:
                        st.error("❌ API Key가 올바르지 않습니다. 유효한 OpenAI API Key를 확인해주세요.")
                    elif "429" in err or "Rate limit" in err or "quota" in err:
                        st.error("⏱️ API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
                    elif "500" in err or "503" in err:
                        st.error("🔧 OpenAI 서버에 일시적인 문제가 발생했습니다. 잠시 후 다시 시도해주세요.")
                    else:
                        st.error(f"⚠️ 오류가 발생했습니다: {e}")


# ──────────────────────────────────────────────────────────
# 6. 기숙사 안내 섹션
# ──────────────────────────────────────────────────────────
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown('<p style="font-family:\'Cinzel\',serif;font-size:1.3rem;font-weight:700;color:#f5c518;text-align:center;letter-spacing:2px;margin-bottom:1rem;">⚡ 4개의 기숙사</p>', unsafe_allow_html=True)

st.markdown("""
<div class="houses-grid">
    <div class="house-card house-gryffindor">
        <div style="font-size:2rem;margin-bottom:0.4rem;">🦁</div>
        <p class="house-name-g">그리핀도르</p>
        <p class="house-sub" style="color:#d3a625;">The Bold Builder</p>
        <p class="house-desc">기술이 서툴러도 일단 부딪히는 패스트 러너. 'Building is the method'를 실천하는 용감한 실행가.</p>
        <span class="house-badge badge-g">용기 · 실행력 · 도전</span>
    </div>
    <div class="house-card house-ravenclaw">
        <div style="font-size:2rem;margin-bottom:0.4rem;">🦅</div>
        <p class="house-name-r">래번클로</p>
        <p class="house-sub" style="color:#8090c0;">The Strategic Analyst</p>
        <p class="house-desc">AI의 원리를 비즈니스 전략으로 풀어내는 논리적이고 분석적인 지혜로운 자.</p>
        <span class="house-badge badge-r">지혜 · 전략 · 분석</span>
    </div>
    <div class="house-card house-slytherin">
        <div style="font-size:2rem;margin-bottom:0.4rem;">🐍</div>
        <p class="house-name-s">슬리데린</p>
        <p class="house-sub" style="color:#6aad7a;">The Business Closer</p>
        <p class="house-desc">기술을 도구로 삼아 압도적인 수익과 ROI를 만들어내는 야심찬 성과주의자.</p>
        <span class="house-badge badge-s">야망 · 성과 · ROI</span>
    </div>
    <div class="house-card house-hufflepuff">
        <div style="font-size:2rem;margin-bottom:0.4rem;">🦡</div>
        <p class="house-name-h">후플푸프</p>
        <p class="house-sub" style="color:#c8a040;">The Agile Supporter</p>
        <p class="house-desc">팀의 결속을 돕고 유저 피드백을 성실히 반영하여 제품을 다듬는 헌신적인 협업자.</p>
        <span class="house-badge badge-h">헌신 · 협업 · 성실</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# 7. 푸터
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
    ✨ Generated by your AI-Driven Business Evolution Partner<br>
    <span style="font-size:0.75rem;letter-spacing:1px;">KAIST IMMS · AI Sorting Hat · 2026</span>
</div>
""", unsafe_allow_html=True)
