import streamlit as st
import pandas as pd
import altair as alt
from snowflake.snowpark.context import get_active_session

# Page config
st.set_page_config(page_title="Conversion Lab Dashboard", layout="wide")

# Title
st.title("🧠 Customer Conversion Lab Dashboard")
st.markdown("Explore how product features, review sentiment, and NLP signals influence conversion behavior.")

# Get Snowflake session
session = get_active_session()

# Load enriched data
@st.cache_data(ttl=600)
def load_data():
    return session.table("REVIEWS.PUBLIC.REVIEW_SEGMENTED_ENRICHED").to_pandas()

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
product_types = ["All"] + sorted(df["PRODUCT_TYPE"].dropna().unique())
selected_type = st.sidebar.selectbox("Product Type", product_types)

layouts = ["All"] + sorted(df["PRODUCT_LAYOUT"].dropna().unique())
selected_layout = st.sidebar.selectbox("Product Layout", layouts)

segments = ["All", "HIGH_CONVERT", "MID", "LOW_CONVERT"]
selected_segment = st.sidebar.selectbox("Conversion Segment", segments)

# Apply filters
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["PRODUCT_TYPE"] == selected_type]
if selected_layout != "All":
    filtered_df = filtered_df[filtered_df["PRODUCT_LAYOUT"] == selected_layout]
if selected_segment != "All":
    filtered_df = filtered_df[filtered_df["SEGMENT"] == selected_segment]

# Overview metrics
st.header("📈 Overview Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg. Prediction", f"{filtered_df['PREDICTION'].mean():.2f}")
col2.metric("Avg. Sentiment", f"{filtered_df['REVIEW_SENTIMENT'].mean():.2f}")
col3.metric("Purchase Rate", f"{filtered_df['PURCHASE_DECISION'].mean()*100:.1f}%")
col4.metric("Total Reviews", f"{len(filtered_df):,}")

# Feature impact chart
st.subheader("🔬 Feature Impact on Conversion")
feature_chart = alt.Chart(filtered_df).mark_circle(size=60, opacity=0.6).encode(
    x="FEATURE_1:Q",
    y="PREDICTION:Q",
    color="FEATURE_2:Q",
    tooltip=["FEATURE_1", "FEATURE_2", "PREDICTION"]
).properties(height=400)
st.altair_chart(feature_chart, use_container_width=True)

# Residual distribution
st.subheader("📉 Residual Error Distribution")
filtered_df["RESIDUAL"] = filtered_df["PREDICTION"] - filtered_df["TRUE_LABEL"]
residual_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("RESIDUAL:Q", bin=True),
    y="count()",
    tooltip=["RESIDUAL"]
).properties(height=300)
st.altair_chart(residual_chart, use_container_width=True)

# Sentiment vs conversion
st.subheader("💬 Sentiment vs Conversion")
sentiment_chart = alt.Chart(filtered_df).mark_boxplot().encode(
    x="SENTIMENT_TAG:N",
    y="PREDICTION:Q",
    color="SENTIMENT_TAG:N"
).properties(height=300)
st.altair_chart(sentiment_chart, use_container_width=True)

# NLP signal analysis
st.subheader("🧠 NLP Signals and Conversion")
nlp_cols = ["FRICTION_FLAG", "TRUST_SIGNAL", "PURCHASE_INTENT", "EMOTION", "AUTHENTICITY_SCORE"]
if all(col in filtered_df.columns for col in nlp_cols):
    nlp_summary = filtered_df.groupby("PURCHASE_INTENT")["PREDICTION"].mean().reset_index()
    intent_chart = alt.Chart(nlp_summary).mark_bar().encode(
        x="PURCHASE_INTENT:N",
        y=alt.Y("PREDICTION:Q", title="Avg. Conversion Score"),
        color="PURCHASE_INTENT:N"
    ).properties(height=300)
    st.altair_chart(intent_chart, use_container_width=True)

# Sample reviews
st.subheader("📝 Sample Reviews")
sample = filtered_df[["REVIEW_TEXT", "REVIEW_SENTIMENT", "SEGMENT", "PURCHASE_DECISION"]].dropna().head(5)
for _, row in sample.iterrows():
    st.markdown(f"""
    **Sentiment:** {row['REVIEW_SENTIMENT']:.2f} | **Segment:** {row['SEGMENT']} | **Purchased:** {'Yes' if row['PURCHASE_DECISION'] == 1 else 'No'}
    
    > {row['REVIEW_TEXT']}
    """)

# Footer
st.markdown("---")
st.caption("Built with Streamlit + Snowflake. Data from REVIEW_SEGMENTED_ENRICHED.")
