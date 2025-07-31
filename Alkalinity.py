port streamlit as st

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

# Alkalinity Species Logic
hydroxide = carbonate = bicarbonate = 0.0

if pm == 0:
    bicarbonate = 122.5 * mf
elif pm == pf:
    hydroxide = 34 * pf
elif pm > pf:
    hydroxide = 34 * (pm - pf)
    carbonate = 60 * (2 * pf)
else:
    carbonate = 60 * pf
    bicarbonate = 122.5 * (mf - pf)

# Contamination check including hardness logic
contamination = (carbonate > 100) or (bicarbonate > 100) or (calcium > 1000) or (hardness < 500)

# Output Alkalinity Species
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"**Hardness (mg/L):** {round(hardness, 2)}")

# Treatment Recommendations
st.header("🧪 Suggested Treatments")

lime_ppb = round(carbonate / 1200, 2) if carbonate > 0 else 0
caustic_ppb = round(hydroxide / 340, 2) if hydroxide > 0 else 0
soda_ash_ppb = round((bicarbonate / 1220) * 1.5, 2) if bicarbonate > 0 else 0

st.write(f"**Lime (ppb):** {lime_ppb}")
st.write(f"**Caustic Soda (ppb):** {caustic_ppb}")
st.write(f"**Soda Ash (ppb):** {soda_ash_ppb}")

# Advisory
st.header("🛡️ Advisory")
if contamination:
    st.error("⚠️ Contamination or imbalance detected: carbonate, bicarbonate, calcium, or low hardness. Verify soda ash use and treatment levels.")
else:
    st.success("✅ System appears balanced — no contamination flagged.")
