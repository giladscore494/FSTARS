import streamlit as st
import pandas as pd
import os

# הגדרה של הנתיב לקובץ (בתוך תיקיית האפליקציה)
DATA_PATH = os.path.join(os.path.dirname(__file__), "players_data-2024_2025.csv")

# דירוג ליגות - ככל שהמספר נמוך יותר, הליגה איכותית יותר
LEAGUE_RANKINGS = {
    "Premier League": 1, "La Liga": 2, "Bundesliga": 3, "Serie A": 4, "Ligue 1": 5,
    "Eredivisie": 6, "Primeira Liga": 7, "Brasileirão": 8, "Argentine Liga": 9,
    "Belgian Pro League": 10, "Turkish Süper Lig": 11, "Swiss Super League": 12,
    "Austrian Bundesliga": 13, "Scottish Premiership": 14, "MLS": 15
}

# טוען את קובץ הנתונים
@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error("שגיאה: הקובץ 'players_data-2024_2025.csv' לא נמצא בתיקייה. ודא שהוא קיים לצד app.py.")
        st.stop()
    return pd.read_csv(DATA_PATH, low_memory=False)

df = load_players()

# כותרת
st.title("🌟 מדד YSP-75 לשחקנים צעירים")

# שדה קלט לשם שחקן
name_input = st.text_input("הכנס שם שחקן (חלקי או מלא):")

# ניסיון לאתר את שם העמודה של שם השחקן
search_columns = ['short_name', 'Player', 'Name']
name_column = None
for col in search_columns:
    if col in df.columns:
        name_column = col
        break

if name_input and name_column:
    filtered = df[df[name_column].str.lower().str.contains(name_input.lower())]

    if filtered.empty:
        st.warning("לא נמצא שחקן בשם הזה.")
    else:
        player = filtered.iloc[0]
        name = player[name_column]
        age = player.get("age") or player.get("Age") or 0
        minutes = player.get("minutes") or player.get("Min") or 0
        goals = player.get("goals") or player.get("Gls") or 0
        assists = player.get("assists") or player.get("Ast") or 0
        league = player.get("league_name") or player.get("Comp") or "Unknown"

        # חישוב דירוג ליגה
        league_rank = LEAGUE_RANKINGS.get(league, 20)

        # חישוב מדד YSP-75
        try:
            score = (
                100
                - int(age) * 1.5
                + int(minutes) / 500
                + int(goals) * 2.5
                + int(assists) * 2
                - league_rank
            )
            score = round(score, 2)
        except:
            score = 0

        # ניתוח איכות
        if score >= 75:
            tag = "🏆 טופ עולמי"
        elif score >= 65:
            tag = "🚀 כישרון עם פוטנציאל ברור"
        elif score >= 55:
            tag = "👀 כישרון אך צריך יציבות"
        else:
            tag = "🔍 שחקן בבחינה"

        # תצוגת מידע
        st.subheader(f"{name}")
        st.markdown(f"**גיל:** {age} | **דקות:** {minutes} | **גולים:** {goals} | **בישולים:** {assists}")
        st.markdown(f"**ליגה:** {league} (דירוג {league_rank})")
        st.markdown(f"**מדד YSP-75:** `{score}` → {tag}")

# קרדיט
st.markdown("---")
st.caption("נתוני שחקנים באדיבות FBref.com – תחת תנאי שימוש חופשי עם קרדיט")
