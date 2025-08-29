import streamlit as st
import pandas as pd

# === 🔹 PAGE CONFIGURATION ===
st.set_page_config(page_title="Alkalinity Contamination Calculator", layout="centered")
st.title("🛢️ Alkalinity Contamination Calculator")

# === 🔹 INPUT SECTION ===
st.header("🧪 Input Mud Check Values")

pm = st.number_input("Phenolphthalein Alkalinity (Pm)", min_value=0.0, format="%.2f")
pf = st.number_input("Filtrate Alkalinity (Pf)", min_value=0.0, format="%.2f")
mf = st.number_input("M Alkalinity (Mf)", min_value=0.0, format="%.2f")
calcium = st.number_input("Calcium (mg/L)", min_value=0.0, format="%.1f")
hardness = st.number_input("Hardness (mg/L)", min_value=0.0, format="%.1f")

# === 🔹 ALKALINITY SPECIATION LOGIC ===
hydroxide = 0
carbonate = 0
bicarbonate = 0

if pm >= mf:
    # OH only
    hydroxide = 340 * mf
elif (pm > 0) and (mf >= 2 * pm):
    # CO3 only
    carbonate = 60 * pm
elif (pm > 0) and (mf > pm) and (mf < 2 * pm):
    # Mixed OH + CO3
    hydroxide = 340 * (2 * pm - mf)
    carbonate = 120 * (mf - pm)
elif (pm == 0) and (mf > 0):
    # HCO3 only
    bicarbonate = 61 * mf

# === 🔹 RESULTS DISPLAY ===
st.markdown("### 🧾 Alkalinity Species Breakdown")

col1, col2, col3 = st.columns(3)
col1.metric("Hydroxide (OH⁻)", f"{hydroxide:.2f} mg/L")
col2.metric("Carbonate (CO₃²⁻)", f"{carbonate:.2f} mg/L")
col3.metric("Bicarbonate (HCO₃⁻)", f"{bicarbonate:.2f} mg/L")

# === 🔹 CONTAMINATION ADVISORY ===
st.markdown("### ⚠️ Contamination Advisory")

if calcium > 400:
    st.warning("🔸 High calcium may indicate cement contamination or gypsum interaction.")

if hardness > 500 and calcium < 100:
    st.info("🔹 Elevated hardness with low calcium may reflect excess soda ash or carbonate scaling.")

if bicarbonate > 150:
    st.error("🔺 High bicarbonate detected – risk of gas-cut mud or CO₂ contamination.")

if hydroxide > 500:
    st.warning("🔸 Hydroxide is very high – risk of emulsion instability or over-treatment with caustic.")

# === 🔹 EXPORT RESULTS TO CSV ===
st.markdown("### 📤 Export Results")

data = {
    "Parameter": ["Pm", "Pf", "Mf", "Calcium", "Hardness", "Hydroxide", "Carbonate", "Bicarbonate"],
    "Value": [pm, pf, mf, calcium, hardness, hydroxide, carbonate, bicarbonate]
}

df = pd.DataFrame(data)

st.download_button(
    label="📥 Download Results as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="alkalinity_report.csv",
    mime="text/csv"
)

# === ✅ END OF APP ===
