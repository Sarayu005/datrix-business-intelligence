import os
import html
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# DATRIX — BUSINESS INTELLIGENCE ASSISTANT
# ============================================================

API_URL = os.getenv("SALESIQ_API_URL", "http://127.0.0.1:8000")
ORANGE = "#F97316"

st.set_page_config(
    page_title="Datrix | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PREMIUM STYLING  (black + orange, blended accents)
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700;8..60,800&display=swap');

:root {
    --ink: #0F0F10;
    --ink-2: #1B1816;
    --ink-3: #2A2320;
    --orange: #F97316;
    --orange-deep: #EA580C;
    --orange-soft: #FFEDD5;
    --cream: #F6F3EE;
    --line: #E8E2DA;
    --muted: #78716C;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- App background: cream with soft orange glow ---------- */
.stApp {
    background:
        radial-gradient(900px 420px at 92% -5%, rgba(249,115,22,0.13), transparent 60%),
        radial-gradient(700px 380px at -5% 35%, rgba(23,23,23,0.05), transparent 60%),
        var(--cream);
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    font-family: 'Source Serif 4', Georgia, serif !important;
    letter-spacing: -0.5px;
    color: var(--ink);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background:
        radial-gradient(400px 260px at 0% 0%, rgba(249,115,22,0.22), transparent 65%),
        linear-gradient(180deg, #0F0F10 0%, #1B1612 100%);
    border-right: 1px solid #2E2723;
}

[data-testid="stSidebar"] * {
    color: #F5F5F5;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #D4D4D4;
}

[data-testid="stSidebar"] hr {
    border-color: #2F2824;
}

/* Sidebar navigation radio -> pill buttons */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 6px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 9px 12px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(249,115,22,0.14);
    border-color: rgba(249,115,22,0.45);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(100deg, #F97316 0%, #EA580C 100%);
    border-color: #F97316;
    box-shadow: 0 6px 18px rgba(249,115,22,0.35);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * {
    color: #FFFFFF !important;
    font-weight: 700;
}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(520px 260px at 95% 0%, rgba(249,115,22,0.55), transparent 65%),
        radial-gradient(380px 220px at 60% 120%, rgba(234,88,12,0.30), transparent 70%),
        linear-gradient(115deg, #0F0F10 0%, #1F1916 60%, #3A1A0A 100%);
    border: 1px solid #3A2F28;
    border-radius: 20px;
    padding: 34px 36px;
    margin-bottom: 26px;
    box-shadow: 0 14px 40px rgba(15,15,16,0.22);
}

.hero::after {
    content: "";
    position: absolute;
    right: -60px;
    top: -60px;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    border: 1px solid rgba(253,186,116,0.25);
    box-shadow: 0 0 0 36px rgba(253,186,116,0.05),
                0 0 0 78px rgba(253,186,116,0.03);
}

.hero-label {
    display: inline-block;
    color: #FDBA74;
    background: rgba(249,115,22,0.14);
    border: 1px solid rgba(249,115,22,0.35);
    border-radius: 999px;
    padding: 5px 12px;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
}

.hero-title {
    color: white;
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 40px;
    font-weight: 800;
    margin: 14px 0 6px 0;
    line-height: 1.15;
}

.hero-title span {
    background: linear-gradient(90deg, #FDBA74, #F97316);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero-subtitle {
    color: #D6D3D1;
    font-size: 15px;
    max-width: 640px;
}

/* ---------- Metric cards ---------- */
.metric-card {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(180deg, #FFFFFF 0%, #FFF9F3 100%);
    padding: 22px 22px 20px 22px;
    border-radius: 16px;
    border: 1px solid var(--line);
    min-height: 140px;
    box-shadow: 0 6px 20px rgba(30, 25, 20, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 5px;
    background: linear-gradient(180deg, #F97316, #C2410C);
}

.metric-card::after {
    content: "";
    position: absolute;
    right: -30px;
    top: -30px;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(249,115,22,0.18), transparent 70%);
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 30px rgba(249,115,22,0.16);
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.3px;
}

.metric-value {
    color: var(--ink);
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
    font-variant-numeric: tabular-nums;
    font-size: 28px;
    font-weight: 800;
    margin-top: 13px;
    overflow-wrap: anywhere;
}

.metric-caption {
    display: inline-block;
    color: #9A3412;
    background: var(--orange-soft);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 600;
    margin-top: 10px;
}

/* ---------- Section headings ---------- */
.section-heading {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 21px;
    font-weight: 800;
    color: var(--ink);
    margin: 24px 0 3px 0;
    padding-left: 12px;
    border-left: 4px solid var(--orange);
}

.section-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 15px;
    padding-left: 16px;
}

/* ---------- Containers ---------- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-radius: 16px;
    border-color: var(--line);
    box-shadow: 0 6px 22px rgba(30, 25, 20, 0.045);
}

/* ---------- Buttons ---------- */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(100deg, #F97316 0%, #EA580C 100%);
    color: #FFFFFF;
    border: 1px solid #F97316;
    border-radius: 10px;
    font-weight: 700;
    min-height: 44px;
    box-shadow: 0 6px 16px rgba(249,115,22,0.25);
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(100deg, #171717 0%, #2A2320 100%);
    color: #FDBA74;
    border-color: #171717;
    transform: translateY(-1px);
    box-shadow: 0 10px 22px rgba(15,15,16,0.30);
}

/* Suggestion chips (buttons inside bordered containers) */
div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
    background: #FFF7ED;
    color: #9A3412;
    border: 1px solid #FED7AA;
    box-shadow: none;
}

div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
    background: linear-gradient(100deg, #171717 0%, #2A2320 100%);
    color: #FDBA74;
    border-color: #171717;
}

/* Keep the main submit button solid orange */
div[data-testid="stVerticalBlockBorderWrapper"] .stFormSubmitButton > button {
    background: linear-gradient(100deg, #F97316 0%, #EA580C 100%);
    color: #FFFFFF;
    border: 1px solid #F97316;
}

/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
    background: transparent;
    color: #FDBA74;
    border: 1px solid rgba(249,115,22,0.55);
    box-shadow: none;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #F97316;
    color: #FFFFFF;
    border-color: #F97316;
}

/* ---------- Inputs ---------- */
.stTextInput input {
    border-radius: 10px;
    border: 1.5px solid #E5E0D9;
    background: #FFFDFB;
    color: var(--ink);
    padding: 12px 14px;
}

.stTextInput input:focus {
    border-color: var(--orange);
    box-shadow: 0 0 0 3px rgba(249,115,22,0.18);
}

[data-testid="stForm"] {
    border: 1px dashed #FDBA74;
    border-radius: 14px;
    background: #FFFAF5;
}

/* ---------- Expanders / dataframes ---------- */
[data-testid="stExpander"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    background: #FFFFFF;
}

hr {
    border-color: #E7E2DB;
}

/* ---------- Premium AI answer card ---------- */
.ai-answer-card {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 18px;
    overflow: hidden;
    margin: 18px 0 22px 0;
    box-shadow: 0 14px 40px rgba(23, 23, 23, 0.09);
}

.ai-answer-header {
    position: relative;
    background:
        radial-gradient(360px 140px at 100% 0%, rgba(249,115,22,0.50), transparent 70%),
        linear-gradient(110deg, #0F0F10 0%, #1F1916 70%, #3A1A0A 100%);
    border-left: 5px solid #F97316;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 14px;
}

.ai-answer-icon {
    background: linear-gradient(135deg, #FDBA74, #F97316);
    color: #1A0F08;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    font-weight: 800;
    flex-shrink: 0;
    box-shadow: 0 6px 16px rgba(249,115,22,0.45);
}

.ai-answer-title {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 700;
}

.ai-answer-subtitle {
    color: #D6D3D1;
    font-size: 12px;
    margin-top: 3px;
}

.ai-answer-body {
    padding: 26px 28px 24px 28px;
    background:
        radial-gradient(500px 200px at 100% 100%, rgba(249,115,22,0.07), transparent 70%),
        #FFFFFF;
}

.ai-answer-label {
    color: var(--orange-deep);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 12px;
}

.ai-answer-text {
    color: #1C1917;
    font-size: 18px;
    line-height: 1.8;
    overflow-wrap: anywhere;
    padding-left: 16px;
    border-left: 3px solid #FDBA74;
}

.ai-insight-pill {
    display: inline-block;
    margin-top: 18px;
    background: linear-gradient(100deg, #FFF7ED, #FFEDD5);
    border: 1px solid #FED7AA;
    border-radius: 999px;
    padding: 7px 14px;
    color: #9A3412;
    font-size: 12px;
    font-weight: 700;
}

/* ---------- Evidence cards ---------- */
.evidence-section-title {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 21px;
    font-weight: 800;
    color: var(--ink);
    margin: 26px 0 4px 0;
    padding-left: 12px;
    border-left: 4px solid var(--orange);
}

.evidence-section-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 15px;
    padding-left: 16px;
}

.evidence-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(180deg, #FFFFFF 0%, #FFF9F3 100%);
    border: 1px solid var(--line);
    border-top: 4px solid #F97316;
    border-radius: 14px;
    padding: 18px 20px;
    min-height: 118px;
    margin-bottom: 14px;
    box-shadow: 0 6px 18px rgba(23, 23, 23, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.evidence-card::after {
    content: "";
    position: absolute;
    right: -26px;
    bottom: -26px;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(249,115,22,0.16), transparent 70%);
}

.evidence-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 28px rgba(249,115,22,0.15);
}

.evidence-card-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.evidence-card-value {
    color: var(--ink);
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
    font-variant-numeric: tabular-nums;
    font-size: 24px;
    font-weight: 800;
    overflow-wrap: anywhere;
}

.evidence-card-value.revenue {
    color: var(--orange-deep);
}

/* ---------- Footer ---------- */
.footer {
    color: #8A8580;
    font-size: 12px;
    text-align: center;
    padding: 24px 0 0 0;
    margin-top: 30px;
    border-top: 1px solid #E7E2DB;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# API HELPERS
# ============================================================

def api_get(path, params=None):
    try:
        response = requests.get(
            f"{API_URL}{path}",
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


def api_post(path, payload):
    try:
        response = requests.post(
            f"{API_URL}{path}",
            json=payload,
            timeout=70,
        )
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


def find_value(data, possible_keys, default=None):
    """Find a field in common API response formats."""
    if isinstance(data, dict):
        for key in possible_keys:
            if key in data and data[key] is not None:
                return data[key]

        for value in data.values():
            if isinstance(value, dict):
                found = find_value(value, possible_keys)
                if found is not None:
                    return found

    return default


def format_inr(value):
    try:
        return "₹{:,.0f}".format(float(value))
    except (TypeError, ValueError):
        return "—"


def get_monthly_records(payload):
    """Normalize monthly analytics responses for Plotly."""
    records = payload if isinstance(payload, list) else None

    if isinstance(payload, dict):
        for key in (
            "monthly_revenue",
            "monthly_data",
            "months",
            "data",
            "results",
        ):
            if isinstance(payload.get(key), list):
                records = payload[key]
                break

    if not records:
        return pd.DataFrame()

    normalized = []

    for item in records:
        if not isinstance(item, dict):
            continue

        month = find_value(
            item,
            ["month", "year_month", "period", "date", "label"],
        )
        revenue = find_value(
            item,
            ["revenue", "total_revenue", "net_revenue", "sales", "total"],
        )

        if month is not None and revenue is not None:
            try:
                normalized.append({
                    "Month": str(month),
                    "Revenue": float(revenue),
                })
            except (TypeError, ValueError):
                continue

    df = pd.DataFrame(normalized)

    if not df.empty:
        df = df.drop_duplicates(subset=["Month"]).sort_values("Month")

    return df


def metric_card(label, value, caption):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-caption">{html.escape(str(caption))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=400, title=None, x_title="Month", y_title="Revenue (₹)"):
    """Visual-only: high-contrast, readable Plotly layout for all charts."""
    layout = dict(
        height=height,
        margin=dict(l=30, r=30, t=70 if title else 30, b=55),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#1C1917", size=14),
        bargap=0.35,
        uniformtext=dict(minsize=12, mode="show"),
        xaxis=dict(
            title=dict(text=x_title, font=dict(color="#1C1917", size=14)),
            tickfont=dict(color="#1C1917", size=14),
            showgrid=False,
            showline=True,
            linecolor="#44403C",
            linewidth=1.5,
            automargin=True,
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color="#1C1917", size=14)),
            tickfont=dict(color="#1C1917", size=13),
            tickprefix="₹",
            tickformat=",.0f",
            rangemode="tozero",
            showgrid=True,
            gridcolor="#E7E5E4",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="#44403C",
            zerolinewidth=1.5,
            automargin=True,
        ),
        hoverlabel=dict(
            bgcolor="#171717",
            bordercolor="#F97316",
            font=dict(color="#FFFFFF", size=14, family="Inter"),
        ),
    )

    if title:
        layout["title"] = dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(color="#171717", size=20, family="Source Serif 4"),
        )

    fig.update_layout(**layout)
    return fig


def render_evidence(evidence):
    """Render structured evidence as cards, not raw JSON."""
    if isinstance(evidence, dict) and evidence:
        st.markdown(
            '<div class="evidence-section-title">Verified evidence</div>'
            '<div class="evidence-section-subtitle">'
            'Supporting values returned by your analytics backend.'
            '</div>',
            unsafe_allow_html=True,
        )

        items = list(evidence.items())
        columns = st.columns(min(3, len(items)), gap="medium")

        for index, (key, value) in enumerate(items):
            label = str(key).replace("_", " ").title()
            is_revenue = (
                "revenue" in str(key).lower()
                or "amount" in str(key).lower()
            )

            if is_revenue and isinstance(value, (int, float)):
                display_value = format_inr(value)
            elif value is None:
                display_value = "—"
            elif isinstance(value, (dict, list)):
                display_value = "Details available"
            else:
                display_value = str(value)

            value_class = (
                "evidence-card-value revenue"
                if is_revenue
                else "evidence-card-value"
            )

            with columns[index % len(columns)]:
                st.markdown(
                    f"""
                    <div class="evidence-card">
                        <div class="evidence-card-label">
                            {html.escape(label)}
                        </div>
                        <div class="{value_class}">
                            {html.escape(display_value)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Nested evidence is displayed as readable tables or text.
        for key, value in items:
            if isinstance(value, list) and value and all(
                isinstance(row, dict) for row in value
            ):
                st.markdown(f"**{html.escape(str(key).replace('_', ' ').title())}**")
                st.dataframe(
                    pd.DataFrame(value),
                    use_container_width=True,
                    hide_index=True,
                )
            elif isinstance(value, dict):
                st.markdown(f"**{html.escape(str(key).replace('_', ' ').title())}**")
                for nested_key, nested_value in value.items():
                    st.write(
                        f"**{str(nested_key).replace('_', ' ').title()}:** "
                        f"{nested_value}"
                    )

    elif isinstance(evidence, list) and evidence and all(
        isinstance(row, dict) for row in evidence
    ):
        st.markdown(
            '<div class="evidence-section-title">Verified evidence</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            pd.DataFrame(evidence),
            use_container_width=True,
            hide_index=True,
        )

    elif evidence is not None:
        st.markdown(
            '<div class="evidence-section-title">Supporting evidence</div>',
            unsafe_allow_html=True,
        )
        st.write(evidence)

    else:
        st.caption("No separate evidence object was returned for this answer.")



def render_ai_chart(chart_data):
    """Render readable charts only when valid chart data is provided."""
    if not isinstance(chart_data, dict):
        return

    records = chart_data.get("data", [])

    if not isinstance(records, list) or not records:
        return

    df = pd.DataFrame(records)

    if not {"label", "revenue"}.issubset(df.columns):
        return

    df["label"] = df["label"].astype(str)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df = df.dropna(subset=["revenue"])

    if df.empty:
        return

    chart_type = str(chart_data.get("type", "bar")).lower()
    title = str(chart_data.get("title", "Revenue Analysis"))

    # Line charts are suitable for time-based trends.
    # Other revenue comparisons use bar charts.
    if chart_type == "line":
        fig = px.line(
            df,
            x="label",
            y="revenue",
            markers=True,
            text="revenue",
            template="plotly_white",
        )

        fig.update_traces(
            line=dict(color="#F97316", width=3),
            marker=dict(
                size=10,
                color="#F97316",
                line=dict(color="#171717", width=1.5),
            ),
            texttemplate="₹%{y:,.0f}",
            textposition="top center",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: ₹%{y:,.2f}<extra></extra>"
            ),
        )

    else:
        fig = px.bar(
            df,
            x="label",
            y="revenue",
            text="revenue",
            template="plotly_white",
        )

        fig.update_traces(
            marker=dict(
                color="#F97316",
                line=dict(color="#171717", width=1),
            ),
            texttemplate="₹%{y:,.0f}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: ₹%{y:,.2f}<extra></extra>"
            ),
        )

    # Use the same visual style as the existing dashboard.
    style_chart(
        fig,
        height=440,
        title=title,
        x_title="Month / Category",
        y_title="Revenue (₹)",
    )

    maximum = float(df["revenue"].max())
    minimum = min(0, float(df["revenue"].min()))
    padding = max(abs(maximum) * 0.20, 1)

    fig.update_yaxes(
        range=[minimum, maximum + padding],
        tickprefix="₹",
        tickformat=",.0f",
    )

    with st.container(border=True):
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True,
            },
        )



def render_ai_response(result):
    """Show the premium answer and evidence; raw JSON stays collapsed."""
    answer = find_value(
        result,
        ["answer", "response", "message", "answer_text", "text"],
    )

    if answer is not None:
        safe_answer = html.escape(str(answer))

        st.markdown(
            f"""
            <div class="ai-answer-card">
                <div class="ai-answer-header">
                    <div class="ai-answer-icon">✦</div>
                    <div>
                        <div class="ai-answer-title">Datrix Intelligence</div>
                        <div class="ai-answer-subtitle">
                            AI-interpreted · Verified analytics
                        </div>
                    </div>
                </div>
                <div class="ai-answer-body">
                    <div class="ai-answer-label">YOUR ANSWER</div>
                    <div class="ai-answer-text">{safe_answer}</div>
                    <div class="ai-insight-pill">
                        ● Answer grounded in analytics data
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            "The API responded, but no answer field was found."
        )

    evidence = None

    if isinstance(result, dict):
        evidence = result.get("evidence")

        if evidence is None:
            evidence = find_value(
                result,
                ["data", "results", "details", "metrics"],
            )

    # Display a graph generated from verified analytics data.
    chart_data = (
        result.get("chart_data")
        if isinstance(result, dict)
        else None
    )
    render_ai_chart(chart_data)

    # Keep verified evidence cards visible.
    render_evidence(evidence)

    # The raw JSON is the only collapsible technical response panel.
    with st.expander(
        "⚙️ Developer diagnostics · Raw JSON",
        expanded=False,
    ):
        st.json(result)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:14px 0 22px 0;">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="
                    background:linear-gradient(135deg,#FDBA74,{ORANGE});
                    border-radius:12px;
                    width:46px;
                    height:46px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:23px;
                    color:#1A0F08;
                    box-shadow:0 6px 18px rgba(249,115,22,0.45);
                ">◈</div>
                <div>
                    <div style="
                        font-size:25px;
                        font-weight:800;
                        font-family:'Source Serif 4',Georgia,serif;
                    ">Datrix</div>
                    <div style="
                        font-size:10px;
                        letter-spacing:1.8px;
                        color:#A3A3A3;
                    ">INTELLIGENCE, SIMPLIFIED.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        ["Overview", "AI Assistant", "Data Quality"],
        label_visibility="visible",
    )

    st.markdown("---")
    st.markdown("**YOUR WORKSPACE**")
    st.caption("Sales analytics · 2026")

    st.markdown(
        f"<span style='color:{ORANGE};font-size:12px;'>●</span> "
        "Analytics workspace",
        unsafe_allow_html=True,
    )

    if st.button("Refresh dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-label">BUSINESS INTELLIGENCE / 2026</div>
    <div class="hero-title">Know your <span>numbers.</span></div>
    <div class="hero-subtitle">
        Your sales performance, visualized. Your business questions, answered.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD ANALYTICS
# ============================================================


@st.cache_data(ttl=30)
def load_dashboard_data():
    paths = {
        "revenue": "/analytics/revenue",
        "product": "/analytics/top-product",
        "region": "/analytics/top-region",
        "monthly": "/analytics/monthly",
        "quality": "/analytics/data-quality",
        "products": "/analytics/products",
        "regions": "/analytics/regions",
    }

    results = {}
    errors = {}

    for name, path in paths.items():
        results[name], errors[name] = api_get(path)

    return results, errors



data, errors = load_dashboard_data()

if all(errors.get(key) for key in (
    "revenue", "product", "region", "monthly"
)):
    st.error(
        "The analytics API could not be reached. "
        f"Check that FastAPI is running at {API_URL}."
    )

    with st.expander("Connection details"):
        for name, error in errors.items():
            if error:
                st.write(f"**{name}:** {error}")


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":
    revenue_data = data.get("revenue") or {}
    product_data = data.get("product") or {}
    region_data = data.get("region") or {}
    monthly_data = data.get("monthly")

    total_revenue = find_value(
        revenue_data,
        [
            "total_revenue",
            "eligible_net_revenue",
            "net_revenue",
            "revenue",
        ],
    )

    transaction_count = find_value(
        revenue_data,
        [
            "eligible_transactions",
            "transaction_count",
            "total_transactions",
            "count",
        ],
    )

    top_product = find_value(
        product_data,
        ["top_product", "product", "product_name", "name"],
    )

    product_revenue = find_value(
        product_data,
        ["revenue", "total_revenue", "product_revenue"],
    )

    top_region = find_value(
        region_data,
        ["top_region", "region", "region_name", "name"],
    )

    region_revenue = find_value(
        region_data,
        ["revenue", "total_revenue", "region_revenue"],
    )

    st.markdown(
        '<div class="section-heading">Performance at a glance</div>'
        '<div class="section-subtitle">'
        'A snapshot of your sales performance, based on the database.'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        metric_card(
            "TOTAL REVENUE",
            format_inr(total_revenue),
            "Eligible transactions only",
        )

    with c2:
        count_text = (
            f"{int(transaction_count):,}"
            if transaction_count is not None
            else "—"
        )
        metric_card(
            "ELIGIBLE TRANSACTIONS",
            count_text,
            "Included in revenue",
        )

    with c3:
        metric_card(
            "TOP PRODUCT",
            top_product or "—",
            (
                f"{format_inr(product_revenue)} revenue"
                if product_revenue is not None
                else "Highest product revenue"
            ),
        )

    with c4:
        metric_card(
            "LEADING REGION",
            top_region or "—",
            (
                f"{format_inr(region_revenue)} revenue"
                if region_revenue is not None
                else "Highest regional revenue"
            ),
        )

    st.markdown(
        '<div class="section-heading">Revenue trends</div>'
        '<div class="section-subtitle">'
        'Explore how revenue changes across the months.'
        '</div>',
        unsafe_allow_html=True,
    )

    monthly_df = get_monthly_records(monthly_data)

    with st.container(border=True):
        if not monthly_df.empty:
            fig = px.bar(
                monthly_df,
                x="Month",
                y="Revenue",
                text="Revenue",
                color="Revenue",
                color_continuous_scale=[
                    "#FDBA74",
                    "#F97316",
                    "#9A3412",
                ],
                template="plotly_white",
            )

            fig.update_traces(
                texttemplate="₹%{y:,.0f}",
                textposition="outside",
                textfont=dict(color="#171717", size=14, family="Inter"),
                cliponaxis=False,
                marker_line_color="#171717",
                marker_line_width=1.2,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Revenue: ₹%{y:,.0f}<extra></extra>"
                ),
            )

            style_chart(fig, height=430, x_title="Month", y_title="Revenue (₹)")
            fig.update_layout(coloraxis_showscale=False)

            # Extra headroom so the value labels above bars stay readable.
            fig.update_yaxes(
                range=[0, float(monthly_df["Revenue"].max()) * 1.18]
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displaylogo": False, "responsive": True},
            )

        else:
            st.info(
                "Monthly data is unavailable or has an unexpected format."
            )

            with st.expander("Monthly endpoint · Raw JSON"):
                st.json(
                    monthly_data
                    if monthly_data is not None
                    else {"error": errors.get("monthly")}
                )

    
    # Product-wise revenue breakdown
    with st.container(border=True):
        st.markdown("**Product performance**")
        st.caption("Revenue generated by each product.")

        products_payload = data.get("products")
        products_error = errors.get("products")

        if products_error:
            st.warning("Could not load product breakdown.")
        else:
            product_records = (
                products_payload.get("products", [])
                if isinstance(products_payload, dict)
                else []
            )
            product_df = pd.DataFrame(product_records)

            if not product_df.empty and {"product", "revenue"}.issubset(product_df.columns):
                product_df["revenue"] = pd.to_numeric(
                    product_df["revenue"], errors="coerce"
                )
                product_df = product_df.dropna(subset=["revenue"])
                product_df = product_df.sort_values(
                    "revenue", ascending=False
                )

                fig = px.bar(
                    product_df,
                    x="product",
                    y="revenue",
                    text="revenue",
                    template="plotly_white",
                )

                fig.update_traces(
                    marker_color=ORANGE,
                    texttemplate="₹%{y:,.0f}",
                    textposition="outside",
                    cliponaxis=False,
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Revenue: ₹%{y:,.2f}<extra></extra>"
                    ),
                )

                style_chart(
                    fig,
                    height=450,
                    title="Revenue by Product",
                    x_title="Product",
                    y_title="Revenue (₹)",
                )

                max_revenue = float(product_df["revenue"].max())
                fig.update_layout(
                    margin=dict(l=20, r=30, t=70, b=110),
                    showlegend=False,
                )
                fig.update_xaxes(tickangle=-30)
                fig.update_yaxes(
                    range=[0, max_revenue * 1.25 if max_revenue > 0 else 1],
                    tickprefix="₹",
                    separatethousands=True,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displaylogo": False, "responsive": True},
                )

                display_products = product_df.rename(
                    columns={
                        "product": "Product",
                        "revenue": "Revenue (₹)",
                    }
                ).copy()

                display_products["Revenue (₹)"] = (
                    display_products["Revenue (₹)"].map(
                        lambda value: f"₹{value:,.2f}"
                    )
                )

                st.dataframe(
                    display_products,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No product breakdown data is available.")

    # Region-wise revenue breakdown
    with st.container(border=True):
        st.markdown("**Regional performance**")
        st.caption("Revenue generated by each region.")

        regions_payload = data.get("regions")
        regions_error = errors.get("regions")

        if regions_error:
            st.warning("Could not load regional breakdown.")
        else:
            region_records = (
                regions_payload.get("regions", [])
                if isinstance(regions_payload, dict)
                else []
            )
            region_df = pd.DataFrame(region_records)

            if not region_df.empty and {"region", "revenue"}.issubset(region_df.columns):
                region_df["revenue"] = pd.to_numeric(
                    region_df["revenue"], errors="coerce"
                )
                region_df = region_df.dropna(subset=["revenue"])
                region_df = region_df.sort_values(
                    "revenue", ascending=False
                )

                fig = px.bar(
                    region_df,
                    x="region",
                    y="revenue",
                    text="revenue",
                    template="plotly_white",
                )

                fig.update_traces(
                    marker_color=ORANGE,
                    texttemplate="₹%{y:,.0f}",
                    textposition="outside",
                    cliponaxis=False,
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Revenue: ₹%{y:,.2f}<extra></extra>"
                    ),
                )

                style_chart(
                    fig,
                    height=400,
                    title="Revenue by Region",
                    x_title="Region",
                    y_title="Revenue (₹)",
                )

                max_revenue = float(region_df["revenue"].max())
                fig.update_layout(
                    margin=dict(l=20, r=30, t=70, b=60),
                    showlegend=False,
                )
                fig.update_yaxes(
                    range=[0, max_revenue * 1.25 if max_revenue > 0 else 1],
                    tickprefix="₹",
                    separatethousands=True,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displaylogo": False, "responsive": True},
                )

                display_regions = region_df.rename(
                    columns={
                        "region": "Region",
                        "revenue": "Revenue (₹)",
                    }
                ).copy()

                display_regions["Revenue (₹)"] = (
                    display_regions["Revenue (₹)"].map(
                        lambda value: f"₹{value:,.2f}"
                    )
                )

                st.dataframe(
                    display_regions,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No regional breakdown data is available.")


    if st.button("✦ Ask AI about these numbers"):
        st.session_state["selected_page"] = "AI Assistant"
        st.rerun()


# ============================================================
# AI ASSISTANT PAGE
# ============================================================

elif page == "AI Assistant":
    st.markdown(
        '<div class="section-heading">Meet your AI analyst</div>'
        '<div class="section-subtitle">'
        'Ask questions in plain English. Gemini interprets the question, '
        'and your analytics backend supplies the answer.'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("#### What would you like to know?")
        st.caption(
            "Choose a suggested question or enter your own."
        )

        suggestions = [
            "What is the total revenue?",
            "Which product generated the highest revenue?",
            "Which region has the highest revenue?",
            "Compare revenue between January and February 2026",
        ]

        suggestion_cols = st.columns(2, gap="small")

        for index, suggestion in enumerate(suggestions):
            with suggestion_cols[index % 2]:
                if st.button(
                    suggestion,
                    key=f"suggestion_{index}",
                    use_container_width=True,
                ):
                    st.session_state["question_input"] = suggestion

        with st.form("ask_salesiq_form"):
            question = st.text_input(
                "Your question",
                key="question_input",
                placeholder="e.g. Which month had the highest revenue?",
            )

            submitted = st.form_submit_button(
                "✦  Ask Datrix",
                use_container_width=True,
            )

    if submitted:
        if not question.strip():
            st.warning("Please enter a question first.")

        else:
            with st.spinner("Analyzing your question..."):
                result, error = api_post(
                    "/ask-ai",
                    {"question": question.strip()},
                )

            if error:
                st.error(
                    "Could not get an answer from the AI service: "
                    + error
                )
            else:
                render_ai_response(result)

    st.markdown(
        '<div class="section-heading">Questions worth exploring</div>'
        '<div class="section-subtitle">'
        'Discover patterns and insights in your sales data.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "- Which product contributes the most revenue?\n"
        "- How did revenue change between two months?\n"
        "- Which region performs best?\n"
        "- What is the total eligible revenue?"
    )


# ============================================================
# DATA QUALITY PAGE
# ============================================================


elif page == "Data Quality":
    st.markdown(
        '<div class="section-heading">Data quality centre</div>'
        '<div class="section-subtitle">'
        'Understand which records are included in revenue calculations '
        'and which records need attention.'
        '</div>',
        unsafe_allow_html=True,
    )

    quality_data = data.get("quality")

    if errors.get("quality"):
        st.warning(
            "The data-quality endpoint could not be loaded: "
            + str(errors["quality"])
        )

    elif quality_data is not None:
        if isinstance(quality_data, dict):
            original_rows = find_value(
                quality_data,
                ["original_rows", "total_rows", "row_count"],
            )

            eligible_rows = find_value(
                quality_data,
                [
                    "eligible_for_revenue",
                    "eligible_transactions",
                    "eligible_rows",
                ],
            )

            flagged_rows = find_value(
                quality_data,
                [
                    "rows_with_quality_flags",
                    "flagged_rows",
                    "invalid_rows",
                ],
            )

            excluded_rows = find_value(
                quality_data,
                ["excluded_from_revenue", "excluded_rows"],
            )

            # Main metric cards
            a, b, c, d = st.columns(4, gap="medium")

            with a:
                metric_card(
                    "SOURCE ROWS",
                    original_rows if original_rows is not None else "—",
                    "Rows read from CSV",
                )

            with b:
                metric_card(
                    "ELIGIBLE ROWS",
                    eligible_rows if eligible_rows is not None else "—",
                    "Used for revenue",
                )

            with c:
                metric_card(
                    "FLAGGED ROWS",
                    flagged_rows if flagged_rows is not None else "—",
                    "Need attention",
                )

            with d:
                metric_card(
                    "EXCLUDED ROWS",
                    excluded_rows if excluded_rows is not None else "—",
                    "Not counted in revenue",
                )

            st.markdown("")

            # Revenue eligibility policy card
            policy = quality_data.get(
                "revenue_policy",
                "Completed transactions with valid dates and products, "
                "positive quantities and prices, valid nonnegative "
                "discounts, and unique transaction IDs are included.",
            )

            st.markdown(
                f"""
                <div style="
                    background:
                        radial-gradient(420px 160px at 100% 0%,
                            rgba(249,115,22,0.14), transparent 70%),
                        #FFFFFF;
                    border:1px solid #E7E5E4;
                    border-left:6px solid #F97316;
                    border-radius:16px;
                    padding:24px 26px;
                    margin:8px 0 26px 0;
                    box-shadow:0 8px 24px rgba(0,0,0,0.06);
                ">
                    <div style="
                        display:flex;
                        align-items:center;
                        gap:12px;
                        margin-bottom:12px;
                    ">
                        <div style="
                            background:linear-gradient(135deg,#171717,#3A1A0A);
                            border-radius:10px;
                            padding:8px 12px;
                            color:#FDBA74;
                            font-size:18px;
                            font-weight:800;
                        ">✓</div>
                        <div style="
                            font-size:18px;
                            font-weight:800;
                            color:#171717;
                        ">Revenue eligibility policy</div>
                    </div>
                    <div style="
                        color:#44403C;
                        font-size:14px;
                        line-height:1.9;
                    ">{html.escape(str(policy))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Dataset details heading
            st.markdown(
                '<div class="section-heading">Dataset details</div>'
                '<div class="section-subtitle">'
                'Source file, processing summary, and storage location.'
                '</div>',
                unsafe_allow_html=True,
            )

            # Identify fields already displayed as metric cards.
            metric_keys = {
                "original_rows",
                "total_rows",
                "row_count",
                "eligible_for_revenue",
                "eligible_transactions",
                "eligible_rows",
                "rows_with_quality_flags",
                "flagged_rows",
                "invalid_rows",
                "excluded_from_revenue",
                "excluded_rows",
                "revenue_policy",
            }

            # Friendly labels for commonly returned fields.
            friendly_labels = {
                "source_file": "Source file",
                "stored_rows": "Stored rows",
                "eligible_net_revenue": "Eligible net revenue",
                "database": "Database location",
            }

            # Show source file and other remaining scalar details as cards.
            detail_items = []

            for key, value in quality_data.items():
                if key in metric_keys:
                    continue

                if isinstance(value, (dict, list)) or value is None:
                    continue

                label = friendly_labels.get(
                    key,
                    str(key).replace("_", " ").title(),
                )

                detail_items.append((label, value))

            if detail_items:
                for start in range(0, len(detail_items), 2):
                    cols = st.columns(2, gap="medium")

                    for offset, (label, value) in enumerate(
                        detail_items[start:start + 2]
                    ):
                        with cols[offset]:
                            display_value = str(value)

                            if label == "Eligible net revenue":
                                try:
                                    display_value = f"₹{float(value):,.2f}"
                                except (ValueError, TypeError):
                                    pass

                            st.markdown(
                                f"""
                                <div style="
                                    background:linear-gradient(180deg,
                                        #FFFFFF 0%, #FFF9F3 100%);
                                    border:1px solid #E7E5E4;
                                    border-top:4px solid #F97316;
                                    border-radius:14px;
                                    padding:19px 21px;
                                    min-height:100px;
                                    margin-bottom:14px;
                                    box-shadow:0 6px 18px
                                        rgba(0,0,0,0.05);
                                ">
                                    <div style="
                                        color:#78716C;
                                        font-size:11px;
                                        font-weight:800;
                                        letter-spacing:1.1px;
                                        text-transform:uppercase;
                                        margin-bottom:10px;
                                    ">{html.escape(label)}</div>
                                    <div style="
                                        color:#1C1917;
                                        font-size:16px;
                                        font-weight:700;
                                        line-height:1.6;
                                        overflow-wrap:anywhere;
                                    ">{html.escape(display_value)}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

            # Technical JSON remains collapsed.
            with st.expander(
                "⚙️ Developer diagnostics · Raw JSON",
                expanded=False,
            ):
                st.json(quality_data)

        else:
            st.write(quality_data)

            with st.expander(
                "⚙️ Developer diagnostics · Raw JSON",
                expanded=False,
            ):
                st.json(quality_data)

    else:
        st.info("No data-quality information is currently available.")

    if st.button("Refresh quality report"):
        st.cache_data.clear()
        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    DATRIX · BUSINESS INTELLIGENCE ASSISTANT
    <br><br>
    Analytics powered by Python & SQLite
    · AI question interpretation powered by Gemini
</div>
""", unsafe_allow_html=True)