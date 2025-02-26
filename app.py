# Imports
import streamlit as st
import pandas as pd
import os 
from io import BytesIO
import time  # Added for animations

# Setup our App
st.set_page_config(page_title="📊 Data Sweeper", layout="wide")
st.markdown("<h1 style='color: blue; text-align: center;'>🧹 Data Sweeper</h1>", unsafe_allow_html=True)
st.write("🔄 Transform your files between **CSV** and **Excel** formats with built-in data cleaning and visualization.")

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_extension = os.path.splitext(file.name)[-1].lower()

        # Read File
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_extension}")
            continue

        # Display File Info
        st.write(f"📄 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.getbuffer().nbytes / 1024:.2f} KB")

        # Show first 5 rows of DataFrame
        st.subheader("🔎 Preview the Dataframe")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"✅ Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates for {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"🛠 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if not numeric_cols.empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing Values Filled!")
                    else:
                        st.warning("⚠️ No numeric columns found to fill missing values!")

        # Select Columns
        st.subheader("📌 Select Columns to Convert")
        columns = st.multiselect(f"🎯 Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Visualization for {file.name}"):
            numeric_data = df.select_dtypes(include=['number'])
            if not numeric_data.empty and numeric_data.shape[1] >= 2:
                st.bar_chart(numeric_data.iloc[:, :2])
            else:
                st.warning("⚠️ Not enough numeric data for visualization!")

        # File Conversion Options
        st.subheader("📂 File Conversion")
        conversion_type = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"📥 Convert {file.name}"):
            with st.spinner("⏳ Processing file... Please wait."):
                time.sleep(1.5)  # Adding animation delay
                
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_extension, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")  # Fixed error: Added openpyxl engine
                    file_name = file.name.replace(file_extension, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                # Download button
                st.download_button(
                    label=f"⬇️ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )
                st.success(f"✅ {file.name} converted successfully!")

