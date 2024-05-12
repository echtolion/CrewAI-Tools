from typing import Optional, List, Dict
from langchain.graphs import KnowledgeGraph
from crewai_tools import tool

@tool("Write to Knowledge Graph")
def write_to_knowledge_graph(
    nodes: List[Dict],
    relationships: List[Dict],
    graph_data: Optional[str] = None,
    output_format: str = "graphml"
) -> str:
    """
    Writes the provided nodes and relationships to a knowledge graph, optionally combining with existing graph data.

    Args:
        nodes (List[Dict]): A list of dictionaries representing the nodes to be added to the graph. Each dictionary should have keys 'id' and 'type'.
        relationships (List[Dict]): A list of dictionaries representing the relationships to be added to the graph. Each dictionary should have keys 'source', 'target', and 'type'.
        graph_data (Optional[str], optional): Existing knowledge graph data in GraphML format. If provided, the new nodes and relationships will be added to the existing graph. Defaults to None.
        output_format (str, optional): The output format for the graph data. Supported formats are 'graphml', 'json', and 'neo4j'. Defaults to 'graphml'.

    Returns:
        str: The updated knowledge graph data in the specified output format.
    """
    try:
        # Create or load the knowledge graph
        if graph_data:
            graph = KnowledgeGraph.from_graphml(graph_data)
        else:
            graph = KnowledgeGraph()

        # Add the provided nodes and relationships to the graph
        for node in nodes:
            graph.add_node(node["id"], node["type"])
        for relationship in relationships:
            source = relationship["source"]
            target = relationship["target"]
            relation_type = relationship["type"]
            graph.add_relationship(source, target, relation_type)

        # Return the updated knowledge graph data in the specified output format
        if output_format == "graphml":
            return graph.to_graphml()
        elif output_format == "json":
            return graph.to_json()
        elif output_format == "neo4j":
            return graph.to_neo4j()
        else:
            raise ValueError("Unsupported output format. Supported formats are 'graphml', 'json', and 'neo4j'.")
    except Exception as e:
        return f"An error occurred: {e}"