from typing import Optional
from langchain.graphs import KnowledgeGraph
from crewai_tools import tool

@tool("Read Knowledge Graph")
def read_knowledge_graph(graph_data: str, render: bool = False) -> Optional[str]:
    """
    Displays the given knowledge graph data.
    
    Args:
        graph_data (str): The knowledge graph data to display.
        render (bool, optional): Whether to render the graph as a PNG image. Defaults to False.
        
    Returns:
        Optional[str]: The path to the rendered PNG image if render is True, otherwise None.
    """
    try:
        graph = KnowledgeGraph.from_graphml(graph_data)
        
        if render:
            image_path = "knowledge_graph.png"
            graph.render(image_path)
            return image_path
        else:
            return str(graph)
    except Exception as e:
        return f"An error occurred: {e}"