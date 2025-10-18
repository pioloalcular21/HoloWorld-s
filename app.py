# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- PAGE CONFIG ----
st.set_page_config(page_title="SSGMIS Data Visualization", layout="wide")

# ---- CUSTOM CSS ----
st.markdown(
    """
    <style>
    body {
        background-color: #f9fafc;
        color: #1f2937;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #0f172a;
    }
    .title {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1e40af;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        text-align: center;
        color: #475569;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- HEADER ----
st.markdown('<div class="title">📊 SSGMIS TAM & UAT Visualization Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Technology Transfer and Implementation of the Supreme Student Government Management Information System</div>', unsafe_allow_html=True)
st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload Excel Dataset (.xlsx)", type=["xlsx"])

# ---- WAIT FOR FILE ----
if uploaded_file is None:
    st.info("👋 Please upload an Excel dataset (.xlsx) to view the charts.")
    st.stop()

# ---- LOAD DATA ----
try:
    df = pd.read_excel(uploaded_file)
    if "Category" not in df.columns:
        st.error("❌ The uploaded Excel file must contain a 'Category' column.")
        st.stop()
    st.success("✅ Dataset successfully loaded!")
except Exception as e:
    st.error(f"❌ Error reading file: {e}")
    st.stop()

# ---- SIDEBAR MENU ----
section = st.sidebar.radio(
    "Select Section:",
    ("🏫 TAM Charts", "🧪 UAT Charts", "📘 About")
)

# =============================
# 🏫 TECHNOLOGY ACCEPTANCE MODEL (TAM)
# =============================
if section == "🏫 TAM Charts":
    st.header("🏫 Technology Acceptance Model (TAM)")

    tam_chart = st.selectbox(
        "Select a TAM construct:",
        [
            "Perceived Usefulness (PU) - Pie Chart",
            "Perceived Ease of Use (PEOU) - Bar Chart",
            "Attitude Toward Using (ATU) - Line Chart",
            "Behavioral Intention (BI) - Stacked Bar Chart"
        ]
    )

    def get_data(category):
        if category not in df["Category"].values:
            st.warning(f"⚠️ No data found for '{category}'")
            return None
        return df[df["Category"] == category].iloc[0, 1:]

    # ---- PIE CHART ----
    if tam_chart == "Perceived Usefulness (PU) - Pie Chart":
        selected_data = get_data("Perceived Usefulness (PU)")
        if selected_data is not None:
            labels = selected_data.index.tolist()[::-1]
            values = selected_data.values.tolist()[::-1]
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title("Perceived Usefulness (PU)")
            st.pyplot(fig)

    # ---- BAR CHART ----
    elif tam_chart == "Perceived Ease of Use (PEOU) - Bar Chart":
        selected_data = get_data("Perceived Ease of Use (PEOU)")
        if selected_data is not None:
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots()
            ax.bar(labels, values, color="royalblue", edgecolor="black")
            ax.set_title("Perceived Ease of Use (PEOU)")
            st.pyplot(fig)

    # ---- LINE CHART ----
    elif tam_chart == "Attitude Toward Using (ATU) - Line Chart":
        selected_data = get_data("Attitude Toward Using (ATU)")
        if selected_data is not None:
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots()
            ax.plot(labels, values, marker="o", color="mediumseagreen", linewidth=2)
            ax.set_title("Attitude Toward Using (ATU)")
            st.pyplot(fig)

    # ---- STACKED BAR CHART ----
    elif tam_chart == "Behavioral Intention (BI) - Stacked Bar Chart":
        category = "Behavioral Intention (BI)"
        if category in df["Category"].values:
            selected_data = df[df["Category"] == category]
            scales = ["3-Neutral", "4-Agree", "5-Strongly Agree"]
            colors = ["moccasin", "lightskyblue", "royalblue"]

            fig, ax = plt.subplots()
            bottom = [0]
            for i, scale in enumerate(scales):
                if scale not in selected_data.columns:
                    st.warning(f"Missing column: {scale}")
                    continue
                ax.bar(
                    [category],
                    selected_data[scale],
                    bottom=bottom,
                    label=scale,
                    color=colors[i]
                )
                bottom = [a + b for a, b in zip(bottom, selected_data[scale])]
            ax.legend(title="Scale", bbox_to_anchor=(1.05, 1), loc="upper left")
            ax.set_title("Behavioral Intention (BI)")
            st.pyplot(fig)
        else:
            st.warning(f"⚠️ No data found for '{category}'")

# =============================
# 🧪 USER ACCEPTANCE TESTING (UAT)
# =============================
elif section == "🧪 UAT Charts":
    st.header("🧪 User Acceptance Testing (UAT)")

    uat_chart = st.selectbox(
        "Select a UAT construct:",
        [
            "Functionality (Pie Chart)",
            "Usability (Bar Chart)",
            "Performance (Line Chart)",
            "Satisfaction & Acceptance (Stacked Bar Chart)"
        ]
    )

    def get_uat_data(cat):
        if cat not in df["Category"].values:
            st.warning(f"⚠️ No data found for '{cat}'")
            return None
        return df[df["Category"] == cat].iloc[0, 1:]

    if uat_chart == "Functionality (Pie Chart)":
        selected_data = get_uat_data("UAT Functionality")
        if selected_data is not None:
            labels = selected_data.index.tolist()[::-1]
            values = selected_data.values.tolist()[::-1]
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title("UAT Functionality")
            st.pyplot(fig)

    elif uat_chart == "Usability (Bar Chart)":
        selected_data = get_uat_data("UAT Usability")
        if selected_data is not None:
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots()
            ax.bar(labels, values, color="lightcoral", edgecolor="black")
            ax.set_title("UAT Usability")
            st.pyplot(fig)

    elif uat_chart == "Performance (Line Chart)":
        selected_data = get_uat_data("UAT Performance")
        if selected_data is not None:
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots()
            ax.plot(labels, values, marker="o", color="darkorange", linewidth=2)
            ax.set_title("UAT Performance")
            st.pyplot(fig)

    elif uat_chart == "Satisfaction & Acceptance (Stacked Bar Chart)":
        uat_subset = df[df["Category"].str.contains("UAT")]
        if uat_subset.empty:
            st.warning("⚠️ No UAT data found.")
        else:
            categories = uat_subset["Category"]
            scales = ["3-Neutral", "4-Agree", "5-Strongly Agree"]
            colors = ["moccasin", "lightskyblue", "royalblue"]

            fig, ax = plt.subplots()
            bottom = [0] * len(categories)
            for i, scale in enumerate(scales):
                if scale not in uat_subset.columns:
                    st.warning(f"Missing column: {scale}")
                    continue
                ax.bar(categories, uat_subset[scale], bottom=bottom, label=scale, color=colors[i])
                bottom = [a + b for a, b in zip(bottom, uat_subset[scale])]
            ax.legend(title="Scale", bbox_to_anchor=(1.05, 1), loc="upper left")
            ax.set_title("UAT Satisfaction & Acceptance")
            st.pyplot(fig)

# =============================
# 📘 ABOUT
# =============================
elif section == "📘 About":
    st.header("📘 About this Dashboard")
    st.markdown("""
    **Developer:** Piolo Alcular  
    **Project Title:** Technology Transfer and Implementation of the SSG Management Information System (SSGMIS)  
    **Institution:** Agusan del Sur State College of Agriculture and Technology (ASSCAT)  

    This dashboard visually presents results from:
    - **Technology Acceptance Model (TAM)**
    - **User Acceptance Testing (UAT)**
    """)
