import string
import random
import urllib.request
import streamlit as st

st.set_page_config(page_title="데바데 랜덤 제약 시드 생성기", page_icon="⚙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #202124; color: #FFFFFF; }
    h1, h2, h3 { color: #8AB4F8 !important; font-family: 'CookieRun', Arial !important; }
    .stButton>button { background-color: #8AB4F8 !important; color: #202124 !important; font-weight: bold !important; width: 100%; border-radius: 8px; font-family: 'CookieRun', Arial !important; }
    div[data-baseweb="select"] { background-color: #292a2d !important; }
    p, span, label { font-family: 'CookieRun', Arial !important; }
    </style>
""", unsafe_allow_html=True)

score_values = ['0', '100', '200', '300', '400']
# 🎯 무작위 항목을 등급의 최상단 0순위로 탑재 완료!
grade_options = ['무작위', 'S', 'A', 'B', 'C', 'D', 'X']
CATEGORIES = [
    '무작위', '오라버프통합', '버프', '오라', '스텔스', '방해', '생존', 
    '탈진', '아이템', '오라/버프', '어그로', '자힐', '호재', 
    '터널링 방지', '터널링 대응', '발전기', '타힐', '기도', '안티 캠핑', '토템'
]
VIRTUAL_CAT_MAP = {'오라버프통합': ['오라', '버프', '오라/버프']}
DEFAULT_GRADES = ['S', 'A', 'B', 'B']
GRADE_VALUES = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'X': 0}

# 🎯 [수정 포인트] 작성자님의 진짜 Gist Raw 주소를 이 따옴표 사이에 꼭 유지해주세요!
GITHUB_RAW_URL = "https://githubusercontent.com"

@st.cache_data
def load_web_matrix():
    data_map = {'S': {}, 'A': {}, 'B': {}, 'C': {}, 'D': {}, 'X': {}}
    try:
        req = urllib.request.Request(GITHUB_RAW_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            raw_html = response.read().decode('utf-8-sig')
        for line in raw_html.strip().split('\n'):
            if line.strip():
                score_str, grade, cat = line.split('\t')
                if grade in data_map: data_map[grade].setdefault(cat, []).append(int(score_str))
        return data_map
    except: return None

PERK_DETAIL_DATA = load_web_matrix()
if not PERK_DETAIL_DATA:
    st.error("⚠️ 데이터 동기화 대기 중... Gist 주소를 매핑해주세요.")
    st.stop()

ENCODE_MAP = {
    '무작위':'N', 'S':'Q', 'A':'W', 'B':'E', 'C':'R', 'D':'T', 'X':'Y',
    '무작위카테고리':'Z', '오라버프통합':'U', '버프':'I', '오라':'O', '스텔스':'P', '방해':'A', '생존':'S',
    '탈진':'D', '아이템':'F', '오라/버프':'G', '어그로':'H', '자힐':'J', '호재':'K',
    '터널링 방지':'L', '터널링 대응':'C', '발전기':'V', '타힐':'B', '기도':'N', '안티 캠핑':'M', '토템':'X'
}

st.title(" 데바데 랜덤 조건 설정기 (웹 버전)")
st.caption("발급된 암호 코드를 스트리머의 채널 채팅창에 공유해 내기를 시작하세요!")

st.header("⚙️ 1. 글로벌 규칙 및 점수 범위 설정")
col1, col2 = st.columns(2)
with col1: combo_min = st.selectbox("최저 점수 제한", score_values, index=2)
with col2: combo_max = st.selectbox("최고 점수 제한", score_values, index=4)

col3, col4 = st.columns(2)
with col3: cat_dup = st.checkbox("대분류 중복 허용", value=True)
with col4: surv_dup = st.checkbox("생존자 중복 허용", value=True)

st.header("🃏 2. 4개 퍽 슬롯 조건 세부 빌딩")
slots_data = []

for i in range(4):
    st.write(f"---")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        # 🎯 [개선점1] '등급 제한' 문구를 '등급 고정'으로 직관성 200% 상용 등급 패치!
        g_val = st.selectbox(f"등급 고정 ({i+1}번 퍽)", grade_options, index=grade_options.index(DEFAULT_GRADES[i]), key=f"g_{i}")
    
    with sc2:
        # 🎯 [개선점2] 유저가 등급 고정을 '무작위'로 선택하면 대분류를 강제 마비시키고 꿀잼 안내 멘트 발포!
        if g_val == '무작위':
            c1_val = st.selectbox(f"대분류 지정 1 ({i+1}번)", ["무작위 등급은 대분류를 지정 할 수 없습니다"], index=0, disabled=True, key=f"c1_{i}")
        else:
            avail_cats = ['무작위', '오라버프통합'] + sorted(list(PERK_DETAIL_DATA[g_val].keys()))
            c1_val = st.selectbox(f"대분류 지정 1 ({i+1}번)", avail_cats, index=0, key=f"c1_{i}")
            
    with sc3:
        if g_val == '무작위':
            c2_val = '무작위'
            st.markdown("<p style='color:#E74C3C; font-size:12px; margin-top:35px; font-weight:bold;'>🚫 대분류 지정 불가</p>", unsafe_allow_html=True)
        else:
            if c1_val != '무작위' and c1_val != "무작위 등급은 대분류를 지정 할 수 없습니다":
                c2_val = st.selectbox(f"대분류 지정 2 ({i+1}번)", avail_cats, index=0, key=f"c2_{i}")
            else:
                c2_val = '무작위'
                st.markdown("<p style='color:#9AA0A6; font-size:13px; margin-top:35px;'>지정 안 함</p>", unsafe_allow_html=True)
                
    slots_data.append({'g': g_val, 'c1': c1_val if c1_val != "무작위 등급은 대분류를 지정 할 수 없습니다" else '무작위', 'c2': c2_val})

st.header("🪙 3. 실시간 최종 판돈 및 시드 발행")

# 웹 실시간 판돈 가감산 연산 (무작위 슬롯당 무조건 +1 코인 고정 가산 처리 연동)
total_cost = 0
has_x_grade = False
total_cost += ((400 - int(combo_max)) // 100) + ((200 - int(combo_min)) // 100)

for i in range(4):
    if slots_data[i]['g'] == '무작위':
        # 🎯 [개선점2] 거리를 따지지 않고 무작위 등급 슬롯당 무조건 깔끔하게 +1 코인 고정 산출!
        total_cost += 1
    else:
        diff = GRADE_VALUES[DEFAULT_GRADES[i]] - GRADE_VALUES[slots_data[i]['g']]
        if diff > 0: total_cost += diff
        if slots_data[i]['g'] == 'X': has_x_grade = True; total_cost += 20
        if slots_data[i]['c1'] != '무작위': total_cost += 1
        if slots_data[i]['c2'] != '무작위': total_cost += 1

final_coin = max(2, 2 + total_cost)
st.metric(label="📊 요구 베팅 판돈", value=f"{final_coin} Coin")
if has_x_grade: st.warning("⚠️ X등급 포함 시 패배 정산은 1.5배가 아닌 1배(본전)로 적용됩니다.")

if st.button("🚀 압축 시드 코드 생성"):
    min_tot, max_tot = 0, 0
    valid_flag = True
    for i in range(4):
        g = slots_data[i]['g']
        if g == '무작위':
            # 무작위 등급인 경우 S~D 조건의 극한 범위를 미리 적립해 디펜더 통과 조율
            min_tot += 0; max_tot += 100; continue
        c1 = slots_data[i]['c1']
        c2 = slots_data[i]['c2']
        cats = list(PERK_DETAIL_DATA[g].keys()) if c1 == '무작위' else (VIRTUAL_CAT_MAP[c1] if c1 in VIRTUAL_CAT_MAP else [c1])
        if c1 != '무작위' and c2 != '무작위': cats.extend(VIRTUAL_CAT_MAP[c2] if c2 in VIRTUAL_CAT_MAP else [c2])
        v_scores = []
        for c in set(cats):
            if c in PERK_DETAIL_DATA[g]: v_scores.extend(PERK_DETAIL_DATA[g][c])
        if not v_scores: valid_flag = False; break
        v_scores.sort()
        min_tot += v_scores; max_tot += v_scores[-1]
        
    if not valid_flag or max_tot < int(combo_min) or min_tot > int(combo_max):
        st.error(f"⚠️ 선택하신 조합의 점수한계는 [{min_tot}~{max_tot}]점 입니다. 범위 제한과 절대 겹칠 수 없습니다!")
    else:
        min_head = combo_min
        max_head = combo_max
        c_dup_bit = "1" if cat_dup else "0"
        s_dup_bit = "1" if surv_dup else "0"
        
        slot_pieces = []
        for i in range(4):
            g_c = ENCODE_MAP.get(slots_data[i]['g'], 'N')
            c1_c = ENCODE_MAP.get(slots_data[i]['c1'] if slots_data[i]['c1'] != '무작위' else '무작위카테고리', 'Z')
            c2_c = ENCODE_MAP.get(slots_data[i]['c2'] if slots_data[i]['c2'] != '무작위' else '무작위카테고리', 'Z')
            slot_pieces.append(f"{g_c}{c1_c}{c2_c}")
            
        real_seed = f"{min_head[0]}{max_head[0]}{c_dup_bit}{s_dup_bit}{''.join(slot_pieces)}"
        st.success(f"🎯 암호화 시드 코드가 정상 발급되었습니다!")
        st.code(real_seed, language="text")
        st.info("💡 위 회색 박스 안의 코드를 복사해서 스트리머에게 전송하세요!")
