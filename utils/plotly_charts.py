import plotly.graph_objects as go
import os
import numpy as np
from utils.datainfo import DataInfo

ALGORITHMS = ['TSNE', 'UMAP', 'RANDOM', 'MDS']
ALG_NAMES = dict(zip(ALGORITHMS, ['t-SNE', 'UMAP', 'Random', 'MDS']))
ALG_COLORS = {
    'TSNE' : 'darkblue',
    'UMAP' : 'purple',
    'MDS' : 'darkred',
    'RANDOM' : 'darkgreen',
}

def plot_curves(
        dataset: str, 
        run: int, 
        selected_algorithms, 
        take_log: bool,
        max_x: float, 
        dataInfo: DataInfo,
        title_name: str,
        y_axis_name: str
        
        ):
    fig = go.Figure()
    
    for alg in selected_algorithms:
        filename = f"{dataset}_{alg}_{run}.npy"
        filepath = os.path.join(dataInfo.data_dir, filename)
        
        if os.path.exists(filepath):
            data = np.load(filepath)
            # Filter data based on x_limit
            mask = dataInfo.scales <= max_x
            if take_log:
                y = np.log(data[mask])
            else:
                y = data[mask]
            fig.add_trace(go.Scatter(
                x=dataInfo.scales[mask],
                y=y,
                name=ALG_NAMES[alg],
                line=dict(color=ALG_COLORS[alg])
            ))
        else:
            return None
    
    fig.update_layout(
        title=title_name,
        xaxis_title="Scale",
        yaxis_title=y_axis_name,
        template="plotly_white",
        height=600,
        # paper_bgcolor='white', # if not dark_mode else 'rgba(17,17,17,1)',  # transparent background
        # plot_bgcolor='white', # if not dark_mode else 'rgba(17,17,17,1)',  # transparent or dark background
        # font=dict(
        #     color='black' # if not dark_mode else 'white'
        # )
    )
    
    return fig


def plot_embedding(filepath: str, labels: np.ndarray, alg):
    if os.path.exists(filepath):
        embedding = np.load(filepath)
        
    fig = go.Figure()

    marker_dict = dict(
        size=8,
        opacity=0.6,
        showscale=False  # Don't show the colorbar
    )
    if labels is not None: # Different colors for clusters
        marker_dict.update(dict(
            color=labels,
            colorscale='thermal'
        ))

    fig.add_trace(go.Scatter(
        x=embedding[:, 0],
        y=embedding[:, 1],
        mode='markers',
        marker=marker_dict,
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"{ALG_NAMES[alg]} Embedding",
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(
                color='black',
                size=16
            )
        ),
        template="plotly_white",
        height=400,
        width=400,
        showlegend=False,
        # Make the plot square
        xaxis=dict(
            scaleanchor="y", 
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            scaleanchor="x", 
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        # Add white background and border
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

def plot_embeddings(dataset, run, algs):
    labels_path = f"dataset_labels/{dataset}.npy"
    if os.path.exists(labels_path):
        labels = np.load(labels_path)
    else:
        labels = None
    
    figs = dict()
    for alg in algs:
        filename = f"{dataset}_{alg}_{run}.npy"
        filepath = f"embeddings/{filename}"

        if os.path.exists(filepath):
            figs[alg] = plot_embedding(filepath, labels, alg=alg)
        else:
            figs[alg] = None

    return figs

