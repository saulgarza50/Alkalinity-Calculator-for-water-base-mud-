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

# === Alkalinity Species Calculation (Based on Table 5-2) ===
hydroxide = carbonate = bicarbonate = 0.0  # Reset

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
    hydroxide = carbonate = bicarbonate = 0  # Failsafe

# === Contamination Flags ===
contamination = (carbonate > 100) or (bicarbonate > 100)
high_calcium = calcium > 1000
low_hardness = hardness < 500

# === Output Section ===
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"**Hardness (mg/L):** {round(hardness, 2)}")

# === Contamination Treatment Block ===
st.subheader("🧪 Block 1: Contamination Treatment (lb/bbl)")

lime = round(carbonate / 1200, 2) if carbonate > 0 else 0
caustic = round(hydroxide / 340, 2) if hydroxide > 0 else 0
soda_ash = round((bicarbonate / 1220) * 1.5, 3) if bicarbonate > 0 else 0

st.write(f"Lime: {lime}")
st.write(f"Caustic Soda: {caustic}")
st.write(f"Soda Ash: {soda_ash}")

# === Calcium/Hardness Correction Block ===
st.subheader("🧪 Block 2: Calcium / Hardness Correction (lb/bbl)")

target_hardness = 500
excess_hardness = hardness - target_hardness

if excess_hardness > 0:
    excess_calcium = 0.8 * excess_hardness
    soda_ash_hardness_ppb = round((excess_calcium / 100) * 0.09, 3)
else:
    soda_ash_hardness_ppb = 0

st.write(f"Soda Ash (for excess Ca²⁺): {soda_ash_hardness_ppb}")

# === Advisory Flags ===
st.header("🛡️ Advisory Flags")
if contamination:
    st.warning("⚠️ Bicarbonate or Carbonate Contamination Detected")
if high_calcium:
    st.warning("⚠️ High Calcium (> 1000 mg/L)")
if low_hardness:
    st.warning("⚠️ Low Hardness (< 500 mg/L) — risk of foaming or pump cavitation")
if not (contamination or high_calcium or low_hardness):
    st.success("✅ No contamination or instability detected — fluid system appears balanced.")

# === Reset Button ===
if st.button("🔄 Reset"):
    st.experimental_rerun()
