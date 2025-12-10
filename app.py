
import streamlit as st
import random
import json
from pathlib import Path

SCOREBOARD_PATH_JSON = Path("scoreboard.json")
SCOREBOARD_PATH_CSV = Path("docs/demo/scoreboard.csv")

# ---------------- Scoreboard helpers ----------------
def ensure_dirs():
    try:
        SCOREBOARD_PATH_CSV.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

def load_scoreboard():
    try:
        if SCOREBOARD_PATH_JSON.exists():
            with open(SCOREBOARD_PATH_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception:
        pass
    return []

def save_score(player: str, score: int):
    ensure_dirs()
    sb = load_scoreboard()
    sb.append({"player": player or "Player", "score": int(score)})
    sb = sorted(sb, key=lambda x: x["score"], reverse=True)[:10]  # keep top 10
    # write JSON
    try:
        with open(SCOREBOARD_PATH_JSON, 'w', encoding='utf-8') as f:
            json.dump(sb, f, indent=2)
    except Exception:
        st.warning("Could not write scoreboard.json (ephemeral storage in cloud).")
    # write CSV (appears in GitHub Pages if committed)
    try:
        with open(SCOREBOARD_PATH_CSV, 'w', encoding='utf-8') as f:
            f.write("player,score
")
            for row in sb:
                f.write(f"{row['player']},{row['score']}
")
    except Exception:
        pass
    return sb

# ---------------- Game logic ----------------
def init_state():
    state = st.session_state
    if "initialized" not in state:
        state.hero = "Hero"
        state.enemy = "Enemy"
        state.age = 25
        state.hero_hp = 100
        state.enemy_hp = 100
        state.hero_score = 50  # +50 when battle starts
        state.handicap = 5 if state.age > 25 else 10
        state.power_boost = 1.0
        state.boost_ready = False
        state.game_over = False
        state.initialized = True
        state.scoreboard = load_scoreboard()


def punch(attacker, defender, defender_hp, min_damage=5, max_damage=15, power_boost=1.0):
    damage = int(random.randint(min_damage, max_damage) * power_boost)
    defender_hp = max(0, defender_hp - damage)
    st.write(f"{attacker} punches {defender} for {damage} damage. {defender} HP: {defender_hp}")
    return defender_hp


def holy_water(attacker, defender, defender_hp, min_damage=10, max_damage=25, power_boost=1.0):
    damage = int(random.randint(min_damage, max_damage) * power_boost)
    defender_hp = max(0, defender_hp - damage)
    st.write(f"{attacker} casts HOLY WATER on {defender} for {damage} damage. {defender} HP: {defender_hp}")
    return defender_hp


def dark_strike(attacker, defender, defender_hp):
    damage = random.randint(12, 25)
    defender_hp = max(0, defender_hp - damage)
    st.write(f"{attacker} uses DARK STRIKE on {defender} for {damage} damage. {defender} HP: {defender_hp}")
    return defender_hp


def reset_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    init_state()


st.set_page_config(page_title="Text Battle", page_icon=None)
st.title("Text Battle")
st.caption("A simple turn-based battle game with a Top 10 scoreboard.")

init_state()
s = st.session_state

with st.sidebar:
    st.subheader("Setup")
    s.hero = st.text_input("Hero name", s.hero)
    s.enemy = st.text_input("Enemy name", s.enemy)
    s.age = st.number_input("Your age", min_value=1, max_value=120, value=s.age)
    s.handicap = 5 if s.age > 25 else 10
    st.write(f"Age Bonus (handicap): +{s.handicap} points")
    if st.button("Reset Game"):
        reset_game()
        st.rerun()

# ---------------- Scoreboard display ----------------
st.subheader("Top 10 Scoreboard")
sb = s.scoreboard
if sb:
    st.table(sb)
else:
    st.write("No scores yet — finish a game and save your score!")

try:
    if SCOREBOARD_PATH_CSV.exists():
        with open(SCOREBOARD_PATH_CSV, 'rb') as f:
            st.download_button("Download scoreboard.csv", f, file_name="scoreboard.csv", mime="text/csv")
except Exception:
    pass

with st.expander("Admin: Clear scoreboard (local runs)"):
    if st.button("Clear scoreboard"):
        try:
            if SCOREBOARD_PATH_JSON.exists(): SCOREBOARD_PATH_JSON.unlink()
            if SCOREBOARD_PATH_CSV.exists(): SCOREBOARD_PATH_CSV.unlink()
            s.scoreboard = []
            st.success("Scoreboard cleared.")
        except Exception:
            st.warning("Could not clear scoreboard in this environment.")

# ---------------- Battle UI ----------------
if s.game_over:
    st.success("Game Over!")
    final_score = s.hero_score + s.handicap
    st.write(f"Base Score: {s.hero_score}")
    st.write(f"Age Bonus Applied: +{s.handicap} points")
    st.write(f"Final Score: {final_score}")

    # Save score to scoreboard
    player_name = st.text_input("Enter player name for scoreboard", value=s.hero)
    if st.button("Save score"):
        s.scoreboard = save_score(player_name, final_score)
        st.success("Score saved!")

else:
    st.subheader("Battle")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Hero HP", s.hero_hp)
    with col2:
        st.metric("Enemy HP", s.enemy_hp)

    action = st.radio("Choose your action:", ["PUNCH", "HOLY", "REST"], horizontal=True)

    if st.button("Take Turn"):
        # Player turn
        if action == "REST":
            s.power_boost = 1.5
            s.boost_ready = True
            st.info("You rest and charge up! Next attack will deal extra damage.")
        elif action == "PUNCH":
            hero_boost = s.power_boost if s.boost_ready else 1.0
            s.enemy_hp = punch(s.hero, s.enemy, s.enemy_hp, 8, 15, hero_boost)
            if s.boost_ready:
                st.info("Power boost used!")
                s.boost_ready = False
                s.power_boost = 1.0
        elif action == "HOLY":
            hero_boost = s.power_boost if s.boost_ready else 1.0
            s.enemy_hp = holy_water(s.hero, s.enemy, s.enemy_hp, 12, 22, hero_boost)
            if s.boost_ready:
                st.info("Power boost used!")
                s.boost_ready = False
                s.power_boost = 1.0

        # Check win
        if s.enemy_hp <= 0:
            st.success("Enemy defeated! You win!")
            s.game_over = True
        else:
            # Enemy turn
            if s.enemy_hp <= 30:
                s.hero_hp = dark_strike(s.enemy, s.hero, s.hero_hp)
            else:
                s.hero_hp = punch(s.enemy, s.hero, s.hero_hp, 5, 12)

            if s.hero_hp <= 0:
                st.error("You were defeated!")
                s.game_over = True

    st.divider()
    st.caption("Tip: Use REST to power-up your next attack.")
