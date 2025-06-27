import streamlit as st
import pandas as pd
import os

# הגדרת נתיב מלא לקובץ CSV מתוך תיקיית האפליקציה
DATA_PATH = os.path.join(os.path.dirname(__file__), "players_data-2024_2025.csv")

# טוען את כל הנתונים עם שמירה בזיכרון
@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error("\u274c שגיאה: הקובץ 'players_data-2024_2025.csv' לא נמצא בתיקייה. ודא שהוא קיים לצד app.py.")
        st.stop()
    return pd.read_csv(DATA_PATH, low_memory=False)

# טוען הנתונים
players_df = load_players()

# הכותרת והקלט
st.title("\ud83c\udf1f YSP-75: דירוג פוטנציאל לשחקנים צעירים")
name_input = st.text_input("הכנס שם שחקן:")

if name_input:
    # בדיקה: עמודה נכונה
    valid_columns = ["short_name", "Player"]
    found_col = None
    for col in valid_columns:
        if col in players_df.columns:
            found_col = col
            break

    if not found_col:
        st.error("\u274c לא נמצאה עמודת שמות תקינה בקובץ.")
        st.stop()

    # סינון לפי שם (מזהה גם תווים קטנים)
    filtered = players_df[players_df[found_col].str.lower().str.contains(name_input.lower())]

    if filtered.empty:
        st.warning("\u26a0\ufe0f לא נמצא שחקן תואם.")
    else:
        player = filtered.iloc[0]  # השחקן הראשון המתאים

        # חישוב מדד YSP-75 לפי שדות קיימים
        age = player.get("Age", player.get("age", 0))
        minutes = player.get("Min", player.get("minutes", 0))
        goals = player.get("Gls", player.get("goals", 0))
        assists = player.get("Ast", player.get("assists", 0))
        league = player.get("Comp", player.get("league_name", ""))

        try:
            age = float(age)
            minutes = float(minutes)
            goals = float(goals)
            assists = float(assists)
        except:
            st.error("\u274c שגיאה בקריאת ערכי גיל או סטטיסטיקות")
            st.stop()

        # דירוג ליגה (דירוג בינ"ל מדומה)
        LEAGUE_SCORES = {
            'Premier League': 1.0, 'La Liga': 0.95, 'Serie A': 0.9,
            'Bundesliga': 0.9, 'Ligue 1': 0.85,
            'Championship': 0.75, 'Eredivisie': 0.7, 'Liga Portugal': 0.7,
            'Belgian Pro League': 0.65, 'Turkish Super Lig': 0.6,
            # ... המשך ליגות לפי צורך ...
        }
        league_score = LEAGUE_SCORES.get(league, 0.5)

        # שקלול כולל למדד YSP-75
        score = (
            (90 - age) * 0.25 +
            (minutes / 3000) * 25 +
            (goals + assists) * 2 +
            league_score * 20
        )

        # קטגוריה
        if score >= 75:
            tag = "\ud83c\udfc6 טופ עולמי!"
        elif score >= 65:
            tag = "\u2b50 פוטנציאל ברור – שווה מעקב"
        elif score >= 55:
            tag = "\u23f3 כישרון עם צורך ביציבות"
        else:
            tag = "\ud83c\udfa7 צריך שיפור"

        # הצגה
        st.subheader(f"{player[found_col]} – ציון: {round(score,1)}")
        st.markdown(f"**{tag}**")

        st.markdown("---")
        st.write("**נתונים**:")
        st.write({
            "גיל": age,
            "דקות": minutes,
            "גולים": goals,
            "בישולים": assists,
            "ליגה": league
        })

        st.caption("\u2139\ufe0f מבוסס על נתוני FBref – שימוש מותר עם קרדיט")
