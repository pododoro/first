import streamlit as st
import random
import requests

# 📌 GitHub RAW URL 설정
GITHUB_RAW_URL = https://raw.githubusercontent.com/pododoro/first/main/%F0%9F%93%96%202025%EB%85%84%202%EC%B2%AD%EB%85%84%EB%B6%80%20%EB%8F%99%EA%B3%84%EC%88%98%EB%A0%A8%ED%9A%8C%20%EC%84%B1%EA%B2%BD%ED%80%B4%EC%A6%88%EB%8C%80%ED%9A%8C%20%EC%98%88%EC%83%81%EB%AC%B8%EC%A0%9C%20106.txt

# 📌 GitHub에서 데이터 불러오기
def load_questions(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []  # 파일을 불러오지 못하면 빈 리스트 반환
    lines = response.text.split("\n")

    questions = []
    question = None
    answer = None
    explanation = None
    reference = None

    for line in lines:
        line = line.strip()
        if line.startswith("📖") or not line:  # 제목 또는 빈 줄 무시
            continue
        if line[0].isdigit():  # 문제 번호로 시작하는 줄
            if question:  # 이전 문제 저장
                questions.append({"문제": question, "정답": answer, "해설": explanation, "성경구절": reference})
            question = line.split(")")[1].strip()  # 번호 제거 후 문제 저장
        elif line.startswith("정답:"):
            answer = line.replace("정답:", "").strip()
        elif line.startswith("해설:"):
            explanation = line.replace("해설:", "").strip()
        elif "(" in line and ")" in line:  # 성경구절 정보
            reference = line.strip()
    
    # 마지막 문제 추가
    if question and answer and explanation:
        questions.append({"문제": question, "정답": answer, "해설": explanation, "성경구절": reference})

    return questions

# 🚀 GitHub에서 퀴즈 데이터 불러오기
questions_data = load_questions(GITHUB_RAW_URL)

# 데이터 로드 오류 방지
if not questions_data:
    st.error("❌ 퀴즈 데이터를 불러오지 못했습니다. GitHub 파일을 확인하세요.")
    st.stop()

# 🎯 Streamlit 웹 앱 설정
st.title("📖 성경 퀴즈 마스터")
st.write("랜덤 성경 퀴즈를 풀어보세요!")

# 📝 문제 랜덤 출제
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions_data)

question = st.session_state.current_question

# 📌 문제 표시
st.subheader("문제")
st.write(f"📖 {question['성경구절']}")
st.write(question["문제"])

# 📝 정답 입력 받기
user_answer = st.text_input("정답을 입력하세요:")

# ✅ 정답 확인
if st.button("제출"):
    if user_answer.strip() == question["정답"]:
        st.success("🎉 정답입니다!")
    else:
        st.error(f"❌ 오답입니다! 정답: {question['정답']}")
    st.write(f"📖 해설: {question['해설']}")

    # 🔄 새로운 문제 랜덤 출제
    st.session_state.current_question = random.choice(questions_data)
    st.button("다음 문제 풀기 🔄", on_click=lambda: st.rerun())
