import streamlit as st
import pandas as pd
import os

# נתיב לקובץ הנתונים
DATA_PATH = os.path.join(os.path.dirname(__file__), 'players_data-2024_2025.csv')

# קריאת קובץ הנתונים עם בדיקת שגיאה
@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error(f"שגיאה: הקובץ '{DATA_PATH}' לא נמצא. ודא שהוא נמצא בתיקייה לצד app.py.")
        st.stop()
    return pd.read_csv(DATA_PATH)

# דירוג ליגות עולמי – ככל שהציון גבוה יותר, הליגה חזקה יותר
LEAGUE_SCORES = {
    'Premier League': 1.0,
    'La Liga': 0.95,
    'Serie A': 0.9,
    'Bundesliga': 0.9,
    'Ligue 1': 0.85,
    'Eredivisie': 0.8,
    'Liga Portugal': 0.78,
    'Belgian Pro League': 0.75,
    'Brazilian Serie A': 0.73,
    'Argentine Primera': 0.7,
    'MLS': 0.65,
    'Israeli Premier League': 0.5,
}

# חישוב מדד YSP-75 לשחקן
def compute_ysp75(row):
    try:
        age = float(row["Age"])
        goals = float(row["Goals"])
        assists = float(row["Assists"])
        minutes = float(row["Minutes"])
        league = row["League"]
    except:
        return 0  # במקרה של ערך חסר

    league_score = LEAGUE_SCORES.get(league, 0.6)  # ניקוד ליגה
    performance = (goals * 4 + assists * 3 + minutes / 90) / max(age, 1)
    ysp_score = league_score * performance
    return round(ysp_score, 2)

# טען את הדאטה
df = load_players()

# ממשק
st.title("🎯 YSP-75 – מדד סיכויי הצלחה לשחקן צעיר")

name_input = st.text_input("הזן שם שחקן (באנגלית):")

if name_input:
    filtered = df[df['Player'].fillna('').str.lower().str.strip().str.contains(name_input.lower().strip())]

    if filtered.empty:
        st.warning("שחקן לא נמצא.")
    else:
        for idx, row in filtered.iterrows():
            score = compute_ysp75(row)
            st.subheader(f"{row['Player']} – ציון YSP-75: {score}")

            if score < 55:
                st.info("⚪ פוטנציאל לא גבוה או לא יציב.")
            elif score < 65:
                st.warning("🟡 כישרון שדורש יציבות נוספת.")
            elif score < 75:
                st.success("🟢 כישרון עם פוטנציאל ברור! שווה מעקב.")
            else:
                st.balloons()
                st.success("💎 טופ עולמי – מועמד בולט ביותר להצלחה!")

            st.write(f"ליגה: {row['League']} | גיל: {row['Age']} | דקות: {row['Minutes']} | גולים: {row['Goals']} | בישולים: {row['Assists']}")
