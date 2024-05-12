from typing import Optional
from langchain.graphs import KnowledgeGraph
from crewai_tools import tool

@tool("Write to Knowledge Graph")
def write_to_knowledge_graph(
    graph_data: Optional[str] = None,
    nodes: Optional[list] = None,
    relationships: Optional[list] = None,
    output_format: str = "graphml"
) -> str:
    """
    Writes nodes and relationships to a knowledge graph.
    
    Args:
        graph_data (Optional[str], optional): Existing knowledge graph data in GraphML format. If provided, the new nodes and relationships will be added to the existing graph. Defaults to None.
        nodes (Optional[list], optional): A list of node objects to add to the graph. Each node should be a dictionary with keys 'id' and 'type'. Defaults to None.
        relationships (Optional[list], optional): A list of relationship objects to add to the graph. Each relationship should be a dictionary with keys 'source', 'target', and 'type'. Defaults to None.
        output_format (str, optional): The output format for the graph data. Supported formats are 'graphml', 'json', and 'neo4j'. Defaults to 'graphml'.
        
    Returns:
        str: The updated knowledge graph data in the specified output format.
    """
    try:
        if graph_data:
            graph = KnowledgeGraph.from_graphml(graph_data)
        else:
            graph = KnowledgeGraph()
        
        if nodes:
            for node in nodes:
                graph.add_node(node["id"], node["type"])
        
        if relationships:
            for relationship in relationships:
                source = relationship["source"]
                target = relationship["target"]
                relation_type = relationship["type"]
                graph.add_relationship(source, target, relation_type)
        
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