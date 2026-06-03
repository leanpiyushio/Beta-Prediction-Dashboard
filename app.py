import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="SME Beta Prediction",
    page_icon="180.png",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #040f0c;
    color: #e8f5f0;
}

section[data-testid="stMain"] > div {
    background: transparent;
}

.block-container {
    padding: 3rem 3rem 4rem;
    max-width: 1440px;
}

.hero-wrap {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 20px;
    margin-bottom: 28px;
}

.hero-left {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 44px 48px 40px;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 100px;
    line-height: 1.03;
    font-weight: 400;
    color: #ffffff;
    letter-spacing: -1.5px;
    margin: 0 0 20px;
}

.hero-title em {
    font-style: italic;
    color: #34d399;
}

.hero-sub {
    font-size: 20px;
    line-height: 1.75;
    color: #7aa896;
    max-width: 600px;
    margin: 0 0 30px;
}

.chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.chip {
    font-size: 12.5px;
    font-weight: 500;
    color: #a7f3d0;
    background: rgba(52,211,153,0.07);
    border: 1px solid rgba(52,211,153,0.16);
    border-radius: 8px;
    padding: 7px 14px;
}

.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 36px 32px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    box-sizing: border-box;
}


.stat-block { flex: 1; }

.stat-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 10px;
}

.stat-value {
    font-family: 'DM Serif Display', serif;
    font-size: 76px;
    font-weight: 400;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 6px;
}

.stat-sub {
    font-size: 13px;
    color: #7aa896;
}

.stat-divider {
    height: 1px;
    background: rgba(255,255,255,0.07);
    margin: 28px 0;
    flex-shrink: 0;
}

.stat-model-name {
    font-family: 'DM Serif Display', serif;
    font-size: 38px;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 6px;
}

/* ── SECTION HEADINGS via st.subheader ── */
div[data-testid="stHeadingWithActionElements"] h3 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 42px !important;
    font-weight: 400 !important;
    color: #ffffff !important;
    letter-spacing: -0.5px !important;
    margin: 0 0 20px 0 !important;
    line-height: 1.1 !important;
    padding: 0 !important;
}

div[data-testid="stHeadingWithActionElements"] a {
    display: none !important;
}

/* ── TOP-ALIGN COLUMNS ── */
div[data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
}

/* ── LABELS ── */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
    color: #5e9980 !important;
    margin-bottom: 2px !important;
}

/* ── NUMBER INPUT ── */
div[data-testid="stNumberInput"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

div[data-testid="stNumberInput"] > div:focus-within {
    border-color: rgba(52,211,153,0.45) !important;
    box-shadow: 0 0 0 3px rgba(52,211,153,0.06) !important;
}

div[data-testid="stNumberInput"] input {
    background: transparent !important;
    color: #e8f5f0 !important;
    font-size: 17px !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    border: none !important;
    padding: 14px 16px !important;
}

div[data-testid="stNumberInput"] button {
    display: none !important;
}

div[data-testid="stTextInput"] label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
    color: #5e9980 !important;
}

div[data-testid="stTextInput"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
}

/* ── TEXT INPUT ── */
div[data-testid="stTextInput"] input {
    background: transparent !important;
    color: #e8f5f0 !important;
    font-size: 17px !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    border: none !important;
    padding: 14px 16px !important;
}

div[data-testid="stTextInput"] > div:focus-within {
    border-color: rgba(52,211,153,0.45) !important;
    box-shadow: 0 0 0 3px rgba(52,211,153,0.06) !important;
}

/* ── SELECT BOX ── */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
    max-height: 44px !important;
}

div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: rgba(52,211,153,0.45) !important;
}

div[data-testid="stSelectbox"] span,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    color: #e8f5f0 !important;
    font-size: 15px !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    min-height: 44px !important;
}

div[data-testid="stSelectbox"] svg {
    fill: #4ade80 !important;
}

ul[data-baseweb="menu"],
div[data-baseweb="popover"] {
    background: #0d2820 !important;
    border: 1px solid rgba(52,211,153,0.18) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

li[role="option"] {
    color: #e8f5f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}

li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background: rgba(52,211,153,0.1) !important;
    color: #a7f3d0 !important;
}

/* ── SUBMIT BUTTON ── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 56px !important;
    background: #059669 !important;
    border: none !important;
    border-radius: 14px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px !important;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 0 0 0 rgba(52,211,153,0) !important;
}

div[data-testid="stButton"] > button:hover {
    background: #047857 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 0 32px 8px rgba(52,211,153,0.30) !important;
}

div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 0 16px 4px rgba(52,211,153,0.18) !important;
}

/* ── RESULT CARD ── */
.result-outer {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 52px 36px 44px;
    margin-top: 28px;
    text-align: center;
}

.result-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #5e9980;
    margin-bottom: 16px;
}

.result-number {
    font-family: 'DM Serif Display', serif;
    font-size: 96px;
    font-weight: 400;
    color: #34d399;
    line-height: 1;
    margin-bottom: 10px;
}

.result-desc {
    font-size: 14px;
    color: #5e9980;
}

.risk-pill {
    display: inline-block;
    margin-top: 24px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 10px 26px;
    border-radius: 100px;
}

.risk-low  { background: rgba(34,197,94,0.10);  border: 1px solid rgba(34,197,94,0.25);  color: #86efac; }
.risk-med  { background: rgba(251,191,36,0.10);  border: 1px solid rgba(251,191,36,0.25);  color: #fde68a; }
.risk-high { background: rgba(239,68,68,0.10);   border: 1px solid rgba(239,68,68,0.25);   color: #fca5a5; }

#MainMenu, footer, header { visibility: hidden; }

</style>
""", unsafe_allow_html=True)

# ─── HERO ───────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-left">
    <h1 class="hero-title">SME<br> Beta Prediction</em> Dashboard</h1>
    <p class="hero-sub">
      Predict unlevered beta using ensemble machine learning models<br>trained on
      financial structure, profitability, operational efficiency, and working
      capital dynamics across Indian SMEs.
    </p>
    <div class="chips">
      <span class="chip">100+ Companies Benchmarked</span>
      <span class="chip">10+ Regression Models Evaluated</span>
      <span class="chip">Operational + Financial Indicators</span>
    </div>
  </div>
  <div class="stat-card">
    <div class="stat-block">
      <div class="stat-label">Model Performance</div>
      <div class="stat-value">0.69</div>
      <div class="stat-sub">Test R² Score</div>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-block">
      <div class="stat-label">Best Model</div>
      <div class="stat-model-name">XGBoost</div>
      <div class="stat-sub">Top performing ensemble</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# INPUT COLUMNS
company_name = st.text_input("Company Name", placeholder="e.g. Amul Industries")

left_col, right_col = st.columns(2, gap="large")
left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.subheader("Financial Metrics")
    de_ratio          = st.number_input("D/E Ratio",             min_value=0.000, value=0.500,  step=0.001, format="%.3f")
    roce              = st.number_input("ROCE (%)",                               value=0.150,  step=0.001, format="%.3f")
    net_profit_margin = st.number_input("Net Profit Margin (%)",                  value=0.080,  step=0.001, format="%.3f")
    ebitda_margin     = st.number_input("EBITDA Margin (%)",                      value=0.120,  step=0.001, format="%.3f")
    ln_revenue        = st.number_input("ln(Revenue)",                            value=6.000,  step=0.001, format="%.3f")

with right_col:
    st.subheader("Operational Metrics")
    inventory_days  = st.number_input("Inventory Days",  min_value=0.000, value=50.000, step=0.001, format="%.3f")
    receivable_days = st.number_input("Receivable Days", min_value=0.000, value=40.000, step=0.001, format="%.3f")
    industry        = st.selectbox("Industry", ["FMCG","Edible Oils","Food Ingredients","Beverage","Packaging","Staples & Rice","Logistics"])
    export_presence = st.selectbox("Export Presence", ["No", "Yes"])

# ─── CENTRED BUTTON ─────────────────────────────────────────
st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    predict_button = st.button("Generate Risk Assessment →")

# ─── RESULT ─────────────────────────────────────────────────
if predict_button:
    try:
        model = joblib.load("xgb_unlevered_beta_model.pkl")

        input_df = pd.DataFrame([{
            'D/E Ratio':                 de_ratio,
            'ROCE(%)':                   roce,
            'Recievable Days':           receivable_days,
            'Net Profit Margin':         net_profit_margin,
            'Inventory Days':            inventory_days,
            'Export Presence':           1 if export_presence == "Yes" else 0,
            'Industry_FMCG':             1 if industry == "FMCG" else 0,
            'Industry_Edible Oils':      1 if industry == "Edible Oils" else 0,
            'ln(Revenue)':               ln_revenue,
            'Industry_Food Ingredients': 1 if industry == "Food Ingredients" else 0,
            'Industry_Beverage':         1 if industry == "Beverage" else 0,
            'Industry_Packaging':        1 if industry == "Packaging" else 0,
            'Industry_Logistics':        1 if industry == "Logistics" else 0,
            'EBITDA Margin(%)':          ebitda_margin,
            'Industry_Staples & Rice':   1 if industry == "Staples & Rice" else 0
        }])

        prediction = model.predict(input_df)[0]

        if prediction < 0.7:
            risk_class, risk_label = "risk-low", "Low Systematic Risk"
        elif prediction < 1.0:
            risk_class, risk_label = "risk-med", "Moderate Systematic Risk"
        else:
            risk_class, risk_label = "risk-high", "High Systematic Risk"

        st.markdown(f"""
        <div class="result-outer">
          <div class="result-eyebrow">{"Predicted Unlevered Beta for " + company_name.upper() if company_name else "Predicted Unlevered Beta"}</div>
          <div class="result-number">{prediction:.3f}</div>
          <div class="result-desc">{industry} &nbsp;·&nbsp; {"Export" if export_presence == "Yes" else "Domestic"} &nbsp;
          <div><span class="risk-pill {risk_class}">{risk_label}</span></div>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("Model file not found. Place `xgb_unlevered_beta_model.pkl` in the same directory as app.py.")

# python -m streamlit run app.py
