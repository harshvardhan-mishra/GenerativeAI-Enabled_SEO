import streamlit as st
from scripts.keyword_extraction import possible_keywords
from scripts.rephrase_text import new_text
from scripts.keyword_ranker import keyword_study
from scripts.graph_keyword import create_graph
from scripts.keyword_attributes import attributes_keyword

st.title("Generative AI Enabled SEO")

# Initialize session state variables if not already set
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'output' not in st.session_state:
    st.session_state.output = None
if 'keyword_analysis' not in st.session_state:
    st.session_state.keyword_analysis = ""
if 'answer' not in st.session_state:
    st.session_state.answer = None

# Define tab structure
tab_names = ["Keyword Extractor", "Keyword Ranker", "Rephrase Text"]
tabs = st.tabs(tab_names)

# Keyword Extractor tab
with tabs[0]:
    st.session_state.input_text = st.text_area("Enter your text here:", value=st.session_state.input_text, height=300)

    if st.button("Generate Keywords"):
        if not st.session_state.input_text.strip():  # Checks if text is empty or whitespace
            st.warning("Please enter text and then press the button.")
        else:
            st.session_state.output = possible_keywords(st.session_state.input_text)  # Generate keywords
            # st.write(f"The possible keywords in your text are: {st.session_state.output[:5]}")

    # Display the generated keywords even when switching tabs
    if st.session_state.output:
        st.write(f"The possible keywords in your text are: {st.session_state.output[:5]}")

# Keyword Ranker tab
with tabs[1]:
    if st.session_state.output:
        if st.button("Compare Keywords"):
            st.session_state.keyword_analysis = keyword_study(st.session_state.output[:5])
            # if st.session_state.keyword_analysis:
            #     st.write(st.session_state.keyword_analysis)
    else:
        st.warning("Please generate keywords first in the 'Keyword Extractor' tab.")

    # Displaying the analysis if it exists in session state
    if st.session_state.keyword_analysis:
        # st.write(st.session_state.keyword_analysis)
        # st.write(type(st.session_state.keyword_analysis))
        ans = attributes_keyword(st.session_state.keyword_analysis)
        create_graph(ans)

# Rephrase Text tab
with tabs[2]:
    if st.session_state.output:
        selected_option = st.selectbox("Select one option from the list:", st.session_state.output[:5])
        st.write("You selected:", selected_option)
        
        if st.button("Generate New Text"):
            st.session_state.answer = new_text(st.session_state.input_text, selected_option)
        
        if st.session_state.answer:
            st.write("Rephrased Text:", st.session_state.answer)
    else:
        st.warning("Please generate keywords first in the 'Keyword Extractor' tab.")
