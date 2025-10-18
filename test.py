import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- PAGE CONFIG ----
st.set_page_config(page_title="SSGMIS Data Visualization", layout="wide")
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

# ---- SHOW NOTHING UNTIL UPLOAD ----
if uploaded_file is None:
    st.info("👋 Please upload an Excel dataset (.xlsx) to view the charts.")
else:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Dataset successfully loaded!")

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

        # ---- PIE CHART ----
        if tam_chart == "Perceived Usefulness (PU) - Pie Chart":
            selected_data = df[df["Category"] == "Perceived Usefulness (PU)"].iloc[0, 1:]
            labels = selected_data.index.tolist()[::-1]
            values = selected_data.values.tolist()[::-1]
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title("Perceived Usefulness (PU)")
            st.pyplot(fig)

        # ---- BAR CHART ----
        elif tam_chart == "Perceived Ease of Use (PEOU) - Bar Chart":
            selected_data = df[df["Category"] == "Perceived Ease of Use (PEOU)"].iloc[0, 1:]
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.bar(labels, values, color="royalblue", edgecolor="black")
            ax.set_title("Perceived Ease of Use (PEOU)")
            st.pyplot(fig)

        # ---- LINE CHART ----
        elif tam_chart == "Attitude Toward Using (ATU) - Line Chart":
            selected_data = df[df["Category"] == "Attitude Toward Using (ATU)"].iloc[0, 1:]
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(labels, values, marker="o", color="mediumseagreen", linewidth=2)
            ax.set_title("Attitude Toward Using (ATU)")
            st.pyplot(fig)

        # ---- STACKED BAR ----
        elif tam_chart == "Behavioral Intention (BI) - Stacked Bar Chart":
            selected_data = df[df["Category"] == "Behavioral Intention (BI)"]
            scales = ["3-Neutral", "4-Agree", "5-Strongly Agree"]
            colors = ["moccasin", "lightskyblue", "royalblue"]

            fig, ax = plt.subplots(figsize=(8, 5))
            bottom = [0]
            for i, scale in enumerate(scales):
                ax.bar(
                    ["Behavioral Intention (BI)"],
                    selected_data[scale],
                    bottom=bottom,
                    label=scale,
                    color=colors[i]
                )
                bottom = [a + b for a, b in zip(bottom, selected_data[scale])]
            ax.legend(title="Scale", bbox_to_anchor=(1.05, 1), loc="upper left")
            ax.set_title("Behavioral Intention (BI)")
            st.pyplot(fig)

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

        if uat_chart == "Functionality (Pie Chart)":
            selected_data = df[df["Category"] == "UAT Functionality"].iloc[0, 1:]
            labels = selected_data.index.tolist()[::-1]
            values = selected_data.values.tolist()[::-1]
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title("UAT Functionality")
            st.pyplot(fig)

        elif uat_chart == "Usability (Bar Chart)":
            selected_data = df[df["Category"] == "UAT Usability"].iloc[0, 1:]
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.bar(labels, values, color="lightcoral", edgecolor="black")
            ax.set_title("UAT Usability")
            st.pyplot(fig)

        elif uat_chart == "Performance (Line Chart)":
            selected_data = df[df["Category"] == "UAT Performance"].iloc[0, 1:]
            labels = selected_data.index.tolist()
            values = selected_data.values.tolist()
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(labels, values, marker="o", color="darkorange", linewidth=2)
            ax.set_title("UAT Performance")
            st.pyplot(fig)

        elif uat_chart == "Satisfaction & Acceptance (Stacked Bar Chart)":
            uat_subset = df[df["Category"].str.contains("UAT")]
            categories = uat_subset["Category"]
            scales = ["3-Neutral", "4-Agree", "5-Strongly Agree"]
            colors = ["moccasin", "lightskyblue", "royalblue"]

            fig, ax = plt.subplots(figsize=(9, 6))
            bottom = [0] * len(categories)
            for i, scale in enumerate(scales):
                ax.bar(categories, uat_subset[scale], bottom=bottom, label=scale, color=colors[i])
                bottom = [a + b for a, b in zip(bottom, uat_subset[scale])]
            ax.legend(title="Scale", bbox_to_anchor=(1.05, 1), loc="upper left")
            ax.set_title("UAT Satisfaction & Acceptance")
            st.pyplot(fig)

    # =============================
    # 📘 ABOUT SECTION
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
