# 실습#5 : 실습#2 공학용 계산기를 streamlit 버전으로 개발
# 사용한 기능 : 전역변수 (st.session_state)
# 실행 : streamlit run app.py
import math
import streamlit as st

st.title("🧮 공학용 계산기")

# ---------------------------------------------------------------
# 전역변수 : streamlit 은 버튼을 누를 때마다 코드 전체가 다시 실행된다.
# 그래서 일반 변수는 매번 초기화되므로, 입력 중인 수식을 st.session_state 에 저장한다.
# ---------------------------------------------------------------
if "display" not in st.session_state:
    st.session_state.display = "0"     # 결과창에 보이는 수식
    st.session_state.ans = 0           # 직전 계산 결과


# ---------------- 버튼 동작 함수 (과제2 calc.py 와 같은 이름) ----------------
def append_text(text):
    if text in ["sin", "cos", "tan", "log", "√"]:   # 함수 버튼은 '(' 자동으로 붙이기
        text = text + "("
    elif text == "x²":
        text = "^(2)"

    if st.session_state.display in ["0", "Error"]:
        st.session_state.display = text
    else:
        st.session_state.display += text


def clear_display():
    st.session_state.display = "0"


def delete_last():
    text = st.session_state.display
    if len(text) > 1 and text != "Error":
        st.session_state.display = text[:-1]
    else:
        st.session_state.display = "0"


def calculate_result():
    expr = st.session_state.display
    try:
        # 화면 기호 → 파이썬 수식
        expr = expr.replace("π", "pi").replace("√", "sqrt").replace("^", "**").replace("%", "/100")
        names = {
            "sin": lambda x: math.sin(math.radians(x)),   # 각도(degree) 기준
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "sqrt": math.sqrt,
            "log": math.log10,
            "pi": math.pi,
            "e": math.e,
            "ans": st.session_state.ans,
        }
        res = eval(expr, {"__builtins__": {}}, names)
        if isinstance(res, float):
            res = round(res, 8)
            if res.is_integer():
                res = int(res)
        st.session_state.ans = res
        st.session_state.display = str(res)
    except Exception:
        st.session_state.display = "Error"


# ---------------- 화면 ----------------
# 1행 : 결과창 + del + C
c1, c2, c3 = st.columns([5, 1, 1])
c1.text_input("결과", value=st.session_state.display, disabled=True, label_visibility="collapsed")
c2.button("del", on_click=delete_last, use_container_width=True)
c3.button("C", on_click=clear_display, use_container_width=True)

# 2~5행 : SimpleCalc.ui 와 같은 배치
keypad = [
    ["sin", "cos", "tan", "7", "8", "9", "*"],
    ["√",   "x²",  "π",   "4", "5", "6", "/"],
    ["(",   ")",   "e",   "1", "2", "3", "+"],
    ["log", "ans", "%",   "0", ".", "=", "-"],
]
for row in keypad:
    cols = st.columns(7)
    for i, key in enumerate(row):
        if key == "=":
            cols[i].button("=", on_click=calculate_result, type="primary", use_container_width=True)
        else:
            cols[i].button(key, on_click=append_text, args=(key,), use_container_width=True)

st.caption(f"ans = {st.session_state.ans}")
