import streamlit as st

st.set_page_config(page_title="🧪 Alkalinity Contamination Calculator", layout="centered")

st.title("🧪 Alkalinity Contamination Calculator")
st.markdown("This tool calculates hydroxide, carbonate, and bicarbonate contamination, evaluates calcium and hardness balance, and recommends treatment dosages.")

st.header("🔢 Input Mud Check Values")

# Safe input conversion
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

# ------------------------
# Alkalinity Speciation
# ------------------------
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

# ------------------------
# Contamination Advisory
# ------------------------
contamination_flag = (
    carbonate > 100 or
    bicarbonate > 100 or
    calcium > 1000 or
    hardness < 500
)

# ------------------------
# Base Treatment Doses
# ------------------------
lime_ppb = round((carbonate / 1200) * 3, 2) if carbonate > 0 else 0  # 3:1 Lime to Caustic
caustic_ppb = round(lime_ppb / 3, 2) if lime_ppb > 0 else round(hydroxide / 340, 2)
soda_ash_ppb = round((bicarbonate / 1220) * 1.5, 2) if bicarbonate > 0 else 0

# ------------------------
# Hardness / Calcium Adjustments
# ------------------------
excess_soda_ash_ppb = round((500 - hardness) / 540, 2) if hardness < 500 else 0
calcium_reduction_ppb = round((calcium - 400) / 10650, 2) if calcium > 400 else 0

# ------------------------
# Final Treatment Totals
# ------------------------
total_soda_ash_ppb = round(soda_ash_ppb + excess_soda_ash_ppb, 2)
total_calcium_chloride_ppb = calcium_reduction_ppb
total_lime_ppb = lime_ppb
total_caustic_ppb = caustic_ppb

# ------------------------
# Output Section
# ------------------------
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"**Hardness (mg/L):** {round(hardness, 2)}")

st.header("🧪 Suggested Treatments (lb/bbl)")
st.write(f"**Lime:** {total_lime_ppb}")
st.write(f"**Caustic Soda:** {total_caustic_ppb}")
st.write(f"**Soda Ash:** {total_soda_ash_ppb}")
st.write(f"**Calcium Chloride (CaCl₂):** {total_calcium_chloride_ppb}")

# Advisory
st.header("🛡️ Advisory")
if contamination_flag:
    msg = "⚠️ Bicarbonate Contamination (HCO₃⁻ > 0) | Carbonate > 100 mg/L | Ca > 1000 mg/L | Hardness < 500 mg/L"
    st.error(msg)
else:
    st.success("✅ System appears balanced — no contamination flagged.")

# Optional Reset Notice
st.caption("🔁 To reset inputs, refresh the page.")