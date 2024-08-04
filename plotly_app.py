import streamlit as st
import plotly.graph_objects as go
import numpy as np
import trimesh

st.title("Point Cloud Visualization")

# Utility functions to plot mesh and transforms
def get_scene_dict():
    return dict(
        xaxis=dict(title="X"),
        yaxis=dict(title="Y"),
        zaxis=dict(title="Z"),
        aspectmode="data",
    )

def plot_mesh(mesh, color="lightpink"):
    vertices = mesh.vertices
    faces = mesh.faces

    mesh_plot = go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        color=color,
        opacity=0.5,
        name="Mesh",
    )

    layout = go.Layout(
        scene=get_scene_dict(),
        showlegend=True,
        title="Mesh",
    )

    fig = go.Figure(data=[mesh_plot], layout=layout)
    return fig

def plot_point_cloud(points, colors=None, size=4):
    if colors is None:
        colors = points[:, 2]

    scatter_plot = go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode="markers",
        marker=dict(
            size=size,
            color=colors,
            colorscale="viridis",
            colorbar=dict(title="Density Scale"),
        ),
        name="Point Cloud",
    )

    layout = go.Layout(
        scene=get_scene_dict(),
        showlegend=True,
        title="Point Cloud",
    )

    fig = go.Figure(data=[scatter_plot], layout=layout)
    return fig

# Generate sample data
mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
point_cloud = np.random.rand(1000, 3) - 0.5

# Display the mesh
st.subheader("Mesh Visualization")
fig_mesh = plot_mesh(mesh)
st.plotly_chart(fig_mesh)

# Display the point cloud
st.subheader("Point Cloud Visualization")
fig_point_cloud = plot_point_cloud(point_cloud)
st.plotly_chart(fig_point_cloud)

# Interactive filtering by point size
point_size = st.slider("Point Size", 1, 10, 4)
fig_point_cloud_interactive = plot_point_cloud(point_cloud, size=point_size)
st.plotly_chart(fig_point_cloud_interactive)
