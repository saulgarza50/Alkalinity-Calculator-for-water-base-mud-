import streamlit as st

st.set_page_config(page_title="🧪 Alkalinity Contamination Calculator", layout="centered")

st.title("🧪 Alkalinity Contamination Calculator")
st.markdown("This calculator determines hydroxide, carbonate, and bicarbonate concentrations in drilling fluid and flags treatment recommendations based on PM, PF, MF, calcium, and hardness.")

st.header("🔢 Input Mud Check Values")

# Safe float input handler
def safe_float_input(label, default="0.0"):
    try:
        return float(st.text_input(label, value=default))
    except:
        return 0.0

# Inputs
pm = safe_float_input("Phenolphthalein Alkalinity (Pm)")
pf = safe_float_input("Filtrate Alkalinity (Pf)")
mf = safe_float_input("M Alkalinity (Mf)")
calcium = safe_float_input("Calcium (mg/L)")
hardness = safe_float_input("Hardness (mg/L)")

# Initialize species
hydroxide = carbonate = bicarbonate = 0.0

# Species logic based on classic alkalinity tables
if pf == 0:
    bicarbonate = 1220 * mf
elif 2 * pf < mf:
    carbonate = 1200 * pf
    bicarbonate = 1220 * (mf - 2 * pf)
elif 2 * pf == mf:
    carbonate = 1200 * pf
elif 2 * pf > mf:
    hydroxide = 340 * (2 * pf - mf)
    carbonate = 1200 * (mf - pf)
elif pf == mf:
    hydroxide = 340 * mf

# Treatment Calculations
lime_ppb = round(carbonate / 1200, 2) if carbonate > 0 else 0
caustic_ppb = round(hydroxide / 340, 2) if hydroxide > 0 else 0

# Soda ash and calcium PPB logic based on Ca-Hardness
try:
    ca_ppb = round((calcium - (hardness - calcium)) / 10, 2)
    soda_ash_ppb = round(-1 * ca_ppb, 3)
except:
    ca_ppb = 0
    soda_ash_ppb = 0

# Output
st.header("📊 Alkalinity Species (mg/L)")
st.write(f"**Hydroxide (OH⁻):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (CO₃²⁻):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (HCO₃⁻):** {round(bicarbonate, 2)}")

st.header("🧪 Treatment Recommendations")
st.write(f"**Lime (ppb):** {lime_ppb}")
st.write(f"**Caustic Soda (ppb):** {caustic_ppb}")
st.write(f"**Soda Ash (ppb):** {soda_ash_ppb}")
st.write(f"**Calcium (ppb):** {ca_ppb}")

# Advisory Zone
st.header("🛡️ Advisory Zone")
flags = []
if bicarbonate > 0: flags.append("bicarbonate")
if carbonate > 0: flags.append("carbonate")
if hydroxide > 0: flags.append("hydroxide")
if ca_ppb > 1: flags.append("excess calcium")
if hardness < 500: flags.append("low hardness")

if flags:
    st.error(f"⚠️ Contamination or imbalance detected: {', '.join(flags)}. Review treatment strategy.")
else:
    st.success("✅ System appears balanced — no contamination flagged.")
