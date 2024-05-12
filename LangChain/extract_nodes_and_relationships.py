from typing import Tuple, List, Dict
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
from crewai_tools import tool

@tool("Extract Nodes and Relationships")
def extract_nodes_and_relationships(
    text: str,
    model_name: str = "distilgpt2"
) -> Tuple[List[Dict], List[Dict]]:
    """
    Extracts nodes and relationships from unstructured text using a pre-trained language model.

    Args:
        text (str): The unstructured text data to extract nodes and relationships from.
        model_name (str, optional): The name of the pre-trained language model to use. Defaults to "distilgpt2".

    Returns:
        Tuple[List[Dict], List[Dict]]: A tuple containing two lists: the first list contains dictionaries representing the extracted nodes, and the second list contains dictionaries representing the extracted relationships.
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
        nodes, relationships = extract_from_predicted_labels(predicted_labels)

        return nodes, relationships
    except Exception as e:
        return [], [], str(e)

def extract_from_predicted_labels(predicted_labels: str) -> (List[Dict], List[Dict]):
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