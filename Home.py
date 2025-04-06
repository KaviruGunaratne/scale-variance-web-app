import streamlit as st

# Set page config
st.set_page_config(page_title="The Effect of Scale on Quality Metrics for Dimensionality Reduction", layout="centered")

st.write("# The Effect of Scale on Quality Metrics for Dimensionality Reduction")

st.markdown(
    """The quality of projections created by dimensionality reduction algorithms can be measured using 
    normalized stress and KL divergence.
    However, a main issue with these metrics is that they are sensitive to scale.
    This website demonstrates the scale sensitiveness of these two metrics on various datasets and dimensionality
    reduction algorithms."""
)