import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from modules.database import (
    init_db, add_transaction, get_transactions, delete_transaction,
    set_budget, get_budgets
)
from modules.categorization import predict_category
from modules.forecasting import forecast_next_month
from modules.anomaly_detection import detect_anomalies
from modules.insights import generate_insights
from modules.report_generator import create_monthly_report

st.set_page_config(
    page_title="FINOVA AI | Smart Finance",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)
init_db()

# -------------------------------------------------------------------
# Theme system: selected in the sidebar and applied across the app.
# -------------------------------------------------------------------
if "finova_theme" not in st.session_state:
    st.session_state.finova_theme = "Dark"

theme_choice = st.session_state.finova_theme
if theme_choice == "Light":
    C = {
        "bg": "#f4f7fc", "surface": "#ffffff", "surface2": "#edf2fa",
        "text": "#17243a", "muted": "#64748b", "border": "#dce5f1",
        "accent": "#4169e1", "accent2": "#7658d6", "sidebar": "#ffffff",
        "plot": "plotly_white", "shadow": "0 10px 30px rgba(28, 48, 82, .07)"
    }
else:
    C = {
        "bg": "#08111f", "surface": "#111e31", "surface2": "#172840",
        "text": "#edf4ff", "muted": "#9aabc2", "border": "#263a55",
        "accent": "#78a6ff", "accent2": "#a78bfa", "sidebar": "#0c1829",
        "plot": "plotly_dark", "shadow": "0 12px 34px rgba(0, 0, 0, .22)"
    }

st.markdown(f"""
<style>
:root {{
 --fin-bg:{C['bg']}; --fin-surface:{C['surface']}; --fin-surface2:{C['surface2']};
 --fin-text:{C['text']}; --fin-muted:{C['muted']}; --fin-border:{C['border']};
 --fin-accent:{C['accent']}; --fin-accent2:{C['accent2']};
}}
.stApp, [data-testid="stAppViewContainer"] {{background:var(--fin-bg); color:var(--fin-text);}}
[data-testid="stHeader"] {{background:transparent;}}
[data-testid="stSidebar"] {{background:{C['sidebar']}; border-right:1px solid var(--fin-border);}}
[data-testid="stSidebar"] > div:first-child {{padding-top:1.1rem;}}
.block-container {{padding-top:2rem; padding-bottom:3rem; max-width:1500px;}}
h1,h2,h3,h4,p,label,span {{color:var(--fin-text);}}
small,.stCaption {{color:var(--fin-muted)!important;}}
div[data-testid="stMetric"] {{
 background:var(--fin-surface); border:1px solid var(--fin-border);
 padding:18px 20px; border-radius:18px; box-shadow:{C['shadow']};
}}
div[data-testid="stMetricLabel"] p {{color:var(--fin-muted)!important; font-weight:600;}}
div[data-testid="stMetricValue"] {{color:var(--fin-text)!important;}}
div[data-testid="stForm"], div[data-testid="stExpander"], div[data-testid="stDataFrame"],
div[data-testid="stAlert"] {{border-radius:16px;}}
div[data-testid="stForm"] {{background:var(--fin-surface); border:1px solid var(--fin-border); padding:18px;}}
.stTextInput input,.stNumberInput input,.stDateInput input,
.stSelectbox [data-baseweb="select"],.stTextArea textarea {{
 background:var(--fin-surface)!important; color:var(--fin-text)!important;
 border-color:var(--fin-border)!important; border-radius:11px!important;
}}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button {{
 border:1px solid var(--fin-accent)!important; border-radius:12px!important;
 color:var(--fin-accent)!important; background:transparent!important;
 font-weight:650; padding:.55rem 1rem; transition:all .18s ease;
}}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover {{
 background:var(--fin-accent)!important; color:white!important;
 transform:translateY(-2px); box-shadow:0 7px 18px rgba(65,105,225,.2);
}}
[data-testid="stSidebar"] .stRadio label {{padding:7px 10px; border-radius:10px;}}
hr {{border-color:var(--fin-border)!important;}}
.finova-hero {{
 background:linear-gradient(120deg,{C['surface']} 0%,{C['surface2']} 100%);
 border:1px solid var(--fin-border); border-radius:24px; padding:26px 28px;
 box-shadow:{C['shadow']}; margin-bottom:22px;
}}
.finova-eyebrow {{font-size:12px; letter-spacing:2px; font-weight:800; color:var(--fin-accent); text-transform:uppercase;}}
.finova-title {{font-size:32px; font-weight:850; letter-spacing:-1px; margin:5px 0 4px; color:var(--fin-text);}}
.finova-sub {{color:var(--fin-muted); font-size:14px;}}
.finova-card {{
 background:var(--fin-surface); border:1px solid var(--fin-border);
 border-radius:18px; padding:18px 20px; box-shadow:{C['shadow']}; height:100%;
}}
.finova-card-label {{font-size:12px; color:var(--fin-muted); font-weight:700; text-transform:uppercase; letter-spacing:1px;}}
.finova-card-value {{font-size:25px; color:var(--fin-text); font-weight:800; margin-top:8px;}}
.finova-card-note {{font-size:12px; color:var(--fin-muted); margin-top:5px;}}
.finova-brand {{font-size:22px; font-weight:900; letter-spacing:-.7px; color:var(--fin-text);}}
.finova-brand span {{color:var(--fin-accent);}}
.finova-pill {{display:inline-block; padding:5px 10px; border-radius:99px; background:var(--fin-surface2); color:var(--fin-accent); font-size:11px; font-weight:800;}}
</style>
""", unsafe_allow_html=True)

# Sidebar: navigation, theme control and app information.
with st.sidebar:
    st.markdown('<div class="finova-brand">💠 FINOVA<span> AI</span></div>', unsafe_allow_html=True)
    st.caption("SMART PERSONAL FINANCE")
    st.divider()
    st.markdown("**WORKSPACE**")
    menu = st.radio(
        "Navigation",
        ["Dashboard", "Add Transaction", "Transactions", "AI Categorization",
         "Forecasting", "Anomaly Detection", "Budgets", "AI Insights", "Reports",
         "Information"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**APPEARANCE**")
    selected_theme = st.radio(
        "Choose interface theme",
        ["Dark", "Light"],
        index=0 if st.session_state.finova_theme == "Dark" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    if selected_theme != st.session_state.finova_theme:
        st.session_state.finova_theme = selected_theme
        st.rerun()
    st.caption(f"{'☀️ Light' if selected_theme == 'Light' else '🌙 Dark'} theme is active across the entire app.")
    st.divider()
    st.caption("FINOVA AI  •  Personal finance workspace")
    st.caption("Your records are stored in the local SQLite database.")

df = get_transactions()
if not df.empty:
    df["date"] = pd.to_datetime(df["date"]).dt.date
    income = float(df.loc[df.transaction_type == "Income", "amount"].sum())
    expenses = float(df.loc[df.transaction_type == "Expense", "amount"].sum())
else:
    income = expenses = 0.0
balance = income - expenses

def hero(kicker, title, subtitle):
    st.markdown(
        f'<div class="finova-hero"><div class="finova-eyebrow">{kicker}</div>'
        f'<div class="finova-title">{title}</div><div class="finova-sub">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )

def money_card(label, value, note, icon):
    st.markdown(
        f'<div class="finova-card"><div class="finova-card-label">{icon} &nbsp; {label}</div>'
        f'<div class="finova-card-value">₹{value:,.2f}</div>'
        f'<div class="finova-card-note">{note}</div></div>',
        unsafe_allow_html=True,
    )

if menu == "Dashboard":
    hero("YOUR MONEY, MADE CLEAR", "Financial dashboard", "A smarter view of your income, spending and monthly activity.")
    a, b, c = st.columns(3)
    with a: money_card("Total income", income, "All recorded income", "↗")
    with b: money_card("Total expenses", expenses, "All recorded expenses", "↘")
    with c: money_card("Available balance", balance, "Income minus expenses", "◈")
    st.write("")
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("### Spending breakdown")
        exp_df = df[df.transaction_type == "Expense"] if not df.empty else pd.DataFrame()
        if not exp_df.empty:
            by_cat = exp_df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
            fig = px.pie(by_cat, names="category", values="amount", hole=.62,
                         color_discrete_sequence=px.colors.qualitative.Pastel,
                         template=C["plot"])
            fig.update_layout(margin=dict(t=15,b=15,l=5,r=5), legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Your category chart will appear after you add expense transactions.")
    with right:
        st.markdown("### Spending activity")
        if not exp_df.empty:
            trend = exp_df.groupby("date", as_index=False)["amount"].sum()
            fig = px.area(trend, x="date", y="amount", template=C["plot"])
            fig.update_traces(line=dict(color=C["accent"], width=3), fillcolor="rgba(100,145,240,.15)")
            fig.update_layout(margin=dict(t=15,b=15,l=5,r=5), xaxis_title="", yaxis_title="Amount (₹)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Daily activity will appear here when expenses are available.")
    st.markdown("### Recent transactions")
    if not df.empty:
        st.dataframe(df.sort_values("date", ascending=False).head(8), use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet. Select **Add Transaction** from the left menu to get started.")

elif menu == "Add Transaction":
    hero("RECORD ACTIVITY", "Add a transaction", "Keep your financial activity organised in one place.")
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tx_date = st.date_input("Date", value=date.today())
            description = st.text_input("Description", placeholder="e.g. Grocery shopping")
            amount = st.number_input("Amount (₹)", min_value=0.01, step=10.0)
        with col2:
            tx_type = st.selectbox("Type", ["Expense", "Income"])
            categories = ["Food", "Travel", "Shopping", "Entertainment", "Education",
                          "Healthcare", "Utilities", "Rent", "Groceries", "Personal Care", "Other"]
            suggested = predict_category(description) if description.strip() else "Other"
            category = st.selectbox("Category", categories, index=categories.index(suggested) if suggested in categories else len(categories)-1)
            payment = st.selectbox("Payment method", ["UPI", "Cash", "Card", "Net Banking", "Other"])
        submitted = st.form_submit_button("＋ Save transaction", use_container_width=True)
        if submitted:
            if not description.strip():
                st.error("Please enter a transaction description.")
            else:
                add_transaction(str(tx_date), description.strip(), float(amount), tx_type, category, payment)
                st.success("Transaction saved successfully.")
                st.rerun()

elif menu == "Transactions":
    hero("YOUR RECORDS", "Transaction history", "Search, review, export or remove recorded transactions.")
    if df.empty:
        st.info("No transactions available.")
    else:
        q = st.text_input("⌕ Search description, category or payment method", placeholder="Type to filter transactions...")
        show = df.copy()
        if q:
            show = show[show.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)]
        st.dataframe(show.sort_values("date", ascending=False), use_container_width=True, hide_index=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            ids = show["transaction_id"].tolist()
            if ids:
                selected = st.selectbox("Transaction ID to delete", ids)
                if st.button("Delete selected transaction"):
                    delete_transaction(int(selected))
                    st.success("Transaction deleted.")
                    st.rerun()
        with col2:
            st.download_button("↓ Export filtered CSV", show.to_csv(index=False), "finova_transactions.csv", "text/csv")

elif menu == "AI Categorization":
    hero("AI ASSIST", "Expense categorization", "Get a suggested category from a transaction description.")
    desc = st.text_input("Transaction description", placeholder="e.g. Cab ride to college")
    if st.button("✦ Predict category"):
        if desc.strip():
            st.success(f"Suggested category: **{predict_category(desc)}**")
        else:
            st.warning("Enter a description first.")
    st.caption("This starter version uses a transparent keyword-based baseline. The optional ML training script is included in the project.")

elif menu == "Forecasting":
    hero("LOOK AHEAD", "Monthly expense forecast", "A simple trend-based estimate using your recorded monthly expenses.")
    expenses_df = df[df.transaction_type == "Expense"].copy() if not df.empty else pd.DataFrame()
    result = forecast_next_month(expenses_df)
    if result is None:
        st.info("Add expenses across at least two different months to calculate a basic trend forecast.")
    else:
        money_card("Estimated next-month expenses", float(result), "Trend estimate based on recorded monthly totals", "⌁")
        st.caption("This is an informational estimate, not financial advice.")

elif menu == "Anomaly Detection":
    hero("SPENDING CHECK", "Unusual spending review", "Highlight transactions that may deserve a closer look.")
    expenses_df = df[df.transaction_type == "Expense"].copy() if not df.empty else pd.DataFrame()
    flagged = detect_anomalies(expenses_df)
    if flagged is None or flagged.empty:
        st.info("Add at least five expense transactions to enable anomaly screening.")
    else:
        st.dataframe(flagged, use_container_width=True, hide_index=True)
        st.caption("Flags are prompts for human review, not proof of fraud.")

elif menu == "Budgets":
    hero("STAY ON TRACK", "Monthly budgets", "Set category limits and keep an eye on your spending.")
    with st.form("budget_form"):
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Entertainment", "Education", "Healthcare", "Utilities", "Rent", "Groceries", "Personal Care", "Other"])
        limit = st.number_input("Monthly limit (₹)", min_value=1.0, step=100.0)
        save = st.form_submit_button("＋ Save budget")
        if save:
            set_budget(category, float(limit), date.today().month, date.today().year)
            st.success("Budget saved.")
    budgets = get_budgets(date.today().month, date.today().year)
    if budgets:
        exp = df[(df.transaction_type == "Expense") & (pd.to_datetime(df.date).dt.month == date.today().month) & (pd.to_datetime(df.date).dt.year == date.today().year)] if not df.empty else pd.DataFrame()
        spent = exp.groupby("category")["amount"].sum().to_dict() if not exp.empty else {}
        for item in budgets:
            used = float(spent.get(item["category"], 0))
            cap = float(item["monthly_limit"])
            st.markdown(f"**{item['category']}**")
            st.caption(f"₹{used:,.2f} used of ₹{cap:,.2f}")
            st.progress(min(used / cap, 1.0))
            if used > cap:
                st.warning(f"{item['category']} budget exceeded.")

elif menu == "AI Insights":
    hero("PERSONAL FINANCE COACH", "AI insights", "Understand patterns in your recorded financial activity.")
    insights = generate_insights(df)
    if insights:
        for item in insights:
            st.info(item)
    else:
        st.info("Add more transactions to generate useful insights.")

elif menu == "Reports":
    hero("MONTHLY SUMMARY", "Financial reports", "Generate a PDF summary for a selected month.")
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox("Month", list(range(1, 13)), index=date.today().month-1)
    with col2:
        year = st.number_input("Year", min_value=2020, max_value=2100, value=date.today().year)
    if st.button("✦ Generate PDF report"):
        path = create_monthly_report(df, int(month), int(year))
        if path:
            with open(path, "rb") as f:
                st.download_button("↓ Download PDF report", f.read(), f"FINOVA_{year}_{month:02d}_report.pdf", "application/pdf")
        else:
            st.warning("No transactions found for this month.")

elif menu == "Information":
    hero("ABOUT THE WORKSPACE", "Meet FINOVA AI", "A clear, organised space to understand everyday personal finances.")
    st.markdown("""
    <div class="finova-card">
      <div class="finova-eyebrow">WHAT YOU CAN DO</div>
      <h3>One workspace. Better money awareness.</h3>
      <p style="color:var(--fin-muted)">FINOVA AI brings transaction tracking, spending insights and simple forecasting into one dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    cards = st.columns(3)
    features = [
        ("01", "Track transactions", "Record income and expenses with date, category and payment method."),
        ("02", "Explore patterns", "Review category charts, trends and unusual-spending prompts."),
        ("03", "Plan ahead", "Set monthly category budgets and create PDF reports."),
        ("04", "AI assistance", "Get keyword-based category suggestions and generated insights."),
        ("05", "Theme control", "Switch between Light and Dark from the left sidebar. The full interface updates."),
        ("06", "Local storage", "This starter app stores records in a local SQLite database.")
    ]
    for i, (num, title, desc) in enumerate(features):
        with cards[i % 3]:
            st.markdown(f'<div class="finova-card"><span class="finova-pill">{num}</span><h4>{title}</h4><p style="color:var(--fin-muted);font-size:13px">{desc}</p></div>', unsafe_allow_html=True)
        if i % 3 == 2 and i != len(features)-1:
            cards = st.columns(3)
    st.write("")
    st.markdown("### Important notes")
    st.warning("FINOVA AI is a project starter, not a banking service. It does not connect to bank accounts. Forecasts and anomaly flags are basic informational tools and should be reviewed by a person.")
    st.caption("For a demo, use sample data and keep personal financial information private.")
