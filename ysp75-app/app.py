import streamlit as st
import pandas as pd
import os

DATA_PATH = "players_data-2024_2025.csv"

@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error(f"שגיאה: הקובץ '{DATA_PATH}' לא נמצא. ודא שהוא קיים בתיקייה ysp75-app.")
        st.stop()
    try:
        df = pd.read_csv(DATA_PATH)
        if df.empty:
            st.error("שגיאה: הקובץ ריק או לא נטען כראוי.")
            st.stop()
        return df
    except Exception as e:
        st.error(f"שגיאה בטעינת קובץ: {e}")
        st.stop()

def calculate_ysp_score(row):
    try:
        age = row['Age']
        minutes = row['Min']
        goals = row['Gls']
        assists = row['Ast']
    except KeyError:
        st.error("שגיאה: העמודות הדרושות לא קיימות בקובץ.")
        st.stop()

    # ניקוד בסיסי לפי ביצועים
    score = 0
    if pd.notna(goals):
        score += goals * 3
    if pd.notna(assists):
        score += assists * 2
    if pd.notna(minutes) and minutes > 0:
        score += (minutes / 90) * 0.5
    if pd.notna(age) and age < 23:
        score += (23 - age) * 1.5

    return round(score, 2)

# טען דאטה
df = load_players()

# ממשק
st.title("🎯 YSP-75 – מדד סיכויי הצלחה לשחקן צעיר")
name_input = st.text_input("הזן שם שחקן (באנגלית):")

if name_input:
    if 'Player' not in df.columns:
        st.error("שגיאה: עמודת 'Player' לא קיימת בקובץ.")
        st.stop()

    filtered = df[df['Player'].str.lower().str.contains(name_input.lower())]
    if filtered.empty:
        st.warning("שחקן לא נמצא.")
    else:
        for _, row in filtered.iterrows():
            score = calculate_ysp_score(row)
            st.subheader(f"{row['Player']} – ציון YSP: {score}")
