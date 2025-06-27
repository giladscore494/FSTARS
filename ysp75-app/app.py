import streamlit as st
import pandas as pd
import os

DATA_PATH = "players_data-2024_2025.csv"

@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error(f"שגיאה: הקובץ '{DATA_PATH}' לא נמצא. ודא שהוא קיים בתיקייה.")
        st.stop()
    return pd.read_csv(DATA_PATH)

# דירוג הליגות - לצורך ניקוד איכות ליגה
LEAGUE_SCORES = {
    'Premier League': 1.0, 'La Liga': 0.95, 'Serie A': 0.9,
    'Bundesliga': 0.9, 'Ligue 1': 0.85, 'Eredivisie': 0.75,
    'Primeira Liga': 0.7, 'Championship': 0.6, 'MLS': 0.5
}

def ysp75_score(row):
    try:
        age = float(row["Age"])
        goals = float(row["Gls"])
        assists = float(row["Ast"])
        minutes = float(row["Min"])
        league = row["Comp"]
    except:
        return 0

    if minutes == 0 or age == 0:
        return 0

    gpa = (goals + assists) / (minutes / 90)  # תרומה למשחק
    age_factor = 1 + (22 - age) * 0.05 if age < 22 else 1  # תגמול לצעירים
    league_weight = LEAGUE_SCORES.get(league, 0.4)  # ברירת מחדל לליגות לא מוכרות

    score = gpa * age_factor * league_weight * 25
    return round(score, 2)

# טען דאטה
df = load_players()

# ממשק משתמש
st.title("🎯 YSP-75 – מדד סיכויי הצלחה לשחקן צעיר")

name_input = st.text_input("הזן שם שחקן (באנגלית):")

if name_input:
    filtered = df[df["Player"].str.lower().str.contains(name_input.lower())]

    if filtered.empty:
        st.warning("שחקן לא נמצא.")
    else:
        for _, row in filtered.iterrows():
            st.subheader(row["Player"])
            st.write(f"✳️ קבוצה: {row['Squad']} | ליגה: {row['Comp']} | גיל: {row['Age']}")
            score = ysp75_score(row)
            st.metric("YSP-75 Score", score)
