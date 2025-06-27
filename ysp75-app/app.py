import os
import pandas as pd
import streamlit as st

# מיקום הקובץ בתוך התיקייה ysp75-app
DATA_PATH = os.path.join("ysp75-app", "players_data-2024_2025.csv")

# טען את הקובץ אם קיים
@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error(f"שגיאה: הקובץ '{DATA_PATH}' לא נמצא. ודא שהוא קיים בתיקייה ysp75-app.")
        st.stop()
    return pd.read_csv(DATA_PATH)

# דירוג הליגות - ככל שהמספר נמוך יותר, הליגה נחשבת איכותית יותר
LEAGUE_SCORES = {
    'Premier League': 1,
    'La Liga': 2,
    'Bundesliga': 3,
    'Serie A': 4,
    'Ligue 1': 5,
    'Eredivisie': 6,
    'Liga Portugal': 7,
    'Belgian Pro League': 8,
    'Championship': 9,
    'Turkish Super Lig': 10,
    'Other': 15  # ברירת מחדל
}

# חישוב מדד YSP-75
def compute_ysp75(player_row):
    age = player_row['age']
    minutes = player_row['minutes']
    goals = player_row['goals']
    assists = player_row['assists']
    league = player_row['league_name']

    # ניקוד לפי ליגה
    league_score = LEAGUE_SCORES.get(league, LEAGUE_SCORES['Other'])
    league_factor = max(1, 16 - league_score)  # ככל שהליגה גבוהה יותר (מספר נמוך), הפקטור גבוה יותר

    # משקלולים
    age_score = max(0, (23 - age)) * 1.5
    minutes_score = min(minutes / 2000, 1.5) * 10
    performance_score = (goals + 0.75 * assists) * 3

    ysp_score = age_score + minutes_score + performance_score + league_factor
    return round(ysp_score, 2)

# טען את הדאטה
df = load_players()

# ממשק
st.title("🎯 YSP-75 – מדד סיכויי הצלחה לשחקן צעיר")
name_input = st.text_input("הזן שם שחקן (באנגלית):")

if name_input:
    filtered = df[df['short_name'].str.lower().str.contains(name_input.lower())]
    if filtered.empty:
        st.warning("שחקן לא נמצא.")
    else:
        player = filtered.iloc[0]
        score = compute_ysp75(player)

        st.markdown(f"### ✨ {player['short_name']} – ציון YSP-75: **{score}**")
        st.markdown(f"""
        - גיל: {player['age']}
        - קבוצה: {player['club_name']}
        - ליגה: {player['league_name']}
        - דקות: {player['minutes']}
        - גולים: {player['goals']}
        - בישולים: {player['assists']}
        """)

        # הערכת כישרון לפי ציון
        if score > 75:
            st.success("🏆 טופ עולמי – שחקן שכדאי לעקוב אחריו ברצינות.")
        elif score > 65:
            st.info("🔎 כישרון עם פוטנציאל ברור – דורש מעקב המשכי.")
        elif score > 55:
            st.warning("⚠️ כישרון – אך יש צורך ביציבות או שדרוג ליגה.")
        else:
            st.error("❌ סיכויי הצלחה נמוכים לפי מדד YSP-75.")
