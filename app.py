import string
import random
import urllib.request
import streamlit as st # 웹 전용 특수 빌더 라이브러리 탑재

# ==========================================
# 🎨 1. 웹 화면 글로벌 다크 테마 및 레이아웃 설정
# ==========================================
st.set_page_config(page_title="데바데 랜덤 제약 시드 생성기", page_icon="⚙️", layout="centered")

# 🎯 [수직 리모델링 전용 특수 CSS 주입] 요구베팅과 패배코인을 2층으로 웅장하게 쌓아 올리는 웹 빌더 마감
st.markdown("""
    <style>
    .stApp { background-color: #202124; color: #FFFFFF; }
    h1, h2, h3 { color: #8AB4F8 !important; font-family: 'Arial', sans-serif; }
    
    /* 요구 베팅 코인 타일 상자 스타일 */
    .coin-box { background-color: #292a2d; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #323639; width: 100%; height: 95px; }
    .coin-box-title { color: #9AA0A6; font-size: 13px; margin: 0; }
    .coin-box-val { color: #FFD700; font-size: 26px; font-weight: bold; margin: 3px 0 0 0; }
    
    /* 2연속 패배시 페이백되는 코인 타일 상자 스타일 */
    .penalty-box { background-color: #292a2d; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #323639; width: 100%; height: 95px; }
    .penalty-box-title { color: #9AA0A6; font-size: 13px; margin: 0; }
    .penalty-box-val { color: #FF9800; font-size: 26px; font-weight: bold; margin: 3px 0 0 0; }
    .penalty-box-warn { color: #E74C3C; font-size: 15px; font-weight: bold; margin: 15px 0 0 0; }
    
    /* 🔄 설정 초기화 및 버튼 칼정렬 수직 매커니즘 */
    .stButton>button { background-color: #1E5631 !important; color: #FFFFFF !important; font-weight: bold !important; width: 100%; border-radius: 6px; border: none; height: 35px; }
    .gen-btn>div>.stButton>button { background-color: #8AB4F8 !important; color: #202124 !important; font-size: 15px !important; height: 45px; border-radius: 6px; }
    div[data-baseweb="select"] { background-color: #292a2d !important; }
    </style>
""", unsafe_allow_html=True)

score_values = ['0', '100', '200', '300', '400']
grade_options = ['무작위', 'S', 'A', 'B', 'C', 'D', 'X']

# 🎯 대본진 프로그램과 1의 오차도 허용하지 않는 카테고리 순서 철통 사수 선언
CATEGORIES = [
    '무작위', '오라버프통합', '버프', '오라', '스텔스', '방해', '생존', 
    '탈진', '아이템', '오라/버프', '어그로', '자힐', '호재', 
    '터널링 방지', '터널링 대응', '발전기', '타힐', '기도', '안티 캠핑', '토템'
]
VIRTUAL_CAT_MAP = {'오라버프통합': ['오라', '버프', '오라/버프']}
DEFAULT_GRADES = ['S', 'A', 'B', 'B']
GRADE_VALUES = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1, 'X': 0}

# 🎯 작성자님의 진짜 16자리 패킷 규격과 100% 일치하는 기호 매핑 주머니
MAP_CHARS = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*"
G_ENC = {'무작위':'Z', 'S':'Q', 'A':'W', 'B':'E', 'C':'R', 'D':'T', 'X':'Y'}

# ==========================================
# 🌐 2. [실시간 연동] 깃허브 지스트 마스터 데이터 수혈 엔진
# ==========================================
# 🎯 [작성자님 필독] 이 칸에 예전에 성공하셨던 '진짜 내 Gist Raw 인터넷 주소'를 복사해서 넣어두시면 됩니다!
GITHUB_RAW_URL = "https://gist.githubusercontent.com/bokbokjukjuk/2eed3f39d4b81c33bf557f0bc4dbf25d/raw/cb5851058a2d72e3cdc56a8c11c365fd2de42b44/perk_matrix_txt"

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
st.caption("작성하신 시드 코드를 복사하여 스트리머의 채팅창에 붙여넣기(Ctrl+V) 해주세요!!")

# (1) 글로벌 세팅 존
st.header("⚙️ 1. 글로벌 규칙 및 점수 범위 설정")
col1, col2 = st.columns(2)
with col1:
    combo_min = st.selectbox("최저 점수 제한", score_values, index=2) # 기본 200
with col2:
    combo_max = st.selectbox("최고 점수 제한", score_values, index=4) # 기본 400

col3, col4 = st.columns(2)
with col3:
    cat_dup = st.checkbox("대분류 중복 허용", value=True)
with col4:
    surv_dup = st.checkbox("생존자 중복 허용", value=True)

# (2) 4개 슬롯 제약 설정 존
st.header("🃏 2. 4개 퍽 슬롯 조건 세부 빌딩")
slots_data = []

for i in range(4):
    st.subheader(f"📍 {i+1}번 퍽 슬롯 조건 설정")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        g_val = st.selectbox(f"퍽 등급 고정 ({i+1}번)", grade_options, index=grade_options.index(DEFAULT_GRADES[i]), key=f"g_{i}")
    
    # [무작위 등급 지정 시 대분류 삭제 후 노란색 가이드라인 전환 처리]
    if g_val == '무작위':
        with sc2:
            st.markdown("<p style='color:#FFD700; font-size:14px; font-weight:bold; margin-top:33px;'>💡 무작위 등급은 대분류 지정 불가</p>", unsafe_allow_html=True)
        with sc3:
            st.markdown("<p style='color:#202124; font-size:14px; margin-top:33px;'>-</p>", unsafe_allow_html=True)
        slots_data.append({'g': '무작위', 'c1': '무작위', 'c2': '무작위'})
    else:
        avail_cats = ['무작위', '오라버프통합'] + sorted(list(PERK_DETAIL_DATA[g_val].keys()))
        with sc2:
            c1_val = st.selectbox(f"대분류 지정 1 ({i+1}번)", avail_cats, index=0, key=f"c1_{i}")
        with sc3:
            if c1_val != '무작위':
                c2_val = st.selectbox(f"대분류 지정 2 ({i+1}번)", avail_cats, index=0, key=f"c2_{i}")
            else:
                c2_val = '무작위'
                st.markdown("<p style='color:#9AA0A6; font-size:13px; margin-top:33px;'>지정 안 함</p>", unsafe_allow_html=True)
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

# ----------------------------------------------------
# 🏗️ [좌우 분할 스페이스 매커니즘 개통 - 공간 균형 비율 패치]
# ----------------------------------------------------
# 화면 하단을 왼쪽(판돈 수직 적층 상자 윙)과 오른쪽(대형 조작 버튼 윙)으로 반반 나눕니다.
col_left_wing, col_right_wing = st.columns([1, 2])

with col_left_wing:
    # 🎯 1층: 요구 베팅 코인 상자 드로잉 (높이 95px 강제 세팅 완비)
    st.markdown(f"""
        <div class='coin-box'>
            <p class='coin-box-title'>요구 베팅 코인</p>
            <p class='coin-box-val'>{final_coin} Coin</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 🎯 [개선점 완벽 반영] 상자 사이 정확히 15픽셀의 숨 쉴 간격 마진 뚫어주기!
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # 🎯 2층: 2연속 패배시 배당 코인 상자 드로잉 (높이 95px 가변 렌더링 세팅 완비)
    if has_x_grade:
        # X등급이 하나라도 포착되면 숫자를 날려버리고 수직 상자 안을 붉은색 경고 전광판으로 실시간 변환!
        st.markdown("""
            <div class='penalty-box' style='display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                <p class='penalty-box-title' style='color:#E74C3C;'>⚠️ 알림</p>
                <p style='color:#E74C3C; font-size:12px; font-weight:bold; margin:5px 0 0 0; line-height:1.2; text-align:center;'>X등급 선택시 추가<br>배당코인은 없습니다</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # X등급이 없는 평화로운 상태일 땐 기획안 문구 그대로 1.5배수 곱연산 수치 깔끔 노출!
        st.markdown(f"""
            <div class='penalty-box'>
                <p class='penalty-box-title'>2연속 패배시 페이백되는 코인</p>
                <p class='penalty-box-val'>{penalty_coin} Coin</p>
            </div>
        """, unsafe_allow_html=True)

with col_right_wing:
    # 🎯 1단 축선: 압축 시드 코드 생성 단추
    st.markdown("<div class='gen-btn'>", unsafe_allow_html=True)
    generate_trigger = st.button("🚀 압축 시드 코드 생성")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 🎯 2단 축선: 생성된 시드 코드 박스 및 가이드 메시지 (y=115 공간)
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
                cats = list(PERK_DETAIL_DATA[g].keys()) if c1 == '무작위' else (VIRTUAL_CAT_MAP[c1] if c1 in VIRTUAL_CAT_MAP else [c1])
                if c1 != '무작위' and c2 != '무작위': cats.extend(VIRTUAL_CAT_MAP[c2] if c2 in VIRTUAL_CAT_MAP else [c2])
                v_scores = []
                for c in set(cats):
                    if c in PERK_DETAIL_DATA[g]: v_scores.extend(PERK_DETAIL_DATA[g][c])
            if not v_scores: valid_flag = False; break
            v_scores.sort()
            min_tot += v_scores[0]; max_tot += v_scores[-1]
            
        if not valid_flag or max_tot < int(combo_min) or min_tot > int(combo_max):
            st.error(f"⚠️ 선택하신 조합의 점수한계는 [{min_tot}~{max_tot}]점 입니다. 설정 범위 제한과 절대 겹칠 수 없는 모순 조건입니다!")
        else:
            # 🎯 [작성자님 16자리 마스터 패킷 직결 매핑 변환식]
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
                
            # 오차 마진 단 1픽셀도 없는 완전체 16자리 시드 코드 수식 배출!
            real_seed = f"{min_idx}{max_idx}{c_dup_bit}{s_dup_bit}{''.join(slot_pieces)}"
            
            st.success(f"🎯 16자리 마스터 초압축 시드 발급 성공!")
            st.code(real_seed, language="text")
            st.info("💡 위 회색 박스 안의 코드를 복사(우측 복사 아이콘 딸깍)해서 스트리머의 채팅창에 붙여넣기(Ctrl+V) 해주세요!")
    else:
        # 시드를 생성하기 전 유저 대기실 가이드 빈 상자 렌더링 유지
        st.markdown("<div style='height: 50px; background-color: #202124;'></div>", unsafe_allow_html=True)

    # 🎯 [클릭 미스 가로폭 수직 칼정렬 차단] 복사단추 하단 축선(y=245) 위치에 설정 초기화 대형 버튼 정렬 배치!
    st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True) # 넉넉한 클릭미스 방지 안전 마진 확보
    st.button("🔄 설정 초기화")

