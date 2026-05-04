import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from groq import Groq

# --- SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="T.A.L.O.N. SOVEREIGN ENGINE",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THE HARDWARE ABSTRACTION LAYER ---
class TalonHardware:
    @staticmethod
    def get_telemetry():
        """
        INTERFACE: Silicon Die + Energy Grid. 
        In production, replace np.random with smbus2/API calls.
        """
        return {
            "die_temp": np.random.uniform(55, 88),   # Celsius
            "grid_hz": np.random.uniform(59.92, 60.08), # Hz
            "spot_price": np.random.uniform(-0.02, 0.14) # USD/kWh
        }

# --- STYLING (INDUSTRIAL INTERFACE) ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF41; font-family: 'Courier New', monospace; }
    [data-testid="stMetricValue"] { font-size: 2.5rem; color: #00FF41; }
    .stMetric { border: 1px solid #00FF41; padding: 20px; background: #0a0a0a; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SOVEREIGN CONTROL ---
st.sidebar.header("🦅 T.A.L.O.N. COMMAND")
st.sidebar.markdown("---")

# Secure Key Retrieval
api_key = st.secrets.get("GROQ_API_KEY") or st.sidebar.text_input("Enter Groq API Key", type="password")

thermal_threshold = st.sidebar.slider("Thermal Ceiling (°C)", 75, 95, 85)
grid_sensitivity = st.sidebar.slider("Grid Sensitivity (Hz)", 59.90, 60.10, 60.00)
st.sidebar.markdown("---")

# --- UI LAYOUT ---
st.title("T.A.L.O.N. // SOVEREIGN ARBITRAGE TERMINAL")
st.caption("Silicon-Grid Unified Circuit v3.14 (Optimized for Groq LPU)")

col1, col2, col3, col4 = st.columns(4)
die_ui = col1.empty()
grid_ui = col2.empty()
price_ui = col3.empty()
status_ui = col4.empty()

st.divider()
chart_col, log_col = st.columns([2, 1])
with chart_col:
    st.subheader("ECT Manifold (Energy-Compute-Thermal)")
    chart_ui = st.empty()
with log_col:
    st.subheader("Sovereign Decision Stream")
    log_ui = st.empty()

# --- ENGINE EXECUTION ---
if st.sidebar.button("ENGAGE SOVEREIGN CORE"):
    if not api_key:
        st.error("SYSTEM CRITICAL: Groq API Key Missing. Check secrets.toml or sidebar.")
    else:
        client = Groq(api_key=api_key)
        history = pd.DataFrame(columns=["time", "Die Temp", "Grid Sync"])
        
        while True:
            # 1. LIVE TELEMETRY
            telemetry = TalonHardware.get_telemetry()
            ts = datetime.now()
            
            # 2. GROQ ARBITRAGE LOGIC (The "Industry Shock" Brain)
            decision = "STABLE"
            if telemetry['die_temp'] > thermal_threshold or telemetry['spot_price'] < 0.01:
                try:
                    chat = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are the T.A.L.O.N. Arbitrator. Analyze physics/price data. Provide 1-word commands: OVERDRIVE, SHED_LOAD, or THROTTLE."},
                            {"role": "user", "content": f"T:{telemetry['die_temp']}C, F:{telemetry['grid_hz']}Hz, P:${telemetry['spot_price']}"}
                        ],
                        model="llama-3.3-70b-versatile",
                        max_tokens=10
                    )
                    decision = chat.choices[0].message.content.strip().upper()
                except:
                    decision = "FAILSAFE_ACTIVE"

            # 3. UPDATE METRICS
            die_ui.metric("DIE JUNCTION", f"{telemetry['die_temp']:.2f} °C", delta=f"{telemetry['die_temp']-75:.1f}")
            grid_ui.metric("GRID SINE", f"{telemetry['grid_hz']:.3f} Hz", delta=f"{telemetry['grid_hz']-60.0:.3f}")
            price_ui.metric("SPOT PRICE", f"${telemetry['spot_price']:.4f}/kWh")
            status_ui.metric("ENGINE STATE", decision)

            # 4. UPDATE MANIFOLD CHART
            # Scaling Grid Frequency for visualization alongside Temperature
            scaled_grid = (telemetry['grid_hz'] - 60) * 200 + 70 
            new_row = pd.DataFrame({"time": [ts], "Die Temp": [telemetry['die_temp']], "Grid Sync": [scaled_grid]})
            history = pd.concat([history, new_row]).tail(40)
            chart_ui.line_chart(history.set_index("time"), color=["#00FF41", "#FF4B4B"])

            # 5. LOGGING
            log_ui.code(f"[{ts.strftime('%H:%M:%S')}] CMD >> {decision}\nSYS >> {telemetry['spot_price']:.4f} USD/kWh")

            time.sleep(0.5) # The "Heartbeat" interval
else:
    st.sidebar.warning("Engine Standby: Awaiting Sovereign Engagement")
    st.info("The T.A.L.O.N. system is ready. Ensure hardware connection is verified and API key is set.")
