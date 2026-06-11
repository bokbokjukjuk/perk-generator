import string
import random
import urllib.request
import streamlit as st  # 웹 전용 특수 빌더 라이브러리 탑재

# ==========================================
# 🎨 1. 웹 화면 글로벌 다크 테마 및 레이아웃 설정
# ==========================================
st.set_page_config(page_title="데바데 랜덤 제약 시드 생성기", page_icon="⚙️", layout="centered")

# 방송용 세련된 다크모드 스타일 강제 주입
st.markdown("""
    <style>
    .stApp { background-color: #202124; color: #FFFFFF; }
    h1, h2, h3 { color: #8AB4F8 !important; }
    .stButton>button { background-color: #8AB4F8 !important; color: #202124 !important; font-weight: bold !important; width: 100%; border-radius: 8px; }
    div[data-baseweb="select"] { background-color: #292a2d !important; }
    </style>
""", unsafe_allow_html=True)

score_values = ['0', '100', '200', '300', '400']
grade_options = ['S', 'A', 'B', 'C', 'D', 'X']
CATEGORIES = [
    '무작위', '오라버프통합', '버프', '오라', '스텔스', '방해', '생존',
    '탈진', '아이템', '오라/버프', '어그로', '자힐', '호재',
    '터널링 방지', '터널링 대응', '발전기', '타힐', '기도', '안티 캠핑', '토템'
]
VIRTUAL_CAT_MAP = {'오라버프통합': ['오라', '버프', '오라/버프']}
DEFAULT_GRADES = ['S', 'A', 'B', 'B']
GRADE_VALUES = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'X': 0}

# ==========================================
# 🌐 2. 작성자님의 깃허브 지스트 실시간 웹 데이터 수혈
# ==========================================
# 🎯 [수정 포인트] 예전에 만드신 진짜 Gist Raw 주소를 여기에 그대로 박아두시면 됩니다!
GITHUB_RAW_URL = "https://githubusercontent.com"


@st.cache_data  # 웹 서버 렉 방지를 위한 초고속 데이터 캐싱 주머니 가동
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
    except:
        return None


PERK_DETAIL_DATA = load_web_matrix()
if not PERK_DETAIL_DATA:
    st.error("⚠️ 깃허브 데이터 로딩 실패! 네트워크 상태를 확인해주세요.")
    st.stop()

# ==========================================
# 🔑 3. 100% 싱크로율 구조화 암호화 인코더 물리 엔진
# ==========================================
ENCODE_MAP = {
    'S': 'Q', 'A': 'W', 'B': 'E', 'C': 'R', 'D': 'T', 'X': 'Y',
    '무작위': 'Z', '오라버프통합': 'U', '버프': 'I', '오라': 'O', '스텔스': 'P', '방해': 'A', '생존': 'S',
    '탈진': 'D', '아이템': 'F', '오라/버프': 'G', '어그로': 'H', '자힐': 'J', '호재': 'K',
    '터널링 방지': 'L', '터널링 대응': 'C', '발전기': 'V', '타힐': 'B', '기도': 'N', '안티 캠핑': 'M', '토템': 'X'
}

# ==========================================
# 🏛️ 4. 모던 웹 인터페이스 화면 그리드 드로잉
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
    st.subheader(f"📍 {i + 1}번 퍽 슬롯")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        g_val = st.selectbox(f"등급 제한 ({i + 1}번)", grade_options, index=grade_options.index(DEFAULT_GRADES[i]),
                             key=f"g_{i}")

    # 🧬 [작성자님 기획 완벽 반영] 등급별 진짜 존재하는 카테고리만 실시간 필터 동기화!
    avail_cats = ['무작위', '오라버프통합'] + sorted(list(PERK_DETAIL_DATA[g_val].keys()))

    with sc2:
        c1_val = st.selectbox(f"대분류 지정 1 ({i + 1}번)", avail_cats, index=0, key=f"c1_{i}")
    with sc3:
        # 대분류 1이 무작위가 아닐 때만 대분류 2 선택 창 활성화 (자동 온오프 스케줄러 장착)
        if c1_val != '무작위':
            c2_val = st.selectbox(f"대분류 지정 2 ({i + 1}번)", avail_cats, index=0, key=f"c2_{i}")
        else:
            c2_val = '무작위'
            st.markdown("<p style='color:#9AA0A6; font-size:13px; margin-top:33px;'>지정 안 함</p>", unsafe_allow_html=True)

    slots_data.append({'g': g_val, 'c1': c1_val, 'c2': c2_val})

# (3) 실시간 판돈 및 시드 발행 엔진 연산
st.header("🪙 3. 실시간 최종 판돈 및 시드 발행")

# 코인 코스트 실시간 계산 수식 전개
total_cost = 0
has_x_grade = False
total_cost += ((400 - int(combo_max)) // 100) + ((200 - int(combo_min)) // 100)

for i in range(4):
    diff = GRADE_VALUES[DEFAULT_GRADES[i]] - GRADE_VALUES[slots_data[i]['g']]
    if diff > 0: total_cost += diff
    if slots_data[i]['g'] == 'X': has_x_grade = True; total_cost += 20
    if slots_data[i]['c1'] != '무작위': total_cost += 1
    if slots_data[i]['c2'] != '무작위': total_cost += 1

final_coin = max(2, 2 + total_cost)

# 화면 실시간 판돈 연출
st.metric(label="📊 요구 베팅 판돈", value=f"{final_coin} Coin")
if has_x_grade:
    st.warning("⚠️ X등급 포함 시 패배 정산은 1.5배가 아닌 1배(본전)로 적용됩니다.")

# 🚀 압축 시드 코드 생성기 최종 가동
if st.button("🚀 압축 시드 코드 생성"):
    # 수학적 범위 모순 검증 디펜더 가동
    min_tot, max_tot = 0, 0
    valid_flag = True
    for i in range(4):
        g = slots_data[i]['g']
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
        min_tot += v_scores[0];
        max_tot += v_scores[-1]

    if not valid_flag or max_tot < int(combo_min) or min_tot > int(combo_max):
        st.error(f"⚠️ 선택하신 조합의 점수한계는 [{min_tot}~{max_tot}]점 입니다. 설정 범위 제한과 절대 겹칠 수 없는 모순 조건입니다!")
    else:
        # 진짜 16자리 패킷 압축 구이 실행
        min_head = combo_min[0] if len(combo_min) > 0 else "2"
        max_head = combo_max[0] if len(combo_max) > 0 else "4"
        c_dup_bit = "1" if cat_dup else "0"
        s_dup_bit = "1" if surv_dup else "0"

        slot_pieces = []
        for i in range(4):
            g_c = ENCODE_MAP.get(slots_data[i]['g'], 'E')
            c1_c = ENCODE_MAP.get(slots_data[i]['c1'], 'Z')
            c2_c = ENCODE_MAP.get(slots_data[i]['c2'], 'Z')
            slot_pieces.append(f"{g_c}{c1_c}{c2_c}")

        real_seed = f"{min_head}{max_head}{c_dup_bit}{s_dup_bit}{''.join(slot_pieces)}"

        # 🧾 생성된 시드를 웹 전용 큼직한 텍스트 박스로 안전하게 제공
        st.success(f"🎯 암호화 시드 코드가 정상 발급되었습니다!")
        st.code(real_seed, language="text")
        st.info("💡 위 회색 박스 안의 코드를 복사(오른쪽 복사 아이콘 딸깍)해서 스트리머에게 전송하세요!")
