import streamlit as st

st.set_page_config(page_title="🧪 Alkalinity Contamination Calculator", layout="centered")

st.title("🧪 Alkalinity Contamination Calculator")
st.markdown("This calculator determines hydroxide, carbonate, and bicarbonate concentrations in drilling fluid and flags possible contamination events.")

# Inputs
st.header("🔢 Input Mud Check Values")
pm = st.number_input("Phenolphthalein Alkalinity (Pm)", min_value=0.0, step=0.1)
pf = st.number_input("Filtrate Alkalinity (Pf)", min_value=0.0, step=0.1)
mf = st.number_input("M Alkalinity (Mf)", min_value=0.0, step=0.1)
calcium = st.number_input("Calcium (mg/L)", min_value=0.0, step=10.0)

# Calculation logic
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

# Flag contamination
contamination = (carbonate > 100) or (bicarbonate > 100) or (calcium > 1000)

# Outputs
st.header("📊 Alkalinity Species Results")
st.write(f"**Hydroxide (mg/L):** {round(hydroxide, 2)}")
st.write(f"**Carbonate (mg/L):** {round(carbonate, 2)}")
st.write(f"**Bicarbonate (mg/L):** {round(bicarbonate, 2)}")
st.write(f"**Calcium (mg/L):** {round(calcium, 2)}")

if contamination:
    st.error("🚨 Contamination Detected: Elevated carbonate, bicarbonate, or calcium levels.")
else:
    st.success("✅ No contamination flagged based on input parameters.")
