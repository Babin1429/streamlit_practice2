import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.title("Visualizer")

uploaded_file = st.sidebar.file_uploader("Add your CSV here:", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.sidebar.header("Sorting")

    n_columns = df.select_dtypes(include=['number']).columns
    s_columns = st.sidebar.selectbox("Select Column", n_columns)

    min_value = float(df[s_columns].min())
    max_value = float(df[s_columns].max())

    r_values = st.sidebar.slider(
        "Range of values",
        min_value,
        max_value,
        (min_value, max_value)
    )

    filtered_df = df[
        (df[s_columns] >= r_values[0]) &
        (df[s_columns] <= r_values[1])
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", len(filtered_df))
    with col2:
        st.metric("Mean", round(filtered_df[s_columns].mean(), 2))
    with col3:
        st.metric("Max", round(filtered_df[s_columns].max(), 2))

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    chart_model = st.radio("Select Graph Type:", ["Bar", "Line", "Histogram"])

    if chart_model == "Bar":
        st.bar_chart(filtered_df[s_columns])
    elif chart_model == "Line":
        st.line_chart(filtered_df[s_columns])
    else:
        fig, ax = plt.subplots()
        ax.hist(filtered_df[s_columns], bins=20)
        st.pyplot(fig)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Results", csv, "result.csv", "text/csv")

else:
    st.info("Upload a CSV file to get started.")