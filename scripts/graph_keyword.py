import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Your list of dictionaries
def create_graph(data):

    # Flatten the data into a DataFrame
    flat_data = []
    for sublist in data:
        for item in sublist:
            for keyword, attributes in item.items():
                flat_data.append({
                    "Keyword": keyword,
                    "Keyword Difficulty": attributes.get("Keyword Difficulty", "").capitalize(),
                    "Cost per Click (CPC)": attributes.get("Cost per Click (CPC)", "").capitalize(),
                    "Search Volume": attributes.get("Search Volume", "").capitalize()
                })

    df = pd.DataFrame(flat_data)

    # Display DataFrame in Streamlit
    st.write("Keywords and their Attributes", df)

    # Convert difficulty, CPC, and volume levels to numerical values for plotting
    difficulty_map = {"Low": 1, "Moderate": 2, "Medium": 2, "High": 3}
    df["Keyword Difficulty Value"] = df["Keyword Difficulty"].map(difficulty_map)
    df["Cost per Click (CPC) Value"] = df["Cost per Click (CPC)"].map(difficulty_map)
    df["Search Volume Value"] = df["Search Volume"].map(difficulty_map)

    # Plotting
    st.subheader("Keyword Attributes Plot")

    fig, ax = plt.subplots()
    df.plot(kind="bar", x="Keyword", y=["Keyword Difficulty Value", "Cost per Click (CPC) Value", "Search Volume Value"], ax=ax)
    plt.ylabel("Attribute Level (1=Low, 2=Moderate, 3=High)")
    plt.title("Keyword Attributes Analysis")
    st.pyplot(fig)