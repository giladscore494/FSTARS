import os
import streamlit as st
import pandas as pd

# נתיב לקובץ CSV (הקובץ באותה תיקייה כמו app.py)
DATA_PATH = "players_data-2024_2025.csv"
import os
st.write("Current directory:", os.getcwd())
st.write("Files in directory:", os.listdir())

@st.cache_data
def load_players():
    if not os.path.exists(DATA_PATH):
        st.error(f"שגיאה: הקובץ '{DATA_PATH}' לא נמצא בתיקייה. ודא שהוא נמצא לצד app.py.")
        st.stop()
    return pd.read_csv(DATA_PATH, low_memory=False)

df = load_players()
df = load_players() 
# דירוג ליגות אירופאיות - לפי דירוג אופ"א נכון ל־2025
LEAGUE_TIER = {
    "Premier League": 1,
    "La Liga": 2,
    "Bundesliga": 3,
    "Serie A": 4,
    "Ligue 1": 5,
    "Eredivisie": 6,
    "Primeira Liga": 7,
    "Belgian Pro League": 8,
    "Scottish Premiership": 9,
    "Super Lig": 10,
    "Swiss Super League": 11,
    "Ukrainian Premier League": 12,
    "Greek Super League": 13,
    "Czech First League": 14,
    "Austrian Bundesliga": 15,
    "Russian Premier League": 16,
    "Danish Superliga": 17,
    "Croatian First Football League": 18,
    "Cypriot First Division": 19,
    "Norwegian Eliteserien": 20,
    "Polish Ekstraklasa": 21,
    "Swedish Allsvenskan": 22,
    "Serbian SuperLiga": 23,
    "Israeli Premier League": 24,
    "Romanian Liga I": 25,
    "Slovak Super Liga": 26,
    "Hungarian NB I": 27,
    "Slovenian PrvaLiga": 28,
    "Bulgarian First League": 29,
    "Kazakhstan Premier League": 30,
    "Georgian Erovnuli Liga": 31,
    "Belarusian Premier League": 32,
    "Armenian Premier League": 33,
    "Bosnian Premier League": 34,
    "Latvian Higher League": 35,
    "Lithuanian A Lyga": 36,
    "Estonian Meistriliiga": 37,
    "Finnish Veikkausliiga": 38,
    "Maltese Premier League": 39,
    "Gibraltar National League": 40,
    "Moldovan Super Liga": 41,
    "Faroe Islands Premier League": 42,
    "Icelandic Úrvalsdeild": 43,
    "Northern Ireland Premiership": 44,
    "Luxembourg National Division": 45,
    "Andorran Primera Divisió": 46,
    "San Marino Campionato": 47,
    "Welsh Premier League": 48,
    "Kosovo Superleague": 49,
    "Liechtenstein Clubs": 50,
    "Albanian Superliga": 51,
    "Montenegrin First League": 52,
    "North Macedonian First League": 53,
    "Azerbaijani Premier League": 54,
    "Irish Premier Division": 55,
}

@st.cache_data
def load_players():
    return pd.read_csv(DATA_PATH)

def league_score(league):
    return max(0, 100 - 1.5 * (LEAGUE_TIER.get(league, 60)))  # ליגה לא מדורגת תקבל ניקוד נמוך

def calculate_score(player):
    base = 50
    base += min(player["minutes"] / 300, 10)
    base += min((player["goals"] + player["assists"]) / 2, 10)
    base += league_score(player["league_name"]) / 10
    base -= max(0, player["age"] - 22) * 0.75
    return round(base, 2)

def get_label(score):
    if score >= 75:
        return "🌍 טופ עולמי"
    elif score >= 65:
        return "⭐ כישרון עם פוטנציאל ברור"
    elif score >= 55:
        return "⚠️ כישרון שדורש יציבות"
    else:
        return "🚧 מתחת לסף"

st.title("🎯 YSP-75 – מדד סיכוי הצלחה לשחקן צעיר")

name = st.text_input("הכנס שם שחקן:")

if name:
    df = load_players()
    results = df[df["short_name"].str.lower().str.contains(name.lower())]
    if results.empty:
        st.warning("שחקן לא נמצא בקובץ.")
    else:
        player = results.iloc[0]
        score = calculate_score(player)
        label = get_label(score)

        st.markdown(f"### 🧑‍💼 שם: {player['short_name']}")
        st.markdown(f"**גיל:** {player['age']}")
        st.markdown(f"**קבוצה:** {player['club_name']}")
        st.markdown(f"**ליגה:** {player['league_name']}")
        st.markdown(f"**דקות משחק:** {player['minutes']}")
        st.markdown(f"**שערים:** {player['goals']} | **בישולים:** {player['assists']}")
        st.markdown(f"**ציון YSP-75:** `{score}`")
        st.markdown(f"**הערכת פוטנציאל:** {label}")
        st.markdown("---")
        st.caption("נתוני שחקנים באדיבות FBref.com – תחת תנאי שימוש חופשי עם קרדיט")
