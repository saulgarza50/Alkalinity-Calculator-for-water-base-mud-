import streamlit as st

st.set_page_config(page_title="🛢️ Alkalinity Contamination Calculator", layout="centered")

st.title("🧪 Alkalinity Contamination Calculator")
st.markdown("This calculator determines hydroxide, carbonate, and bicarbonate levels in water-based mud, flags contamination, and splits treatment into contamination and hardness/correction blocks.")

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

# Alkalinity Speciation
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

# Block 1 - Contamination Treatment
lime_contam = round(carbonate / 1200, 3) if carbonate > 0 else 0
caustic_contam = round(hydroxide / 340, 3) if hydroxide > 0 else 0
sodaash_contam = round((bicarbonate / 1220) * 1.5, 3) if bicarbonate > 0 else 0

# Block 2 - Calcium/Hardness Correction
excess_calcium = calcium - hardness
sodaash_hardness = round(excess_calcium / 1065, 3) if excess_calcium > 0 else 0
low_hardness_flag = hardness < 500

# Output
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"**Hardness (mg/L):** {round(hardness, 2)}")

# Block 1 Treatment Output
st.header("🧪 Block 1: Contamination Treatment (lb/bbl)")
st.write(f"**Lime:** {lime_contam}")
st.write(f"**Caustic Soda:** {caustic_contam}")
st.write(f"**Soda Ash:** {sodaash_contam}")

# Block 2 Treatment Output
st.header("🧪 Block 2: Calcium / Hardness Correction (lb/bbl)")
st.write(f"**Soda Ash (for excess Ca²⁺):** {sodaash_hardness}")
if low_hardness_flag:
    st.warning("⚠️ Hardness is below 500 mg/L. Risk of bicarbonate contamination, foaming, or pump cavitation due to excessive soda ash. Monitor treatment strategy.")

# Advisory Flags
st.header("🛡️ Advisory Flags")
flags = []
if bicarbonate > 100:
    flags.append("Bicarbonate Contamination (HCO₃⁻ > 100 mg/L)")
if carbonate > 100:
    flags.append("Carbonate Contamination (CO₃²⁻ > 100 mg/L)")
if calcium > 1000:
    flags.append("High Calcium (> 1000 mg/L)")
if hardness < 500:
    flags.append("Low Hardness (< 500 mg/L)")
if hydroxide > 0 and carbonate == 0 and bicarbonate == 0:
    flags.append("System Balanced (OH⁻ Only)")

if flags:
    st.error(" | ".join(flags))
else:
    st.success("✅ No contamination or imbalance detected.")

# Reset
if st.button("🔄 Reset"):
    st.experimental_rerun()
