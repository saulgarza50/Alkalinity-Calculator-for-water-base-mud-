
import streamlit as st

st.set_page_config(page_title="🧪 Alkalinity Contamination Calculator", layout="centered")

st.title("🧪 Alkalinity Contamination Calculator")
st.markdown("This tool calculates hydroxide, carbonate, and bicarbonate concentrations in drilling fluid and recommends treatment actions based on alkalinity, calcium, and hardness.")

st.header("🔢 Input Mud Check Values")

# Clean input fields using text_input and convert to float
def safe_float_input(label, default="0.0"):
    try:
        return float(st.text_input(label, value=default))
    except:
        return 0.0

pm = safe_float_input("Phenolphthalein Alkalinity (Pm)")
pf = safe_float_input("Filtrate Alkalinity (Pf)")
mf = safe_float_input("M Alkalinity (Mf)")
calcium = safe_float_input("Calcium (mg/L)")
hardness = safe_float_input("Hardness (mg/L)")

# Alkalinity Species Calculation (Based on Table 5-2)
hydroxide = carbonate = bicarbonate = 0.0

if pf == 0:
    hydroxide = 0
    carbonate = 0
    bicarbonate = 1220 * mf
elif 2 * pf < mf:
    hydroxide = 0
    carbonate = 1200 * pf
    bicarbonate = 1220 * (mf - 2 * pf)
elif 2 * pf == mf:
    hydroxide = 0
    carbonate = 1200 * pf
    bicarbonate = 0
elif 2 * pf > mf:
    hydroxide = 340 * (2 * pf - mf)
    carbonate = 1200 * (mf - pf)
    bicarbonate = 0
elif pf == mf:
    hydroxide = 340 * mf
    carbonate = 0
    bicarbonate = 0
else:
    hydroxide = carbonate = bicarbonate = 0

# Contamination check including hardness logic
contamination = (carbonate > 100) or (bicarbonate > 100) or (calcium > 1000) or (hardness < 500)

# Output Alkalinity Species
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"**Hardness (mg/L):** {round(hardness, 2)}")

# Treatment Calculations (Field-Based Logic)
try:
    lime_ppb = round(carbonate / 1200, 2) if carbonate > 0 else 0.00
    caustic_ppb = round(hydroxide / 340, 2) if hydroxide > 0 else 0.00
    soda_ash_ppb = round(bicarbonate / 1220, 2) if bicarbonate > 0 else 0.00
    calcium_correction_ppb = round((calcium - hardness) / 20, 2) if calcium > hardness else 0.00
except:
    lime_ppb = caustic_ppb = soda_ash_ppb = calcium_correction_ppb = 0.00

# Display Treatments
st.header("🧪 Suggested Treatments (Field Dosage Estimates)")
st.write(f"**Lime (ppb):** {lime_ppb}")
st.write(f"**Caustic Soda (ppb):** {caustic_ppb}")
st.write(f"**Soda Ash (ppb):** {soda_ash_ppb}")
st.write(f"**Calcium Treatment (CaO, ppb):** {calcium_correction_ppb}")

# Advisory
st.header("🛡️ Advisory")
if contamination:
    st.error("⚠️ Contamination or imbalance detected: carbonate, bicarbonate, calcium, or low hardness. Verify soda ash use and treatment levels.")
else:
    st.success("✅ System appears balanced — no contamination flagged.")
