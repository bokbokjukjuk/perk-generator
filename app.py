import string
import random
import urllib.request
import streamlit as st # 웹 전용 특수 빌더 라이브러리 탑재

# ==========================================
# 🎨 1. 웹 화면 글로벌 다크 테마 및 레이아웃 설정
# ==========================================
st.set_page_config(page_title="데바데 랜덤 제약 시드 생성기", page_icon="⚙️", layout="centered")

# 방송 브랜딩과 100% 일치하는 크롬 다크모드 스타일 강제 주입
st.markdown("""
    <style>
    .stApp { background-color: #202124; color: #FFFFFF; }
    h1, h2, h3 { color: #8AB4F8 !important; font-family: 'Arial', sans-serif; }
    .stButton>button { background-color: #1E5631 !important; color: #FFFFFF !important; font-weight: bold !important; width: 100%; border-radius: 8px; border: none; height: 40px; }
    .gen-btn>div>.stButton>button { background-color: #8AB4F8 !important; color: #202124 !important; font-size: 16px !important; height: 45px; }
    div[data-baseweb="select"] { background-color: #292a2d !important; }
    div[data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 28px !important; font-weight: bold !important; }
    .penalty-box { background-color: #292a2d; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #323639; }
    </style>
""", unsafe_allow_html=True)

score_values = ['0', '100', '200', '300', '400']
grade_options = ['무작위', 'S', 'A', 'B', 'C', 'D', 'X']
CATEGORIES = [
    '무작위', '오라버프통합', '버프', '오라', '스텔스', '방해', '생존',
    '탈진', '아이템', '오라/버프', '어그로', '자힐', '호재',
    '터널링 방지', '터널링 대응', '발전기', '타힐', '기도', '안티 캠핑', '토템'
]
VIRTUAL_CAT_MAP = {'오라버프통합': ['오라', '버프', '오라/버프']}
DEFAULT_GRADES = ['S', 'A', 'B', 'B']
GRADE_VALUES = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'X': 0}

BASE_CHARS = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*"
G_ENC = {'무작위':'Z', 'S':'Q', 'A':'W', 'B':'E', 'C':'R', 'D':'T', 'X':'Y'}

# ==========================================
# 🌐 2. [간소화 영구 정착] 깃허브 지스트 실시간 메모장 웹 수혈 파서 엔진
# ==========================================
# 🎯 [작성자님 필독] 이 칸에 지난번 성공하셨던 '진짜 내 Gist Raw 인터넷 주소'를 복사해서 넣어주세요!
GITHUB_RAW_URL = "https://githubusercontent.com"

@st.cache_data # 웹 서버 트래픽 렉 폭발 방지를 위한 고성능 데이터 캐싱 가동
def load_web_matrix():
    data_map = {'S': {}, 'A': {}, 'B': {}, 'C': {}, 'D': {}, 'X': {}}
    try:
        req = urllib.request.Request(GITHUB_RAW_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            raw_html = response.read().decode('utf-8-sig')
        for line in raw_html.strip().split('\n'):
            if line.strip():
                score_str, grade, cat = line.split('\t')
                data_map[grade].setdefault(cat, []).append(int(score_str))
        return data_map
    except: return None

PERK_DETAIL_DATA = load_web_matrix()
if not PERK_DETAIL_DATA:
    st.error("⚠️ 깃허브 데이터 로딩 실패! GITHUB_RAW_URL 주소를 다시 점검해 주세요.")
    st.stop()
# ==========================================
# 🏛️ 4. 모던 웹 인터페이스 화면 그리드 드로잉 (2부 시작)
# ==========================================
st.title(" 데바데 랜덤 제약 미션 설정기 (웹 버전)")
st.caption("작성하신 시드 코드를 복사하여 스트리머의 채팅창에 붙여넣어 주세요!!")

# (1) 글로벌 세팅 존
st.header("⚙️ 1. 글로벌 규칙 및 점수 범위 설정")
col1, col2 = st.columns(2)
with col1:
    combo_min = st.selectbox("최저 점수 제한", score_values, index=2)  # 기본 200
with col2:
    combo_max = st.selectbox("최고 점수 제한", score_values, index=4)  # 기본 400

col3, col4 = st.columns(2)
with col3:
    cat_dup = st.checkbox("대분류 중복 허용", value=True)
with col4:
    surv_dup = st.checkbox("생존자 중복 허용", value=True)

# (2) 4개 슬롯 제약 설정 존
st.header("🃏 2. 4개 퍽 슬롯 조건 세부 빌딩")
slots_data = []

for i in range(4):
    # 🎯 [개선점1 반영] 등급 제한 ➡️ 등급 고정 명칭 전면 교정 완료!
    st.subheader(f"📍 {i + 1}번 퍽 슬롯 조건 설정")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        g_val = st.selectbox(f"퍽 등급 고정 ({i + 1}번)", grade_options, index=grade_options.index(DEFAULT_GRADES[i]),
                             key=f"g_{i}")

    # 🎯 [개선점2 반영] 등급 고정이 "무작위"인 경우 대분류 상자 완전 파괴 및 노란색 안내문구 띄우기
    if g_val == '무작위':
        with sc2:
            st.markdown(
                "<p style='color:#FFD700; font-size:14px; font-weight:bold; margin-top:33px;'>💡 무작위 등급은 대분류 지정 불가</p>",
                unsafe_allow_html=True)
        with sc3:
            st.markdown("<p style='color:#202124; font-size:14px; margin-top:33px;'>-</p>", unsafe_allow_html=True)
        slots_data.append({'g': '무작위', 'c1': '무작위', 'c2': '무작위'})
    else:
        avail_cats = ['무작위', '오라버프통합'] + sorted(list(PERK_DETAIL_DATA[g_val].keys()))
        with sc2:
            c1_val = st.selectbox(f"대분류 지정 1 ({i + 1}번)", avail_cats, index=0, key=f"c1_{i}")
        with sc3:
            if c1_val != '무작위':
                c2_val = st.selectbox(f"대분류 지정 2 ({i + 1}번)", avail_cats, index=0, key=f"c2_{i}")
            else:
                c2_val = '무작위'
                st.markdown("<p style='color:#9AA0A6; font-size:13px; margin-top:33px;'>지정 안 함</p>",
                            unsafe_allow_html=True)
        slots_data.append({'g': g_val, 'c1': c1_val, 'c2': c2_val})

# (3) 실시간 판돈 및 시드 발행 엔진 연산
st.header("🪙 3. 실시간 최종 판돈 및 시드 발행")

# 코인 코스트 실시간 가감산 수식 전개
total_cost = 0
has_x_grade = False
total_cost += ((400 - int(combo_max)) // 100) + ((200 - int(combo_min)) // 100)

for i in range(4):
    g_type = slots_data[i]['g']
    if g_type == '무작위':
        total_cost += 1
    else:
        diff = GRADE_VALUES[DEFAULT_GRADES[i]] - GRADE_VALUES[g_type]
        if diff > 0: total_cost += diff
        if g_type == 'X': has_x_grade = True; total_cost += 20

    if g_type != '무작위' and slots_data[i]['c1'] != '무작위': total_cost += 1
    if g_type != '무작위' and slots_data[i]['c2'] != '무작위': total_cost += 1

final_coin = max(2, 2 + total_cost)
penalty_coin = final_coin if has_x_grade else int(final_coin * 1.5)

# 🎯 [개선점4 반영] 대통합본과 완벽 대칭되는 수직 적층형 레이아웃 렌더링 장착!
# 15px 수준의 간격을 주기 위해 Streamlit 고유 컬럼 구조를 세로 레이아웃 타일로 시각화
st.metric(label="📊 요구 베팅 코인", value=f"{final_coin} Coin")

st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)  # 15px 정밀 숨쉴공간 마진 확보

if has_x_grade:
    # 🎯 X등급이 하나라도 켜지면 실패 문구를 날려버리고 경고 전광판으로 실시간 웹 전환!
    st.markdown(f"""
        <div class='penalty-box'>
            <p style='color:#E74C3C; font-size:13px; margin:0;'>⚠️ 알림</p>
            <p style='color:#E74C3C; font-size:20px; font-weight:bold; margin:5px 0 0 0;'>X등급 선택시 추가 배당코인은 없습니다</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # 🎯 X등급이 없으면 기획안 텍스트 그대로 깔끔하게 1.5배수 실시간 노출 사수!
    st.markdown(f"""
        <div class='penalty-box'>
            <p style='color:#9AA0A6; font-size:13px; margin:0;'>2연속 패배시 페이백되는 코인</p>
            <p style='color:#FF9800; font-size:24px; font-weight:bold; margin:5px 0 0 0;'>{penalty_coin} Coin</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# 🎯 시드 복사 미스 방지를 위해 초기화 버튼(새로고침)과 시드 생성 그리드를 우측 배치 유기적 유도
col_btn1, col_btn2 = st.columns([1, 2])
with col_btn1:
    # 웹 특성상 st.button 클릭 시 페이지가 새로고침되므로 자연스럽게 초기화 단추로 유동 작동!
    st.button("🔄 설정 초기화")
with col_btn2:
    st.markdown("<div class='gen-btn'>", unsafe_allow_html=True)
    generate_trigger = st.button("🚀 압축 시드 코드 생성")
    st.markdown("</div>", unsafe_allow_html=True)

# 🚀 11자 기호 직결 초압축 시드 코드 생성기 최종 가동
if generate_trigger:
    min_tot, max_tot = 0, 0
    valid_flag = True
    for i in range(4):
        g = slots_data[i]['g']
        if g == '무작위':
            v_scores = []
            for check_g in ['S', 'A', 'B', 'C', 'D']:
                for cat in PERK_DETAIL_DATA[check_g]: v_scores.extend(PERK_DETAIL_DATA[check_g][cat])
        else:
            c1 = slots_data[i]['c1']
            c2 = slots_data[i]['c2']
            cats = list(PERK_DETAIL_DATA[g].keys()) if c1 == '무작위' else (
                VIRTUAL_CAT_MAP[c1] if c1 in VIRTUAL_CAT_MAP else [c1])
            if c1 != '무작위' and c2 != '무작위': cats.extend(VIRTUAL_CAT_MAP[c2] if c2 in VIRTUAL_CAT_MAP else [c2])
            v_scores = []
            for c in set(cats):
                if c in PERK_DETAIL_DATA[g]: v_scores.extend(PERK_DETAIL_DATA[g][c])
        if not v_scores: valid_flag = False; break
        v_scores.sort()
        min_tot += v_scores;
        max_tot += v_scores[-1]

    if not valid_flag or max_tot < int(combo_min) or min_tot > int(combo_max):
        st.error(f"⚠️ 선택하신 조합의 점수한계는 [{min_tot}~{max_tot}]점 입니다. 설정 범위 제한과 절대 겹칠 수 없는 모순 조건입니다!")
    else:
        # 진짜 11자리 마스터 물리 직결 패킷 생성
        min_idx = str(score_values.index(combo_min))
        max_idx = str(score_values.index(combo_max))
        c_dup_bit = "1" if cat_dup else "0"
        s_dup_bit = "1" if surv_dup else "0"

        slot_pieces = []
        for i in range(4):
            g_c = G_ENC.get(slots_data[i]['g'], 'Z')
            c1_c = MAP_CHARS[CATEGORIES.index(slots_data[i]['c1'])]
            c2_c = MAP_CHARS[CATEGORIES.index(slots_data[i]['c2'])]
            slot_pieces.append(f"{g_c}{c1_c}{c2_c}")

        real_seed = f"{min_idx}{max_idx}{c_dup_bit}{s_dup_bit}{''.join(slot_pieces)}"

        st.success(f"🎯 11자리 다이어트 초압축 시드 발급 성공!")
        st.code(real_seed, language="text")
        st.info("💡 위 회색 박스 안의 코드를 복사(오른쪽 복사 단추 딸깍)해서 스트리머에게 전송하세요!")


