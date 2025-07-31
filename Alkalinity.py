import streamlit as st

st.set_page_config(page_title="🧪 Alkalinity Contamination Calculator", layout="centered")
st.title("🧪 Alkalinity Contamination Calculator")

st.markdown("""
This tool calculates hydroxide, carbonate, and bicarbonate concentrations in drilling fluid and recommends treatment actions based on alkalinity, calcium, and hardness.
""")

st.header("🔢 Input Mud Check Values")

# Input function
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

# Alkalinity Species Calculations
hydroxide = carbonate = bicarbonate = 0.0

if pm == 0:
    bicarbonate = 122.5 * mf
    zone = "HCO₃⁻ only"
elif pm == pf:
    hydroxide = 34 * pf
    zone = "OH⁻ only"
elif pm > pf:
    hydroxide = 34 * (pm - pf)
    carbonate = 60 * (2 * pf)
    zone = "OH⁻ + CO₃²⁻"
else:
    carbonate = 60 * pf
    bicarbonate = 122.5 * (mf - pf)
    zone = "CO₃²⁻ + HCO₃⁻"

# Treatment Recommendations
lime_ppb = round(0.7 * hydroxide / 100, 2) if hydroxide > 0 else 0
caustic_ppb = round(0.54 * hydroxide / 100, 2) if hydroxide > 0 else 0

# If no OH⁻, treat carbonate with caustic
if hydroxide == 0 and carbonate > 0:
    caustic_ppb = round(0.54 * carbonate / 100, 2)

# Soda Ash & Calcium Chloride logic
soda_ash_ppb = round((hardness - calcium) / 10, 3)
calcium_ppb = round((calcium - hardness) / 10, 3)

# Output
st.header("📊 Alkalinity Species Results")
st.write(f"- **Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"- **Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"- **Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"- **Calcium (mg/L):** {round(calcium, 2)}")
st.write(f"- **Hardness (mg/L):** {round(hardness, 2)}")
st.markdown(f"**Contamination Zone:** :orange[{zone}]")

st.header("🧪 Suggested Treatments (ppb)")
st.write(f"- **Lime:** {lime_ppb}")
st.write(f"- **Caustic Soda:** {caustic_ppb}")
st.write(f"- **Soda Ash (balance):** {soda_ash_ppb}")
st.write(f"- **Calcium Chloride (balance):** {calcium_ppb}")

# Advisory
st.header("🛡️ Advisory")
flags = []
if carbonate > 100: flags.append("High Carbonate")
if bicarbonate > 100: flags.append("High Bicarbonate")
if hydroxide > 50: flags.append("Excess Hydroxide")
if calcium > 1000: flags.append("High Calcium")
if hardness < 500: flags.append("Low Hardness")

if flags:
    st.error("⚠️ Advisory: " + ", ".join(flags))
else:
    st.success("✅ System appears balanced — no contamination flagged.")

st.caption("🔁 *To reset calculator, refresh the page.*")
