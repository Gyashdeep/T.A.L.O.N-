import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from groq import Groq

# --- CORE CONFIGURATION ---
st.set_page_config(page_title="T.A.L.O.N. Sovereign", layout="wide", initial_sidebar_state="collapsed")

# Placeholder for Hardware Bridge (Integration Point)
class TalonHardware:
    @staticmethod
    def get_telemetry():
        # In production: Use smbus2 to read Die Temp from PMBus
        # and request Grid Frequency from a local API/Smart Meter
        return {
            "die_temp": np.random.uniform(58, 85),
            "grid_hz": np.random.uniform(59.94, 60.06),
            "energy_price": np.random.uniform(-0.01, 0.15)
        }

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00FF41; }
    .stMetric { border: 1px solid #00FF41; background: #0a0a0a; border-radius: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROL ---
st.sidebar.title("🦅 T.A.L.O.N. CORE")
api_key = st.sidebar.text_input("GROQ API KEY", type="password")
thermal_limit = st.sidebar.slider("Thermal Throttle (C)", 70, 95, 85)
grid_target = st.sidebar.slider("Grid Sensitivity (Hz)", 59.90, 60.10, 60.00)

# --- DASHBOARD HEADER ---
st.title("T.A.L.O.N. // THERMAL-AWARE LOGICAL ORCHESTRATION")
col1, col2, col3, col4 = st.columns(4)
m1 = col1.empty()
m2 = col2.empty()
m3 = col3.empty()
m4 = col4.empty()

st.divider()
chart_placeholder = st.empty()
log_placeholder = st.empty()

# --- ENGINE EXECUTION ---
if st.sidebar.button("ENGAGE SYSTEM"):
    if not api_key:
        st.error("GROQ API KEY REQUIRED")
    else:
        client = Groq(api_key=api_key)
        history = []
        
        while True:
            # 1. Sense
            data = TalonHardware.get_telemetry()
            
            # 2. Arbitrate (The Groq Logic)
            action = "STABLE"
            if data['die_temp'] > thermal_limit or data['energy_price'] < 0.01:
                prompt = f"STATUS: Temp {data['die_temp']}C, Grid {data['grid_hz']}Hz, Price {data['energy_price']}. Command?"
                try:
                    completion = client.chat.completions.create(
                        messages=[{"role": "system", "content": "You are TALON. Output 1-word commands."},
                                 {"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile", # Using the most powerful available
                    )
                    action = completion.choices[0].message.content.upper()
                except Exception as e:
                    action = "FAILSAFE_ACTIVE"

            # 3. Update Metrics
            m1.metric("DIE TEMP", f"{data['die_temp']:.2f} C", f"{data['die_temp']-75:.1f}")
            m2.metric("GRID FREQ", f"{data['grid_hz']:.3f} Hz", f"{data['grid_hz']-60:.3f}")
            m3.metric("SPOT PRICE", f"${data['energy_price']:.4f}")
            m4.metric("ACTION", action)

            # 4. Update Visuals
            history.append({"Time": datetime.now(), "Temp": data['die_temp'], "Grid": (data['grid_hz']-60)*100 + 70})
            if len(history) > 50: history.pop(0)
            chart_placeholder.line_chart(pd.DataFrame(history).set_index("Time"))
            
            log_placeholder.info(f"TX: {datetime.now()} | COMMAND: {action} | STATUS: Arbitrage Active")
            
            time.sleep(0.5)
