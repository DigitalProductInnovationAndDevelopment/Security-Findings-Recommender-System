"""
Module: ai.Clustering.AgglomerativeClustering
Description: Implements Agglomerative Clustering for VulnerabilityReport
"""

from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from kneed import KneeLocator
import plotly.express as px
import pandas as pd

import logging

logger = logging.getLogger(__name__)


class AgglomerativeClusterer:
    def __init__(self, vulnerability_report):
        self.vulnerability_report = vulnerability_report
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _find_optimal_clusters(self, embeddings):
        """
        Find the optimal number of clusters using the elbow method and silhouette analysis.
        """
        max_clusters = len(self.vulnerability_report.get_findings()) // 4
        inertias = []
        silhouette_scores = []

        for k in range(2, max_clusters + 1):
            clustering = AgglomerativeClustering(n_clusters=k)
            cluster_labels = clustering.fit_predict(embeddings)

            # Calculate inertia manually
            inertia = 0
            for i in range(k):
                cluster_points = embeddings[cluster_labels == i]
                centroid = cluster_points.mean(axis=0)
                inertia += ((cluster_points - centroid) ** 2).sum()

            inertias.append(inertia)
            silhouette_scores.append(silhouette_score(embeddings, cluster_labels))

        # Elbow method
        if len(inertias) > 0:
            kl = KneeLocator(range(2, max_clusters + 1), inertias, curve="convex", direction="decreasing")
            optimal_clusters_elbow = kl.elbow
        else:
            optimal_clusters_elbow = None

        # Silhouette analysis
        if len(silhouette_scores) > 0:
            optimal_clusters_silhouette = max(range(2, max_clusters + 1), key=lambda k: silhouette_scores[k - 2])
        else:
            optimal_clusters_silhouette = None

        # Choose the optimal number of clusters based on your preference
        if optimal_clusters_elbow is not None:
            optimal_clusters = optimal_clusters_elbow
        elif optimal_clusters_silhouette is not None:
            optimal_clusters = optimal_clusters_silhouette
        else:
            # Default to 2 clusters if no optimal number is found
            optimal_clusters = 2

        logger.info(f'Optimal number of clusters: {optimal_clusters}')

        return optimal_clusters

    def add_unsupervised_category(self, use_solution=False):
        """
        Apply Agglomerative Clustering to the findings and assign cluster labels.

        :param use_solution: Whether to use the solution as input for clustering.
        """
        findings = self.vulnerability_report.get_findings()
        descriptions = [finding.solution.short_description if use_solution else ' '.join(finding.description) for
                        finding
                        in findings]

        # Text embedding
        embeddings = self.model.encode(descriptions)

        # Find optimal number of clusters
        optimal_clusters = self._find_optimal_clusters(embeddings)

        # Normalize embeddings
        scaler = StandardScaler()
        normalized_embeddings = scaler.fit_transform(embeddings)

        # Apply Agglomerative Clustering
        clustering = AgglomerativeClustering(n_clusters=optimal_clusters)
        cluster_labels = clustering.fit_predict(normalized_embeddings)

        # Assign cluster labels to findings
        for finding, label in zip(findings, cluster_labels):
            finding.set_unsupervised_cluster(label)

    def get_cluster_graph(self):
        """
        Generate an interactive 3D scatter plot of the clustered findings.
        """
        findings = self.vulnerability_report.get_findings()
        descriptions = [' '.join(finding.description) for finding in findings]
        embeddings = self.model.encode(descriptions)

        pca = PCA(n_components=3)
        embeddings_pca = pca.fit_transform(embeddings)

        df_plot = pd.DataFrame({
            'PC1': embeddings_pca[:, 0],
            'PC2': embeddings_pca[:, 1],
            'PC3': embeddings_pca[:, 2],
            'Cluster': [finding.unsupervised_cluster for finding in findings],
            'Severity': [finding.severity for finding in findings],
            'Solution': [finding.solution.short_description if finding.solution else '' for finding in findings]
        })

        fig = px.scatter_3d(df_plot, x='PC1', y='PC2', z='PC3', color='Cluster', symbol='Cluster',
                            hover_data={'Severity': True, 'Cluster': True, 'Solution': True},
                            title='Interactive 3D Visualization of Clustered Findings')

        fig.update_layout(scene=dict(xaxis_title='PC1', yaxis_title='PC2', zaxis_title='PC3'))

        return fig
