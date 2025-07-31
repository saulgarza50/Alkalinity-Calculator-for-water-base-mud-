import streamlit as st

st.set_page_config(page_title="Alkalinity Contamination Calculator", layout="centered")
st.title("🛢️ Alkalinity Contamination Calculator")

# Initialize reset state
if 'reset' not in st.session_state:
    st.session_state.reset = False

def reset_form():
    st.session_state.pm = 0.0
    st.session_state.pf = 0.0
    st.session_state.mf = 0.0
    st.session_state.calcium = 0.0
    st.session_state.hardness = 0.0

# Input section
st.header("🧪 Input Mud Check Values")
pm = st.number_input("PM (Mud Alkalinity)", min_value=0.0, step=0.1, format="%.1f", key="pm")
pf = st.number_input("PF (Filtrate Alkalinity)", min_value=0.0, step=0.1, format="%.1f", key="pf")
mf = st.number_input("MF (M Alkalinity)", min_value=0.0, step=0.1, format="%.1f", key="mf")
calcium = st.number_input("Calcium (mg/L)", min_value=0.0, step=10.0, format="%.0f", key="calcium")
hardness = st.number_input("Total Hardness (mg/L)", min_value=0.0, step=10.0, format="%.0f", key="hardness")

# Alkalinity species logic
if pf == 0:
    oh = 0
    co3 = 0
    hco3 = 1220 * mf
    zone = "Bicarbonate Only (HCO₃⁻)"
elif 2 * pf < mf:
    oh = 0
    co3 = 1200 * pf
    hco3 = 1220 * (mf - 2 * pf)
    zone = "Bicarbonate + Carbonate"
elif 2 * pf == mf:
    oh = 0
    co3 = 1200 * pf
    hco3 = 0
    zone = "Carbonate Only (CO₃²⁻)"
elif 2 * pf > mf:
    oh = 340 * (2 * pf - mf)
    co3 = 1200 * (mf - pf)
    hco3 = 0
    zone = "Hydroxide + Carbonate"
elif pf == mf:
    oh = 0
    co3 = 1200 * pf
    hco3 = 0
    zone = "Carbonate (w/ Possible Error)"
else:
    oh = co3 = hco3 = 0
    zone = "Unknown Alkalinity Pattern"

# Treatment logic
lime = round(co3 / 1200, 2) if co3 > 0 else 0
caustic = round(oh / 340, 2) if oh > 0 else 0
soda_ash = 0
if calcium > hardness:
    excess_ca = calcium - hardness
    soda_ash = round(excess_ca / 10, 2)

# Advisory flags
flags = []
if hco3 > 100: flags.append("High Bicarbonate")
if co3 > 100: flags.append("High Carbonate")
if oh > 50: flags.append("Excess Hydroxide")
if calcium > hardness: flags.append("Excess Calcium")
if hardness < 500: flags.append("Low Hardness")

# Output display
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (OH⁻):** {oh:.1f} mg/L")
st.write(f"**Carbonate (CO₃²⁻):** {co3:.1f} mg/L")
st.write(f"**Bicarbonate (HCO₃⁻):** {hco3:.1f} mg/L")
st.write(f"**Contamination Zone:** :orange[{zone}]")

st.subheader("🧪 Suggested Treatments")
st.write(f"- **Lime (ppb):** {lime}")
st.write(f"- **Caustic Soda (ppb):** {caustic}")
st.write(f"- **Soda Ash (ppb):** {soda_ash}")

st.subheader("📌 Advisory")
if flags:
    st.error("⚠️ Contamination or imbalance detected: " + ", ".join(flags))
else:
    st.success("✅ Mud system appears balanced — no treatment required.")

# Reset Button
if st.button("🔄 Reset Form"):
    reset_form()
    st.experimental_rerun()
