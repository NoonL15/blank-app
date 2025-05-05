# streamlit_app.py
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

# Example structure: 'label': (cost, sustainability_change, happiness_change)
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
st.subheader("🚲 Transportation")
transport_choice = st.radio("Choose your transportation initiative:", list(transport_options.keys()))

st.subheader("⚡ Energy")
energy_choice = st.radio("Choose your energy initiative:", list(energy_options.keys()))

st.subheader("🗑 Waste Management")
waste_choice = st.radio("Choose your waste initiative:", list(waste_options.keys()))

st.subheader("🌳 Green Space")
green_choice = st.radio("Choose your green space initiative:", list(green_space_options.keys()))
# --- APPLY CHOICES AND UPDATE STATS ---
def apply_choices():
    # Get the selected choices
    transport = transport_options[transport_choice]
    energy = energy_options[energy_choice]
    waste = waste_options[waste_choice]
    green_space = green_space_options[green_choice]
    
    # Update sustainability, happiness, and budget
    st.session_state.sustainability += transport[1] + energy[1] + waste[1] + green_space[1]
    st.session_state.happiness += transport[2] + energy[2] + waste[2] + green_space[2]
    st.session_state.budget -= transport[0] + energy[0] + waste[0] + green_space[0]

    # Trigger a random event (we'll create this next!)
    random_event()

    # Update year
    st.session_state.year += 1

    # Add choice results to history
    st.session_state.history.append({
        "year": st.session_state.year - 1,
        "transport": transport_choice,
        "energy": energy_choice,
        "waste": waste_choice,
        "green_space": green_choice
    })

# --- RANDOM EVENT FUNCTION ---
def random_event():
    events = [
        ("A wildfire destroys part of the forest. Replant?", -3, 5, 1_000_000),
        ("A heatwave hits the city. Install cooling stations?", -2, 3, 500_000),
        ("A citizen protest demands better public transport. Do you respond?", 2, 0, 200_000),
        ("Your city is featured in a 'Top Green Cities' article!", 5, 4, 0),
        ("Rising sea levels flood low-lying areas. Invest in flood barriers?", -5, -3, 2_500_000),
    ]
    
    event = random.choice(events)
    st.session_state.sustainability += event[1]
    st.session_state.happiness += event[2]
    st.session_state.budget -= event[3]

    # Display the random event
    st.info(f"🔔 **Event:** {event[0]}")
    st.write(f"**Sustainability:** {event[1]} | **Happiness:** {event[2]} | **Cost:** ${event[3]:,}")

# --- 'Next Year' BUTTON ---
if st.button("Next Year"):
    if st.session_state.year <= 10:
        apply_choices()
        st.experimental_rerun()  # Rerun the app to refresh stats
    else:
        st.write("Game over! You completed 10 years as mayor.")
        # Display final stats and show ending message
        st.write(f"Final Sustainability Score: {st.session_state.sustainability}/100")
        st.write(f"Final Happiness: {st.session_state.happiness}/100")
        st.write(f"Final Budget: ${st.session_state.budget:,}")
        st.write("Thank you for playing! Your city’s future depends on your choices!")
import random

random_events = [
    {
        "description": "🌪️ A wildfire destroys part of your urban forest. Do you replant trees?",
        "sustainability_change": -3,
        "happiness_change": 5,
        "cost": 1_000_000,
        "type": "warning"
    },
    {
        "description": "🔥 A severe heatwave strikes. Citizens demand cooling stations.",
        "sustainability_change": -2,
        "happiness_change": 3,
        "cost": 500_000,
        "type": "warning"
    },
    {
        "description": "🚌 A citizen protest pushes for better transit. Do you invest?",
        "sustainability_change": 2,
        "happiness_change": 0,
        "cost": 200_000,
        "type": "info"
    },
    {
        "description": "🎉 Your city wins a national green innovation award!",
        "sustainability_change": 5,
        "happiness_change": 4,
        "cost": 0,
        "type": "success"
    },
    {
        "description": "🌊 Rising sea levels threaten infrastructure. Flood barriers are needed.",
        "sustainability_change": -5,
        "happiness_change": -3,
        "cost": 2_500_000,
        "type": "error"
    }
]
def random_event():
    event = random.choice(random_events)

    # Update game stats
    st.session_state.sustainability += event["sustainability_change"]
    st.session_state.happiness += event["happiness_change"]
    st.session_state.budget -= event["cost"]

    # Display event info
    if event["type"] == "success":
        st.success(event["description"])
    elif event["type"] == "warning":
        st.warning(event["description"])
    elif event["type"] == "error":
        st.error(event["description"])
    else:
        st.info(event["description"])

    st.write(f"**Impact**: Sustainability {event['sustainability_change']}, Happiness {event['happiness_change']}, Cost ${event['cost']:,}")
def apply_choices():
    # Apply decision-based stat changes (same as before)

    # Then trigger one random event per year
    random_event()

    # Update year
    st.session_state.year += 1
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
if "pending_event" not in st.session_state:
    st.session_state.pending_event = None
def random_event():
    st.session_state.pending_event = random.choice(random_events)
if st.session_state.pending_event:
    event = st.session_state.pending_event
    if event["type"] == "success":
        st.success(event["description"])
    elif event["type"] == "warning":
        st.warning(event["description"])
    elif event["type"] == "error":
        st.error(event["description"])
    else:
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


