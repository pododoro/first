import streamlit as st
import random
import requests

import requests

# GitHub RAW URL
GITHUB_RAW_URL = "https://raw.githubusercontent.com/pododoro/first/main/quest3.txt"

# 파일 다운로드 및 내용 확인
response = requests.get(GITHUB_RAW_URL)

if response.status_code == 200:
    print("✅ 파일을 정상적으로 불러왔습니다!")
    content = response.content.decode("utf-8", errors="ignore")  # UTF-8로 디코딩하며, 오류 발생 시 무시
    
    # 🔹 파일 내용 미리보기 (앞부분 20줄 출력)
    lines = content.split("\n")
    print("\n📄 파일 내용 미리보기 (앞부분 20줄)\n")
    for i, line in enumerate(lines[:20]):
        print(f"{i+1}: {line}")
    
else:
    print(f"❌ 파일을 불러오지 못했습니다! HTTP 상태 코드: {response.status_code}")

def load_questions(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ 파일을 불러오지 못했습니다. HTTP 상태 코드: {response.status_code}")
        return []
    
    lines = response.text.split("\n")

    # 🔹 파일 내용이 비어 있는 경우 처리
    if not lines or len(lines) < 5:
        print("❌ 파일 내용이 너무 짧거나 비어 있습니다. GitHub 파일을 확인하세요.")
        return []

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
            try:
                question = line.split(")")[1].strip()  # 번호 제거 후 문제 저장
            except IndexError:
                print(f"❌ 잘못된 형식 발견: {line}")
                continue
        elif line.startswith("정답:"):
            answer = line.replace("정답:", "").strip()
        elif line.startswith("해설:"):
            explanation = line.replace("해설:", "").strip()
        elif "(" in line and ")" in line:  # 성경구절 정보
            reference = line.strip()
    
    # 마지막 문제 추가
    if question and answer and explanation:
        questions.append({"문제": question, "정답": answer, "해설": explanation, "성경구절": reference})

    if not questions:
        print("❌ 문제 데이터가 없습니다! 파일 형식을 확인하세요.")

    return questions


# 📌 올바른 GitHub RAW URL 입력
GITHUB_RAW_URL = "https://raw.githubusercontent.com/pododoro/first/main/quest.txt"

# 📌 GitHub에서 데이터 불러오기
def load_questions(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            st.error(f"❌ 파일 불러오기 실패. HTTP 상태 코드: {response.status_code}")
            return []

        lines = response.text.split("\n")
        questions = []
        current_data = {"문제": None, "정답": None, "해설": None, "성경구절": None}

        for line in lines:
            line = line.strip()
            if not line or line.startswith("📖"):
                continue

            # 문제 라인 처리 (강화된 검증 로직)
            if line[0].isdigit() and ')' in line:
                parts = line.split(')', 1)  # 최대 1번만 분할
                if len(parts) >= 2:
                    if current_data["문제"]:  # 이전 문제 저장
                        questions.append(current_data)
                        current_data = {"문제": None, "정답": None, "해설": None, "성경구절": None}
                    current_data["문제"] = parts[1].strip()
                else:
                    st.warning(f"⚠️ 잘못된 문제 형식: {line}")
            
            # 나머지 필드 처리
            elif line.startswith("정답:"):
                current_data["정답"] = line.replace("정답:", "").strip()
            elif line.startswith("해설:"):
                current_data["해설"] = line.replace("해설:", "").strip()
            elif '(' in line and ')' in line:
                current_data["성경구절"] = line.strip()

        # 마지막 문제 추가
        if current_data["문제"]:
            questions.append(current_data)

        return questions

    except Exception as e:
        st.error(f"❌ 치명적 오류: {str(e)}")
        return []

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
