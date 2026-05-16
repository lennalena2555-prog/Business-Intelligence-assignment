
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Malaria Risk Dashboard",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("Malaria Risk Interactive Dashboard")
st.markdown(
    "Analyze malaria diagnosis patterns, risk scores, and trends using interactive filters."
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        r"G:\My Drive\MDS\SEM1.2\Malaria_Dataset.csv")
    
    # Print columns to debug KeyError: 'DOA'
    print("Columns in the dataset:", df.columns.tolist())

    # Handle dates safely
    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=["Date"])

    # Create time columns
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()

    return df


df = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Dashboard Filters")

# Year filter
years = sorted(df["Year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

# Diagnosis filter
diagnosis_types = sorted(df["Diagnosis_Type"].unique())

selected_diagnosis = st.sidebar.multiselect(
    "Select Diagnosis Type",
    diagnosis_types,
    default=diagnosis_types
)

# Filter dataset
filtered_df = df[
    (df["Year"] == selected_year)
    & (df["Diagnosis_Type"].isin(selected_diagnosis))
]

# -----------------------------
# KPI METRICS
# -----------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

total_risk = filtered_df["Risk_Score"].sum()
avg_risk = filtered_df["Risk_Score"].mean()
records = filtered_df.shape[0]

col1.metric("Total Risk Score", f"{total_risk:,.0f}")
col2.metric("Average Risk Score", f"{avg_risk:,.2f}")
col3.metric("Total Records", f"{records:,}")

st.markdown("---")

# -----------------------------
# CHARTS SECTION
# -----------------------------
col1, col2 = st.columns(2)

# Trend chart
with col1:
    st.subheader("Risk Score Trend Over Time")

    trend = (
        filtered_df.groupby("Date")["Risk_Score"]
        .sum()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(
        trend.index,
        trend.values,
        marker="o"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Risk Score")
    ax.set_title("Risk Score Trend")

    plt.xticks(rotation=45)

    st.pyplot(fig)

# Bar chart
with col2:
    st.subheader("Risk Score by Diagnosis Type")

    category = (
        filtered_df.groupby("Diagnosis_Type")[
            "Risk_Score"
        ]
        .sum()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(7, 4))

    ax2.bar(
        category.index,
        category.values
    )

    ax2.set_xlabel("Diagnosis Type")
    ax2.set_ylabel("Risk Score")
    ax2.set_title("Diagnosis Comparison")

    plt.xticks(rotation=30)

    st.pyplot(fig2)

# -----------------------------
# MONTHLY ANALYSIS
# -----------------------------
st.subheader("Monthly Risk Analysis")

monthly = (
    filtered_df.groupby("Month")[
        "Risk_Score"
    ]
    .mean()
)

fig3, ax3 = plt.subplots(figsize=(10, 4))

monthly.plot(
    kind="bar",
    ax=ax3
)

ax3.set_ylabel("Average Risk Score")
ax3.set_title("Monthly Average Risk Score")

st.pyplot(fig3)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Download button
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_malaria_data.csv",
    mime="text/csv"
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit | Module 6 Dashboard")
