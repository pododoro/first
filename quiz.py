import streamlit as st
import random
import pandas as pd

# 성경 퀴즈 데이터 로드
questions_data = [
    {"번호": 1, "문제": "당시에 온 땅의 언어와 말은 몇 개였나?", "성경구절": "창세기 11:1", "정답": "하나", "해설": "온 땅의 언어가 하나요 말이 하나였더라"},
    {"번호": 2, "문제": "사람들이 동방으로 옮겨 살기 시작한 평지는?", "성경구절": "창세기 11:2", "정답": "시날 평지", "해설": "그들이 동방으로 옮기다가 시날 평지를 만나 거기 거류하며"},
    {"번호": 3, "문제": "사람들이 시날 평지에 모여 건축을 위해 굽기 시작한 것은?", "성경구절": "창세기 11:3", "정답": "벽돌", "해설": "서로 말하되 자, 벽돌을 만들어 견고히 굽자 하고 벽돌로 돌을 대신하며"},
    {"번호": 4, "문제": "사람들이 벽돌을 어떤 방식으로 만들기 시작하였나?", "성경구절": "창세기 11:3", "정답": "불에 구워서", "해설": "서로 말하되 자, 벽돌을 만들어 견고히 굽자 하고 벽돌로 돌을 대신하며"},
    {"번호": 5, "문제": "사람들이 건축을 위해 돌을 대신한 것은 무엇인가?", "성경구절": "창세기 11:3", "정답": "벽돌", "해설": "벽돌로 돌을 대신하며"}
]

df = pd.DataFrame(questions_data)

# Streamlit 페이지 설정
st.title("📖 성경 퀴즈 마스터")
st.write("성경 퀴즈를 풀어보세요!")

# 문제 랜덤 출제
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions_data)

question = st.session_state.current_question

# 문제 표시
st.subheader(f"문제 {question['번호']}")
st.write(question["문제"])
st.write(f"📖 성경 구절: {question['성경구절']}")

# 정답 입력 받기
user_answer = st.text_input("정답을 입력하세요:")

# 정답 확인
if st.button("제출"):
    if user_answer.strip() == question["정답"]:
        st.success("🎉 정답입니다!")
    else:
        st.error("❌ 오답입니다!")
    st.write(f"✅ 정답: {question['정답']}")
    st.write(f"📖 해설: {question['해설']}")

    # 새로운 문제 랜덤 출제
    st.session_state.current_question = random.choice(questions_data)
    st.button("다음 문제 풀기 🔄", on_click=lambda: st.experimental_rerun())
