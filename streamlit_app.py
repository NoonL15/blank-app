import streamlit as st
import random

# --- INITIAL SETUP ---
st.set_page_config(page_title="Sustainable City Simulator", layout="centered")
st.title("🌱 Sustainable City Simulator")
st.write("You're the mayor of a growing city. Over the next 10 years, your goal is to make it more sustainable while keeping citizens happy and staying within your budget.")

# --- SESSION STATE INITIALIZATION ---
if 'year' not in st.session_state:
    st.session_state.year = 1
    st.session_state.sustainability = 50
    st.session_state.happiness = 50
    st.session_state.budget = 10_000_000  # $10 million
    st.session_state.history = []
    st.session_state.pending_event = None  # No event at start

# Display progress bars
st.subheader("📊 City Stats")

st.progress(min(st.session_state.sustainability / 100, 1.0), text=f"🌱 Sustainability: {st.session_state.sustainability}/100")
st.progress(min(st.session_state.happiness / 100, 1.0), text=f"😊 Happiness: {st.session_state.happiness}/100")

# Budget as a custom text + visual
budget_ratio = min(st.session_state.budget / 5_000_000, 1.0)
st.progress(budget_ratio, text=f"💰 Budget: ${st.session_state.budget:,.0f}")

# --- DISPLAY CURRENT STATS ---
st.markdown(f"### 📆 Year: {st.session_state.year}/10")
col1, col2, col3 = st.columns(3)
col1.metric("🌿 Sustainability", f"{st.session_state.sustainability}/100")
col2.metric("😊 Happiness", f"{st.session_state.happiness}/100")
col3.metric("💰 Budget", f"${st.session_state.budget:,}")

st.divider()

# --- DECISION OPTIONS ---
transport_options = {
    "Expand bike lanes": (500_000, 5, 3),
    "Subsidize electric buses": (2_000_000, 10, 5),
    "Build more highways": (3_000_000, -5, -2),
}

energy_options = {
    "Install solar panels": (1_500_000, 7, 2),
    "Invest in wind energy": (2_500_000, 10, 3),
    "Keep coal plants running": (0, -10, -5),
}

waste_options = {
    "Start compost program": (800_000, 6, 3),
    "Ban single-use plastics": (1_000_000, 8, -2),
    "Do nothing": (0, -3, 0),
}

green_space_options = {
    "Plant urban forests": (2_000_000, 9, 4),
    "Add rooftop gardens": (1_200_000, 6, 2),
    "Convert parks to condos": (3_000_000, -8, -6),
}

# User choices for decisions
transport_choice = st.radio("Choose your transportation initiative:", list(transport_options.keys()))
energy_choice = st.radio("Choose your energy initiative:", list(energy_options.keys()))
waste_choice = st.radio("Choose your waste initiative:", list(waste_options.keys()))
green_choice = st.radio("Choose your green space initiative:", list(green_space_options.keys()))

# --- RANDOM EVENT OPTIONS ---
random_events = [
    {
        "description": "🌪️ A wildfire destroys part of your urban forest. Replant trees?",
        "type": "warning",
        "yes": {"sustainability": 2, "happiness": 3, "cost": 800_000},
        "no": {"sustainability": -4, "happiness": -3, "cost": 0}
    },
    {
        "description": "🔥 A severe heatwave strikes. Build cooling stations?",
        "type": "warning",
        "yes": {"sustainability": 1, "happiness": 4, "cost": 500_000},
        "no": {"sustainability": -3, "happiness": -2, "cost": 0}
    },
    {
        "description": "🚌 A protest demands better transit. Expand buses?",
        "type": "info",
        "yes": {"sustainability": 3, "happiness": 2, "cost": 400_000},
        "no": {"sustainability": -1, "happiness": -1, "cost": 0}
    },
    {
        "description": "🎉 Your city wins a green award! Celebrate publicly?",
        "type": "success",
        "yes": {"sustainability": 0, "happiness": 3, "cost": 100_000},
        "no": {"sustainability": 0, "happiness": 0, "cost": 0}
    },
    {
        "description": "🌊 Rising sea levels are imminent. Build flood barriers?",
        "type": "error",
        "yes": {"sustainability": 4, "happiness": -1, "cost": 2_000_000},
        "no": {"sustainability": -6, "happiness": -2, "cost": 0}
    }
]

# --- RANDOM EVENT TRIGGER ---
def trigger_random_event():
    st.session_state.pending_event = random.choice(random_events)

# --- APPLY CHOICES AND HANDLE EVENTS ---
def apply_choices():
    transport = transport_options[transport_choice]
    energy = energy_options[energy_choice]
    waste = waste_options[waste_choice]
    green_space = green_space_options[green_choice]
    
    # Update sustainability, happiness, and budget
    st.session_state.sustainability += transport[1] + energy[1] + waste[1] + green_space[1]
    st.session_state.happiness += transport[2] + energy[2] + waste[2] + green_space[2]
    st.session_state.budget -= transport[0] + energy[0] + waste[0] + green_space[0]

    # Trigger a random event
    trigger_random_event()

    # Add choice results to history
    st.session_state.history.append({
        "year": st.session_state.year,
        "transport": transport_choice,
        "energy": energy_choice,
        "waste": waste_choice,
        "green_space": green_choice
    })

    # Update year
    st.session_state.year += 1

# --- RESPOND TO RANDOM EVENT ---
if st.session_state.pending_event:
    event = st.session_state.pending_event
    st.info(event["description"])

    col1, col2 = st.columns(2)
    if col1.button("✅ Respond"):
        impact = event["yes"]
        st.session_state.sustainability += impact["sustainability"]
        st.session_state.happiness += impact["happiness"]
        st.session_state.budget -= impact["cost"]
        st.success("You responded to the event.")
        st.session_state.pending_event = None

    if col2.button("❌ Ignore"):
        impact = event["no"]
        st.session_state.sustainability += impact["sustainability"]
        st.session_state.happiness += impact["happiness"]
        st.session_state.budget -= impact["cost"]
        st.warning("You ignored the event.")
        st.session_state.pending_event = None

# --- NEXT YEAR BUTTON ---
if st.button("Next Year"):
    if st.session_state.year <= 10:
        apply_choices()
        st.experimental_rerun()  # Refresh the app to update stats
    else:
        st.write("Game over! You completed 10 years as mayor.")
        # Display final stats
        st.write(f"Final Sustainability: {st.session_state.sustainability}/100")
        st.write(f"Final Happiness: {st.session_state.happiness}/100")
        st.write(f"Final Budget: ${st.session_state.budget:,}")
        st.write("Thank you for playing!")



