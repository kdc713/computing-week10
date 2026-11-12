import pandas as pd
import streamlit as st


st.set_page_config(page_title="일주일 공부 기록", page_icon="📚")
st.title("일주일 공부 기록")
st.caption("예시 데이터 · 2026년 11월 2~8일")

records = [
    ("2026-11-02", "강의 복습", 35),
    ("2026-11-02", "과제", 45),
    ("2026-11-03", "코딩 실습", 60),
    ("2026-11-04", "강의 복습", 25),
    ("2026-11-04", "과제", 75),
    ("2026-11-05", "코딩 실습", 50),
    ("2026-11-05", "강의 복습", 30),
    ("2026-11-06", "과제", 55),
    ("2026-11-07", "코딩 실습", 90),
    ("2026-11-07", "과제", 40),
    ("2026-11-08", "강의 복습", 45),
    ("2026-11-08", "코딩 실습", 35),
]
study_log = pd.DataFrame(records, columns=["날짜", "학습 유형", "공부 시간(분)"])
study_log["날짜"] = pd.to_datetime(study_log["날짜"])

study_type = st.selectbox("학습 유형", ["전체", "강의 복습", "코딩 실습", "과제"])
selected = study_log
if study_type != "전체":
    selected = study_log[study_log["학습 유형"] == study_type]

total_time, session_count, average_time = st.columns(3)
minutes = selected["공부 시간(분)"]
total_time.metric("총 공부 시간", f"{minutes.sum():,}분")
session_count.metric("학습 횟수", f"{len(selected)}회")
average_time.metric("1회 평균", f"{minutes.mean():.1f}분")

st.header("날짜별 공부 시간")
dates = pd.date_range(study_log["날짜"].min(), study_log["날짜"].max())
daily = selected.groupby("날짜")["공부 시간(분)"].sum().reindex(dates, fill_value=0)
daily.index = daily.index.strftime("%m-%d")
daily.index.name = "날짜"
st.bar_chart(daily.reset_index(), x="날짜", y="공부 시간(분)")

st.header("학습 내역")
st.dataframe(
    selected,
    hide_index=True,
    column_config={"날짜": st.column_config.DateColumn(format="YYYY-MM-DD")},
)
