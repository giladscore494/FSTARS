import streamlit as st
import pandas as pd
import os

# נתיב לקובץ הנתונים
DATA_PATH = os.path.join(os.path.dirname(__file__), "players_data-2024_2025.csv")

# טוען נתונים עם בדיקה לקובץ
@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error(f"שגיאה: הקובץ '{DATA_PATH}' לא נמצא. ודא שהוא נמצא לצד app.py")
        st.stop()
    return pd.read_csv(DATA_PATH)

# דירוג ליגות (דוגמה; תוכל לעדכן לפי איכות)
LEAGUE_SCORES = {
    'Premier League': 1.0, 'La Liga': 0.95, 'Serie A': 0.9,
    'Bundesliga': 0.9, 'Ligue 1': 0.85, 'Eredivisie': 0.8,
    'Liga Portugal': 0.75, 'Championship': 0.7, 'MLS': 0.6,
    'Brazil Serie A': 0.8, 'Argentina Primera': 0.78,
}

# מחשב את מדד YSP-75
def calculate_score(row):
    try:
        age = float(row['Age'])
        minutes = float(row['Minutes'])
        goals = float(row['Goals'])
        assists = float(row['Assists'])
        league = row['League']
    except:
        return 0

    # ניקוד גיל – צעירים מקבלים יותר
    age_score = max(0, 30 - age) * 2

    # ניקוד סטטיסטיקה
    stats_score = (goals * 4 + assists * 3 + minutes / 300)

    # ניקוד ליגה
    league_weight = LEAGUE_SCORES.get(league, 0.5)
    total_score = (age_score + stats_score) * league_weight

    return round(total_score, 2)

# ממשק משתמש
st.title("🎯 YSP-75 – מדד סיכויי הצלחה לשחקן צעיר")

name_input = st.text_input("🔍 הזן שם שחקן (באנגלית):")

if name_input:
    df = load_players()

    if 'Player' not in df.columns:
        st.error("❌ הקובץ לא מכיל את העמודה 'Player'.")
        st.stop()

    results = df[df["Player"].str.lower().str.contains(name_input.lower())]

    if results.empty:
        st.warning("שחקן לא נמצא.")
    else:
        player = results.iloc[0]
        score = calculate_score(player)

        st.subheader(f"📊 תוצאה לשחקן {player['Player']}")
        st.metric("מדד YSP-75", f"{score}")

        if score > 75:
            st.success("🏆 טופ עולמי – שווה מעקב צמוד")
        elif score > 65:
            st.info("🌟 כישרון עם פוטנציאל ברור")
        elif score > 55:
            st.warning("🧪 כישרון – אך צריך יציבות")
        else:
            st.error("🔎 נתונים נמוכים – לא רלוונטי כרגע")

        st.markdown("**פרטי שחקן:**")
        st.write(player)
