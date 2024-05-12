from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.graphs import KnowledgeGraph
from crewai_tools import tool
import re

@tool("Extract and Write Knowledge Graph")
def extract_and_write_knowledge_graph(
    text: str,
    graph_data: Optional[str] = None,
    model_name: str = "distilgpt2",
    output_format: str = "graphml"
) -> str:
    """
    Extracts nodes and relationships from unstructured text using a pre-trained language model,
    and writes the extracted information to a knowledge graph, optionally combining with existing graph data.

    Args:
        text (str): The unstructured text data to extract nodes and relationships from.
        graph_data (Optional[str], optional): Existing knowledge graph data in GraphML format. If provided, the new nodes and relationships will be added to the existing graph. Defaults to None.
        model_name (str, optional): The name of the pre-trained language model to use. Defaults to "distilgpt2".
        output_format (str, optional): The output format for the graph data. Supported formats are 'graphml', 'json', and 'neo4j'. Defaults to 'graphml'.

    Returns:
        str: The updated knowledge graph data in the specified output format.
    """
    try:
        # Load the pre-trained model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        # Preprocess the data
        inputs = tokenizer(text, return_tensors="pt")

        # Use the model to predict labels
        outputs = model.generate(**inputs)
        predicted_labels = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract nodes and relationships based on predicted labels
        nodes, relationships = extract_nodes_and_relationships(predicted_labels)

        # Create or load the knowledge graph
        if graph_data:
            graph = KnowledgeGraph.from_graphml(graph_data)
        else:
            graph = KnowledgeGraph()

        # Add the extracted nodes and relationships to the graph
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

def extract_nodes_and_relationships(predicted_labels: str) -> (list, list):
    """
    Helper function to extract nodes and relationships from the predicted labels.
    This implementation assumes the predicted labels follow the format:
    "NODE: <node_id> (<node_type>) RELATIONSHIP: <relationship_type> NODE: <node_id> (<node_type>)"
    """
    nodes = []
    relationships = []

    # Split the predicted labels into individual statements
    statements = re.split(r'\s*\n\s*', predicted_labels.strip())

    for statement in statements:
        # Extract node information
        node_matches = re.findall(r'NODE: (\S+) \((\S+)\)', statement)
        if len(node_matches) == 2:
            node1 = {"id": node_matches[0][0], "type": node_matches[0][1]}
            node2 = {"id": node_matches[1][0], "type": node_matches[1][1]}
            nodes.extend([node1, node2])

            # Extract relationship information
            relationship_match = re.search(r'RELATIONSHIP: (\S+)', statement)
            if relationship_match:
                relationship_type = relationship_match.group(1)
                relationship = {
                    "source": node1["id"],
                    "target": node2["id"],
                    "type": relationship_type
                }
                relationships.append(relationship)

    return list(set(nodes)), list(set(relationships))