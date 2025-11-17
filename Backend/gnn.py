# backend/gnn/gnn_mapper.py
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import networkx as nx
import json

class DisinfoGNN:
    def __init__(self):
        self.model = self._build_gcn()
        
    def _build_gcn(self):
        class GCN(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.conv1 = GCNConv(16, 32)
                self.conv2 = GCNConv(32, 2)
            def forward(self, x, edge_index):
                x = self.conv1(x, edge_index).relu()
                x = self.conv2(x, edge_index)
                return torch.softmax(x, dim=1)
        return GCN()

    def simulate_graph(self, seed_post_id: str):
        # Simulate a disinfo network (in real system: pull from Twitter API)
        G = nx.barabasi_albert_graph(50, 3)
        for i, node in enumerate(G.nodes()):
            G.nodes[node]['post_id'] = f"post_{i}"
            G.nodes[node]['is_source'] = (i == 0)
            G.nodes[node]['features'] = torch.randn(16).tolist()
        
        # Convert to PyG
        edge_index = torch.tensor(list(G.edges())).t().contiguous()
        x = torch.tensor([G.nodes[n]['features'] for n in G.nodes()], dtype=torch.float)
        data = Data(x=x, edge_index=edge_index)
        
        # Run GNN
        with torch.no_grad():
            out = self.model(data.x, data.edge_index)
            risk_scores = out[:, 1].tolist()  # probability of being malicious actor
        
        # Build JSON for frontend
        nodes = [
            {
                "id": str(i),
                "post_id": G.nodes[i]['post_id'],
                "risk": round(risk_scores[i], 2),
                "is_source": G.nodes[i]['is_source']
            }
            for i in G.nodes()
        ]
        edges = [{"from": str(u), "to": str(v)} for u, v in G.edges()]
        
        return {"nodes": nodes, "edges": edges}