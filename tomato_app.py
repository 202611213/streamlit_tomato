#🍅 Tomato Fruit-Set Predictor:app.py
import streamlit as st
import pandas as pd
import joblib
import os

# 1. 페이지 설정 (브라우저 탭 제목, 아이콘, 레이아웃)
st.set_page_config(
    page_title="토마토 착과율 예측 시스템",
    page_icon="🍅",
    layout="centered"
)

# 2. 고급 커스텀 스타일링 CSS 추가 (오류 수정 완료)
st.markdown("""
    <style>
    /* 전체 메인 배경 및 폰트 부드럽게 조정 */
    .main {
        background-color: #f7f9f6;
    }
    
    /* 타이틀 영역 데코레이션 */
    .title-text {
        font-family: 'Nanum Gothic', sans-serif;
        color: #2E7D32;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .subtitle-text {
        color: #666666;
        font-size: 14px;
        margin-bottom: 25px;
    }
    
    /* 입력 폼 섹션 카드화 */
    .input-container {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.08);
        border: 1px solid #e1ebd5;
        margin-bottom: 20px;
    }
    
    /* 커스텀 버튼 디자인 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(46, 125, 50, 0.2);
    }
    
    /* 예측 결과 표시 카드 */
    .result-card {
        background-color: #e8f5e9;
        border-left: 6px solid #2e7d32;
        padding: 20px;
        border-radius: 8px;
        margin-top: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .result-title {
        color: #2e7d32;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .result-value {
        color: #1b5e20;
        font-size: 28px;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 모델 파일 로드 (캐싱을 적용하여 페이지 성능 최적화)
@st.cache_resource
def load_model():
    model_path = "tomato_model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

rf_model = load_model()

# 4. 헤더 영역
st.markdown("<h2 class='title-text'>🍅 토마토 착과율 예측 시스템</h2>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>실시간 온실 환경 데이터(내부 온도, 지온)를 분석하여 예상 착과율을 정밀하게 모니터링합니다.</p>", unsafe_allow_html=True)

# 모델이 없을 경우 안전하게 경고 메시지 출력
if rf_model is None:
    st.error("⚠️ `tomato_model.pkl` 모델 파일을 찾을 수 없습니다. 파일이 스크립트와 동일한 경로에 있는지 확인해 주세요.")
else:
    # 5. 사용자 입력 UI 구성 (카드 형태 레이아웃 및 2단 분할)
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        temp = st.number_input(
            "🌡️ 온실 내부 온도 (°C)", 
            min_value=-10.0, 
            max_value=50.0, 
            value=22.0, 
            step=0.1,
            help="온실 내부의 공기 온도를 입력해 주세요."
        )
    with col2:
        soil_temp = st.number_input(
            "🌱 토양 지온 (°C)", 
            min_value=-10.0, 
            max_value=50.0, 
            value=18.0, 
            step=0.1,
            help="뿌리가 위치한 토양의 깊이별 평균 온도를 입력해 주세요."
        )
        
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. 예측 실행 및 세련된 결과 출력
    if st.button("📈 예측 결과 분석하기"):
        with st.spinner("환경 분석 및 착과율 도출 중..."):
            # 입력 데이터 전처리
            input_data = pd.DataFrame([[temp, soil_temp]], columns=['내부온도', '지온'])
            
            # 예측 수행
            predicted = rf_model.predict(input_data)
            result_pct = predicted[0]
            
            # 커스텀 HTML 카드로 결과 표현
            st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">🎯 분석 완료 - 예상 착과율</div>
                    <div class="result-value">{result_pct:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 착과율 상태에 따른 유용한 가이드 팁 추가 제공
            if result_pct >= 70:
                st.info("💡 **생육 상태 최적:** 현재 입력된 온도 조합은 토마토 수정 및 착과에 매우 이상적인 환경입니다.")
            elif result_pct >= 40:
                st.warning("⚠️ **생육 관리 주의:** 착과율이 보통 수준입니다. 주야간 온도 편차나 수분 관리를 점검해 보세요.")
            else:
                st.error("🚨 **생육 환경 개선 필요:** 온도 스트레스로 인해 착과율 저하가 우려됩니다. 환기 및 가온 장치를 조절해 주세요.")