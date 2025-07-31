import streamlit as st

st.set_page_config(page_title="🧪 Alkalinity Contamination Calculator", layout="centered")

st.title("🧪 Alkalinity Contamination Calculator")
st.markdown("This tool calculates hydroxide, carbonate, and bicarbonate concentrations in drilling fluid and recommends treatment actions based on alkalinity, calcium, and hardness.")

# Input section
st.header("🔢 Input Mud Check Values")

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

# Alkalinity Species Calculation (Table 5-2)
hydroxide = carbonate = bicarbonate = 0.0

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

# Contamination flags
contaminated = False
contam_reasons = []

if carbonate > 100:
    contaminated = True
    contam_reasons.append("Carbonate > 100 mg/L")
if bicarbonate > 100:
    contaminated = True
    contam_reasons.append("Bicarbonate > 100 mg/L")
if calcium > 1000:
    contaminated = True
    contam_reasons.append("Calcium > 1000 mg/L")
if hardness < 500:
    contaminated = True
    contam_reasons.append("Hardness < 500 mg/L")

# Output Results
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"**Hardness (mg/L):** {round(hardness, 2)}")

# Treatment Calculations (in lb/bbl)
lime_lb = round(carbonate / 1200, 2) if carbonate > 0 else 0
caustic_lb = round(lime_lb / 3, 2) if lime_lb > 0 else round(hydroxide / 340, 2) if hydroxide > 0 else 0
soda_ash_lb = round((bicarbonate / 1220) * 0.26, 3) if bicarbonate > 0 else 0

# Suggested Treatments
st.header("🧪 Suggested Treatments (lb/bbl)")
st.write(f"**Lime:** {lime_lb}")
st.write(f"**Caustic Soda:** {caustic_lb}")
st.write(f"**Soda Ash:** {soda_ash_lb}")

# Advisory
st.header("🛡️ Advisory")
if contaminated:
    st.error("⚠️ Contamination or imbalance detected:\n" + ", ".join(contam_reasons))
else:
    st.success("✅ System appears balanced — no contamination flagged.")

# Reset Button
if st.button("🔄 Reset Form"):
    st.experimental_rerun()