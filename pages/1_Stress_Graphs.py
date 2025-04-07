import streamlit as st

from utils.datainfo import DataInfo
from utils.plotly_charts import ALGORITHMS, ALG_NAMES, plot_curves, plot_embeddings


# Set page config
st.set_page_config(page_title="Normalized Stress with Scale", layout="wide")


Low_Min_Data = DataInfo("stress_curve_data/0_to_30__500", 5)
High_Min_Data = DataInfo("stress_curve_data/0_to_2000__2000", 100)

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
selected_algorithms = [alg for alg in ALGORITHMS if st.sidebar.checkbox(alg, value=alg != 'UMAP')]

# Plot log(stress) or just NS
st.sidebar.markdown('### Other Options')
y_options = ["Log(Normalized Stress)", "Normalized Stress"]
take_log = st.sidebar.radio("Y-Axis", y_options) == y_options[0]

# Plot Stress Curves
fig = plot_curves(selected_dataset, selected_run, selected_algorithms, take_log, max_x, dataInfo,
                  f"Stress Curves for {selected_dataset} (Run {selected_run})",
                  "log(Normalized Stress)" if take_log else "Normalized Stress"
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
