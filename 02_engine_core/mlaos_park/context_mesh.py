import hashlib
from typing import Dict, Any, List, Optional
from .models import ContextNode, ProvenanceTuple, AuthorityLevel

class ContextualIntelligenceMesh:
    def __init__(self):
        self.nodes: Dict[str, ContextNode] = {}

    def ingest_context(self, node_type: str, uri: str, content: str, source_desc: str) -> ContextNode:
        content_hash = "0x" + hashlib.sha256(content.encode()).hexdigest().upper()
        prov = ProvenanceTuple(
            source_uri=uri,
            merkle_hash=content_hash,
            confidence_interval=0.98,
            authority_level=AuthorityLevel.OBSERVER
        )
        node = ContextNode(
            node_id=f"CIM_{hashlib.sha256(uri.encode()).hexdigest()[:12]}",
            node_type=node_type,
            uri=uri,
            content_hash=content_hash,
            provenance=prov
        )
        self.nodes[node.node_id] = node
        return node
