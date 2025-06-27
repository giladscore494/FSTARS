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

def ysp_75_score(row):
    try:
        age = row['Age']
        mp = row['MP']
        goals = row['Gls']
        assists = row['Ast']
        mins = row['Min']
        xg = row.get('xG', 0)
        xag = row.get('xAG', 0)
    except:
        return None

    if pd.isna(age) or age <= 0:
        return None

    age_factor = max(0, 1.0 - (age - 18) * 0.07)
    play_time_factor = min(mp / 30, 1.0)
    goal_factor = (goals + assists + xg + xag) / (mins / 90 + 1)
    
    ysp_score = (age_factor * 0.5 + play_time_factor * 0.3 + goal_factor * 0.2) * 100
    return round(ysp_score, 2)

# טען את הדאטה
df = load_players()

# ממשק
st.title("🎯 YSP-75 – מדד סיכויי הצלחה לשחקן צעיר")

name_input = st.text_input("הזן שם שחקן (באנגלית):")

if name_input:
    filtered = df[df['Player'].str.lower().str.contains(name_input.lower())]

    if filtered.empty:
        st.warning("שחקן לא נמצא בקובץ.")
    else:
        for _, row in filtered.iterrows():
            st.subheader(f"{row['Player']} ({row['Squad']})")
            score = ysp_75_score(row)
            if score is not None:
                st.markdown(f"**🔢 YSP-75 Score:** {score}/100")
            else:
                st.markdown("⚠️ לא ניתן לחשב ציון עבור שחקן זה (חסרים נתונים)")
