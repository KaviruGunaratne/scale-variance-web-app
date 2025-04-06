import streamlit as st

from utils.datainfo import DataInfo
from utils.plotly_charts import ALGORITHMS, ALG_NAMES, plot_curves, plot_embeddings


# Set page config
st.set_page_config(page_title="KL Divergence with Scale", layout="wide")


Low_Min_Data = DataInfo("kl_data/0_to_30__400", 5)
High_Min_Data = DataInfo("kl_data/0_to_300__500", 50)

# Runs
runs = [i for i in range(10)]

# SIDEBAR CONTROLS
st.sidebar.title("Controls")

# Select Dataset
selected_dataset = st.sidebar.selectbox("Select Dataset", sorted(Low_Min_Data.dataset_names + High_Min_Data.dataset_names))
# Select DataInfo for selected dataset
low_min = selected_dataset in Low_Min_Data.dataset_names
dataInfo = Low_Min_Data if low_min else High_Min_Data
# Select Run
selected_run = st.sidebar.selectbox("Select Run", runs)
# Max X Slider
max_x = st.sidebar.slider("Max X Value", min_value=dataInfo.min_x, max_value=dataInfo.max_x, value=dataInfo.max_x, step=1)

# Select Algorithms to Plot
st.sidebar.markdown("### Algorithms Plotted")
selected_algorithms = [alg for alg in ALGORITHMS if st.sidebar.checkbox(alg, value=True)]


# Plot KL Divergences
fig = plot_curves(selected_dataset, selected_run, selected_algorithms, False, max_x, dataInfo,
                  f"KL Divergence Curves for {selected_dataset} (Run {selected_run})",
                  "KL Divergence"
)
if fig is None:
    st.error(f"Data for the {selected_dataset} dataset at Run {selected_run} does not currently exist.")
else:
    st.plotly_chart(fig, use_container_width=True)

# Plot Projections
st.markdown("### Projections")

if selected_algorithms:
    cols = st.columns(len(selected_algorithms))
    figs = plot_embeddings(selected_dataset, selected_run, selected_algorithms)
    for col, alg in zip(cols, selected_algorithms):
        if figs[alg] is None:
            col.write(f"No embedding found for {ALG_NAMES[alg]}")
        else:
            col.plotly_chart(figs[alg])
else:
    st.write("Select at least one algorithm to view embeddings") 