import streamlit as st

st.set_page_config(page_title="Alkalinity Contamination Calculator", layout="centered")

# === 🔹 INPUT SECTION ===
st.header("🧪 Input Mud Check Values")
pm = st.number_input("Phenolphthalein Alkalinity (Pm)", min_value=0.0, format="%.2f")
pf = st.number_input("Filtrate Alkalinity (Pf)", min_value=0.0, format="%.2f")
mf = st.number_input("M Alkalinity (Mf)", min_value=0.0, format="%.2f")
calcium = st.number_input("Calcium (mg/L)", min_value=0.0, format="%.1f")
hardness = st.number_input("Hardness (mg/L)", min_value=0.0, format="%.1f")

# === 🔹 ALKALINITY SPECIATION LOGIC ===
if pm >= mf:
    hydroxide = 340 * mf
    carbonate = 0
    bicarbonate = 0
elif pf == mf:
    hydroxide = 340 * pm
    carbonate = 120 * (mf - pm)
    bicarbonate = 0
elif pf > mf:
    hydroxide = 0
    carbonate = 0
    bicarbonate = 122 * pf
else:
    hydroxide = 0
    carbonate = 120 * pf
    bicarbonate = 122 * (mf - pf)

# === 🔹 CONTAMINATION FLAGS ===
contamination = carbonate > 100 or bicarbonate > 100
high_calcium = calcium > 1000
low_hardness = hardness < 500

# === 🔹 OUTPUT – ALKALINITY SPECIES ===
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"**Hardness (mg/L):** {round(hardness, 2)}")

# === 🔹 BLOCK 1: CONTAMINATION TREATMENT ===
st.subheader("🧪 Block 1: Contamination Treatment (lb/bbl)")
lime = round(carbonate / 1200, 2) if carbonate > 0 else 0
caustic = round(hydroxide / 340, 2) if hydroxide > 0 else 0
soda_ash = round((bicarbonate / 1220) * 1.5, 3) if bicarbonate > 0 else 0

st.write(f"**Lime:** {lime}")
st.write(f"**Caustic Soda:** {caustic}")
st.write(f"**Soda Ash:** {soda_ash}")

# === 🔹 BLOCK 2: CALCIUM / HARDNESS CORRECTION ===
st.subheader("🧪 Block 2: Calcium / Hardness Correction (lb/bbl)")
target_hardness = 500
excess_hardness = hardness - target_hardness

if excess_hardness > 0:
    excess_calcium = 0.8 * excess_hardness
    soda_ash_hardness_ppb = round((excess_calcium / 1000) * 6.4, 3)
else:
    soda_ash_hardness_ppb = 0

st.write(f"**Soda Ash (for excess Ca²⁺):** {soda_ash_hardness_ppb}")

# === 🔹 HIGH CALCIUM + CONTAMINATION STRATEGY ===
if high_calcium and (carbonate > 100 or bicarbonate > 100):
    caustic_override = round((calcium / 1000) * 0.25, 3)
    st.write(f"**⚠️ High Calcium Strategy: Add Caustic Soda = {caustic_override} lb/bbl**")

# === 🔹 ADVISORY FLAGS ===
st.subheader("🛡️ Advisory Flags")
if carbonate > 100:
    st.warning("⚠️ Carbonate Contamination Detected (CO₃²⁻ > 100 mg/L)")
if bicarbonate > 100:
    st.warning("⚠️ Bicarbonate Contamination Detected (HCO₃⁻ > 100 mg/L)")
if high_calcium:
    st.warning("⚠️ High Calcium (> 1000 mg/L) — monitor for hardness drop and foaming risk")
if low_hardness:
    st.warning("⚠️ Low Hardness (< 500 mg/L) — risk of bicarbonate foaming or cavitation")
