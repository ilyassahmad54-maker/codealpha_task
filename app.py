from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="LabourLens | India Employment", page_icon="◈", layout="wide")

RATE = "Estimated Unemployment Rate (%)"
EMPLOYED = "Estimated Employed"
PARTICIPATION = "Estimated Labour Participation Rate (%)"
TEAL = "#087f83"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {color-scheme: light;}
.stApp {background:#f4f7f9; color:#182b3a; font-family:'DM Sans',sans-serif;}
h1,h2,h3 {font-family:'Manrope',sans-serif; letter-spacing:-.035em; color:#182b3a;}
.block-container {padding-top:2.2rem; padding-bottom:2rem; max-width:1500px;}
[data-testid="stSidebar"] {background:#eaf0f3; border-right:1px solid #dbe5e9;}
[data-testid="stSidebar"] .block-container {padding-top:2rem;}
[data-testid="stMetric"] {background:white; border:1px solid #e0e8ec; border-radius:16px; padding:21px 24px; box-shadow:0 4px 18px #203e4b04;}
[data-testid="stMetricLabel"] {color:#657681; font-size:13px;}
[data-testid="stMetricValue"] {font-family:'Manrope',sans-serif; font-weight:800; color:#163744; font-size:32px;}
[data-testid="stVerticalBlockBorderWrapper"]>div {border-radius:16px; border-color:#e0e8ec!important;}
[data-testid="stTabs"] button {font-weight:600;}
.stDownloadButton button {border-radius:9px;}
.brand {font-family:'Manrope',sans-serif; font-size:26px; font-weight:800; letter-spacing:-1px; color:#163744;}
.brand span {color:#087f83;}
.eyebrow {font-size:11px; font-weight:700; letter-spacing:2px; color:#087f83; margin-bottom:10px;}
.hero {background:linear-gradient(115deg,#123947,#175966); border-radius:20px; padding:32px 36px; margin:12px 0 24px; position:relative; overflow:hidden;}
.hero:after {content:''; position:absolute; width:240px; height:240px; border:40px solid #ffffff08; border-radius:50%; right:-40px; top:-90px; pointer-events:none;}
.hero h1 {font-size:36px; line-height:1.2; color:#fff; margin:0 0 10px; font-weight:800;}
.hero p {color:#c4dce2; max-width:650px; font-size:15px; margin:0; line-height:1.7;}
.hero .eyebrow {color:#8be0ce;}
.pill {display:inline-block; border:1px solid #ffffff30; padding:5px 11px; border-radius:30px; color:#d4ebe9; font-size:11px; margin-top:20px;}
.insight {background:#e6f3f0; border:1px solid #c6e4dc; border-left:4px solid #087f83; padding:17px 20px; border-radius:12px; margin:18px 0 22px; font-size:14px; line-height:1.7; color:#24534f;}
.note {font-size:12px; color:#788a95; line-height:1.6;}
.footer {margin-top:28px; padding-top:18px; border-top:1px solid #dce5ea; color:#788a95; font-size:12px;}
@media(max-width:700px) {.hero {padding:24px;} .hero h1 {font-size:28px;} .block-container {padding-top:1rem;}}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    data = pd.read_csv(Path(__file__).parent / "Unemployment_Rate_upto_11_2020.csv")
    data.columns = data.columns.str.strip()
    # The source has two Region columns: state first, geographic zone second.
    data = data.rename(columns={"Region": "State", "Region.1": "Zone"})
    data["Date"] = pd.to_datetime(data["Date"].str.strip(), dayfirst=True)
    return data.sort_values(["Date", "State"])


def chart_style(fig, height=340):
    fig.update_layout(
        height=height, margin=dict(l=10, r=15, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#536a78", size=12),
        hoverlabel=dict(bgcolor="white", font_size=13),
        legend=dict(title=None, orientation="h", y=1.13, x=0),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#e9eff2", zeroline=False)
    return fig


df = load_data()
with st.sidebar:
    st.markdown('<div class="brand">◈ Labour<span>Lens</span></div>', unsafe_allow_html=True)
    st.caption("INDIA · EMPLOYMENT INTELLIGENCE")
    st.divider()
    st.markdown("#### Explore the data")
    zones = st.multiselect("Geographic zones", sorted(df["Zone"].unique()), placeholder="All zones")
    available = df[df["Zone"].isin(zones)] if zones else df
    states = st.multiselect("States & territories", sorted(available["State"].unique()), placeholder="All available states")
    months = sorted(df["Date"].unique())
    period = st.select_slider("Observation period", options=months, value=(months[0], months[-1]), format_func=lambda d: pd.Timestamp(d).strftime("%b %Y"))
    st.caption("Leave a selection empty to include all available locations.")
    st.divider()
    st.markdown("#### About this dashboard")
    st.caption("Explore state-level employment patterns in India during 2020, including the disruption around the COVID-19 lockdown.")
    st.markdown('<div class="note">SOURCE FILE<br>Unemployment_Rate_upto_11_2020.csv<br><br>Monthly observations · Historical data<br>Rates are percentages; changes are percentage points.</div>', unsafe_allow_html=True)

filtered = available[available["Date"].between(*period)]
if states:
    filtered = filtered[filtered["State"].isin(states)]

st.markdown('<div class="eyebrow">LABOUR MARKET / INDIA</div>', unsafe_allow_html=True)
st.markdown('''<div class="hero"><div class="eyebrow">THE EMPLOYMENT OBSERVATORY</div><h1>A clearer view of work in India.</h1><p>Explore how unemployment evolved, where the pressure was greatest, and what the numbers reveal about the labour market.</p><div class="pill">2020 HISTORICAL DATA &nbsp; / &nbsp; INTERACTIVE EXPLORER</div></div>''', unsafe_allow_html=True)

if filtered.empty:
    st.info("No observations match these filters. Choose a wider period or another location.")
    st.stop()

start, end = filtered["Date"].min(), filtered["Date"].max()
st.markdown(f"### Labour market overview")
st.caption(f"{start:%b %Y} – {end:%b %Y}  ·  {filtered['State'].nunique()} states & territories  ·  {len(filtered):,} observations")
trend = filtered.groupby("Date", as_index=False).agg(rate=(RATE, "mean"), participation=(PARTICIPATION, "mean"))
latest = filtered[filtered["Date"] == end]
first_rate = trend.iloc[0]["rate"]
last_rate = trend.iloc[-1]["rate"]
a, b, c, d = st.columns(4)
a.metric("Average unemployment", f"{filtered[RATE].mean():.1f}%", help="Unweighted mean of all state-month unemployment observations in the selected scope.")
b.metric("Latest month unemployment", f"{last_rate:.1f}%", f"{last_rate-first_rate:+.1f} pp vs first month" if len(trend)>1 else None, delta_color="inverse")
c.metric("Labour participation", f"{filtered[PARTICIPATION].mean():.1f}%", help="Unweighted average labour participation rate across selected state-month observations.")
d.metric("Latest estimated employed", f"{latest[EMPLOYED].sum()/1e6:.1f}M", help="Sum of estimated employed people for selected states in the latest available month. Coverage may vary by month.")

peak = trend.loc[trend["rate"].idxmax()]
st.markdown(f'<div class="insight"><b>A moment in focus.</b> Average unemployment peaked at <b>{peak["rate"]:.1f}% in {peak["Date"]:%B %Y}</b> within your selection. The latest month is <b>{abs(last_rate-peak["rate"]):.1f} percentage points</b> below that peak.</div>', unsafe_allow_html=True)

overview, compare, data_tab = st.tabs(["Overview", "State comparison", "Explore & download"])
with overview:
    left, right = st.columns([1.65, 1])
    with left, st.container(border=True):
        st.markdown("#### Unemployment over time")
        st.caption("Monthly average across selected states")
        fig = go.Figure(go.Scatter(x=trend["Date"], y=trend["rate"], mode="lines+markers", line=dict(color=TEAL, width=3), marker=dict(size=7, color=TEAL), fill="tozeroy", fillcolor="rgba(8,127,131,0.08)", hovertemplate="%{x|%b %Y}<br>Unemployment: %{y:.2f}%<extra></extra>"))
        fig.update_yaxes(title=None, ticksuffix="%", rangemode="tozero")
        fig.update_xaxes(dtick="M1", tickformat="%b")
        st.plotly_chart(chart_style(fig), width="stretch")
    with right, st.container(border=True):
        st.markdown("#### Highest unemployment")
        st.caption("Top 8 states · average in selected period")
        ranking = filtered.groupby("State", as_index=False)[RATE].mean().nlargest(8, RATE).sort_values(RATE)
        fig = px.bar(ranking, x=RATE, y="State", orientation="h", text=RATE, color_discrete_sequence=[TEAL])
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False, hovertemplate="%{y}<br>Average: %{x:.2f}%<extra></extra>")
        fig.update_xaxes(title=None, ticksuffix="%", range=[0, ranking[RATE].max()*1.24])
        fig.update_yaxes(title=None)
        st.plotly_chart(chart_style(fig), width="stretch")
    with st.container(border=True):
        st.markdown("#### Participation & unemployment")
        st.caption("Each point is a state-month observation. Hover to explore the underlying values.")
        fig = px.scatter(filtered, x=PARTICIPATION, y=RATE, color="Zone", hover_name="State", hover_data={"Date": "|%b %Y", EMPLOYED: ":,", PARTICIPATION: ":.2f", RATE: ":.2f"}, color_discrete_sequence=[TEAL,"#e6a345","#6780b5","#ba7291","#77a995"], opacity=.75)
        fig.update_traces(marker=dict(size=9, line=dict(width=1, color="white")))
        fig.update_xaxes(title="Labour participation (%)", ticksuffix="%")
        fig.update_yaxes(title="Unemployment (%)", ticksuffix="%")
        st.plotly_chart(chart_style(fig, 360), width="stretch")
with compare:
    with st.container(border=True):
        st.markdown("#### The monthly picture, state by state")
        st.caption("Unemployment rate (%) · blank cells indicate missing observations")
        matrix = filtered.pivot_table(index="State", columns="Date", values=RATE).sort_index()
        fig = go.Figure(go.Heatmap(z=matrix.values, x=[date.strftime("%b %Y") for date in matrix.columns], y=matrix.index, colorscale=[[0,"#e6f3f0"],[.35,"#90c8bd"],[.65,"#e9c582"],[1,"#bd624b"]], colorbar=dict(title="Rate %", thickness=12), hoverongaps=False, hovertemplate="%{y} · %{x}<br>Unemployment: %{z:.2f}%<extra></extra>"))
        fig.update_yaxes(autorange="reversed", dtick=1)
        st.plotly_chart(chart_style(fig, max(350, len(matrix)*25+100)), width="stretch")
with data_tab:
    st.markdown("#### Behind the numbers")
    st.caption("The complete filtered dataset, ready for your own analysis.")
    export = filtered.drop(columns=["longitude", "latitude"], errors="ignore").copy()
    export["Date"] = export["Date"].dt.strftime("%Y-%m-%d")
    st.download_button("↓ Download filtered CSV", export.to_csv(index=False).encode("utf-8"), "labourlens_filtered_data.csv", "text/csv")
    st.dataframe(export, width="stretch", hide_index=True)
    with st.expander("How to read these metrics"):
        st.write("Unemployment rate measures the share of the labour force estimated to be unemployed. Labour participation measures the share of the working-age population in the labour force. Estimated employed is a count of people.")
        st.write("Dashboard rate averages are unweighted across available observations, not population-weighted national estimates. Changes in state coverage can affect comparisons over time. The latest employment total uses only states observed in the latest selected month; missing observations are not filled in.")
        st.write("This is a historical exploratory dataset. Patterns and correlations do not establish causation.")
st.markdown('<div class="footer">◈ LabourLens &nbsp; · &nbsp; A closer look at India’s labour market <span style="float:right">Historical data / 2020</span></div>', unsafe_allow_html=True)
