import streamlit as st

st.set_page_config(page_title="🧪 Alkalinity Contamination Calculator", layout="centered")
st.title("🧪 Alkalinity Contamination Calculator")

st.markdown("This calculator determines hydroxide, carbonate, and bicarbonate concentrations in drilling fluid and calculates treatment recommendations for lime, caustic soda, and soda ash. It also flags system imbalances like excess calcium or low hardness.")

# Input helper
def safe_input(label, default="0.0"):
    try:
        return float(st.text_input(label, value=default))
    except:
        return 0.0

# Inputs
pm = safe_input("Phenolphthalein Alkalinity (Pm)")
pf = safe_input("Filtrate Alkalinity (Pf)")
mf = safe_input("M Alkalinity (Mf)")
calcium = safe_input("Calcium (mg/L)")
hardness = safe_input("Hardness (mg/L)")

# Initialize species concentrations
hydroxide = carbonate = bicarbonate = 0.0

# Determine alkalinity species
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

# Product treatment logic
lime_ppb = round(carbonate / 1200, 2) if carbonate > 0 else 0
caustic_ppb = round(hydroxide / 340, 2) if hydroxide > 0 else 0

# Soda ash is used to balance excess calcium — we assume theoretical calcium needed = hardness - Ca
required_calcium = max(hardness - calcium, 0)
calcium_ppb = round((calcium - required_calcium) / 10, 2)
soda_ash_ppb = round(calcium_ppb * -1, 3) if calcium_ppb > 0 else 0

# Display Results
st.subheader("📊 Alkalinity Species Results")
st.write(f"Hydroxide (mg/L): {round(hydroxide, 2)}")
st.write(f"Carbonate (mg/L): {round(carbonate, 2)}")
st.write(f"Bicarbonate (mg/L): {round(bicarbonate, 2)}")
st.write(f"Calcium (mg/L): {round(calcium, 2)}")
st.write(f"Hardness (mg/L): {round(hardness, 2)}")

st.subheader("🧪 Suggested Treatments")
st.write(f"Lime (ppb): {lime_ppb}")
st.write(f"Caustic Soda (ppb): {caustic_ppb}")
st.write(f"Soda Ash (ppb): {soda_ash_ppb}")

st.subheader("🛡️ Advisory")
flags = []
if bicarbonate > 100: flags.append("bicarbonate")
if carbonate > 100: flags.append("carbonate")
if hydroxide > 50: flags.append("hydroxide")
if calcium_ppb > 1.0: flags.append("excess calcium")
if hardness < 500: flags.append("low hardness")

if flags:
    st.error(f"⚠️ Contamination or imbalance detected: {', '.join(flags)}. Verify soda ash use and treatment levels.")
else:
    st.success("✅ System appears stable and balanced.")
