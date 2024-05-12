# Create Conversation Graph

This tool uses the ConversationGraph class from LangChain to create a graph visualization of the conversation history. Here's how it works:

The `create_conversation_graph` function takes three arguments:

- `conversation_history` (str): The conversation history to create a graph for.
- `prune` (bool, optional): Whether to prune the graph by removing non-essential nodes. Defaults to False.
- `render` (bool, optional): Whether to render the graph as a PNG image. Defaults to False.

The function first creates a `ConversationGraph` object from the provided `conversation_history` using `ConversationGraph.from_conversation_history`.

- If `prune` is True, the graph is pruned by calling the `prune` method on the graph object.
- If `render` is True, the graph is rendered as a PNG image using the `render` method, and the path to the rendered image (`conversation_graph.png`) is returned.
- If `render` is False, the string representation of the graph is returned.
- If an exception occurs during the process, an error message is returned.

To use this tool with CrewAI, you can create an agent with the `create_conversation_graph` tool like this:

```python
from crewai import Agent

agent = Agent(
    role="Conversation Analyst",
    goal="Analyze and visualize conversation histories",
    backstory="You are an expert in conversation analysis and visualization.",
    tools=[create_conversation_graph],
)
```

Then, you can call the tool within your agent's tasks or during the conversation:

```python
result = agent.run(
    "Create a graph visualization of the following conversation history: ...",
    conversation_history="...",
    prune=True,
    render=True,
)
```

This will create a graph visualization of the provided conversation history, prune the graph, render it as a PNG image, and return the path to the rendered image.

Note that this example assumes you have LangChain installed and set up correctly. Additionally, you may need to install other dependencies, such as graphviz, for rendering the graph successfully.



# Read Conversation Graph

This tool uses the `KnowledgeGraph` class from LangChain to read and display a knowledge graph. Here's how it works:

The `read_knowledge_graph` function takes two arguments:

- `graph_data` (str): The knowledge graph data to display, in GraphML format.
- `render` (bool, optional): Whether to render the graph as a PNG image. Defaults to False.

The function first creates a `KnowledgeGraph` object from the provided `graph_data` using `KnowledgeGraph.from_graphml`.

- If `render` is True, the graph is rendered as a PNG image using the `render` method, and the path to the rendered image (`knowledge_graph.png`) is returned.
- If `render` is False, the string representation of the graph is returned.
- If an exception occurs during the process, an error message is returned.

To use this tool with CrewAI, you can create an agent with the `read_knowledge_graph` tool like this:

```python
from crewai import Agent

agent = Agent(
    role="Knowledge Graph Reader",
    goal="Read and visualize knowledge graphs",
    backstory="You are an expert in knowledge graph analysis and visualization.",
    tools=[read_knowledge_graph],
)
```

Then, you can call the tool within your agent's tasks or during the conversation:

```python
graph_data = "..."  # Replace with your knowledge graph data in GraphML format
result = agent.run(
    "Read and display the following knowledge graph data:",
    graph_data=graph_data,
    render=True,
)
```

This will read the provided knowledge graph data, render it as a PNG image, and return the path to the rendered image.

Note that this example assumes you have LangChain installed and set up correctly. Additionally, you may need to install other dependencies, such as graphviz, for rendering the graph successfully.

# Write To Conversation Graph

This tool uses the `KnowledgeGraph` class from LangChain to write nodes and relationships to a knowledge graph. Here's how it works:

The `write_to_knowledge_graph` function takes four arguments:

- `graph_data` (Optional[str], optional): Existing knowledge graph data in GraphML format. If provided, the new nodes and relationships will be added to the existing graph. Defaults to None.
- `nodes` (Optional[list], optional): A list of node objects to add to the graph. Each node should be a dictionary with keys 'id' and 'type'. Defaults to None.
- `relationships` (Optional[list], optional): A list of relationship objects to add to the graph. Each relationship should be a dictionary with keys 'source', 'target', and 'type'. Defaults to None.
- `output_format` (str, optional): The output format for the graph data. Supported formats are 'graphml', 'json', and 'neo4j'. Defaults to 'graphml'.

The function first creates a `KnowledgeGraph` object. If `graph_data` is provided, it creates the graph from the existing data using `KnowledgeGraph.from_graphml`. Otherwise, it creates an empty graph.

- If `nodes` is provided, it adds each node to the graph using the `add_node` method.
- If `relationships` is provided, it adds each relationship to the graph using the `add_relationship` method.

The updated graph data is returned in the specified `output_format`. If the format is 'graphml', it uses `graph.to_graphml()`. If the format is 'json', it uses `graph.to_json()`. If the format is 'neo4j', it uses `graph.to_neo4j()`.

If an unsupported output format is provided, it raises a `ValueError`.

If an exception occurs during the process, an error message is returned.

To use this tool with CrewAI, you can create an agent with the `write_to_knowledge_graph` tool like this:

```python
from crewai import Agent

agent = Agent(
    role="Knowledge Graph Writer",
    goal="Write and update knowledge graphs",
    backstory="You are an expert in knowledge graph construction and manipulation.",
    tools=[write_to_knowledge_graph],
)
```

Then, you can call the tool within your agent's tasks or during the conversation:

```python
nodes = [
    {"id": "Marie Curie", "type": "Person"},
    {"id": "Pierre Curie", "type": "Person"},
    {"id": "University of Paris", "type": "Organization"},
]

relationships = [
    {"source": "Marie Curie", "target": "Pierre Curie", "type": "SPOUSE"},
    {"source": "Marie Curie", "target": "University of Paris", "type": "WORKED_AT"},
]

result = agent.run(
    "Write the following nodes and relationships to a new knowledge graph:",
    nodes=nodes,
    relationships=relationships,
    output_format="graphml",
)
```

This will write the provided nodes and relationships to a new knowledge graph in GraphML format.

# Extract and Write to Knowledge Graph

This single tool, `extract_and_write_knowledge_graph`, combines the functionality of extracting nodes and relationships from unstructured text using a pre-trained language model and writing the extracted information to a knowledge graph using LangChain. Here's how the tool works:

The `extract_and_write_knowledge_graph` function takes four arguments:

- `text` (str): The unstructured text data to extract nodes and relationships from.
- `graph_data` (Optional[str], optional): Existing knowledge graph data in GraphML format. If provided, the new nodes and relationships will be added to the existing graph.
- `model_name` (str, optional): The name of the pre-trained language model to use. Defaults to "distilgpt2".
- `output_format` (str, optional): The output format for the graph data. Supported formats are 'graphml', 'json', and 'neo4j'. Defaults to 'graphml'.

The function loads the pre-trained language model and tokenizer using the `model_name` argument.
It preprocesses the input text data and generates predicted labels using the pre-trained language model.
The `extract_nodes_and_relationships` helper function is called to extract nodes and relationships from the predicted labels. This implementation assumes a specific format for the predicted labels, but you can modify this function to match the format generated by your pre-trained language model.
If `graph_data` is provided, the function loads the existing knowledge graph data using `KnowledgeGraph.from_graphml`. Otherwise, it creates a new empty graph.
The extracted nodes and relationships are added to the loaded or newly created graph using the `add_node` and `add_relationship` methods.
Finally, the updated knowledge graph data is returned in the specified `output_format` (graphml, json, or neo4j).

To use this tool with CrewAI, you can create an agent with the `extract_and_write_knowledge_graph` tool like this:

```python
from crewai import Agent

agent = Agent(
    role="Knowledge Graph Extractor and Writer",
    goal="Extract knowledge graphs from unstructured text and update existing graphs",
    backstory="You are an expert in extracting structured information from unstructured data and updating knowledge graphs.",
    tools=[extract_and_write_knowledge_graph],
)
```

Then, you can call the tool within your agent's tasks or during the conversation:

```python
text = """
Steve Jobs, co-founder of Apple Inc., was born on February 24, 1955, in San Francisco, California.
He later co-founded Pixar Animation Studios.
Steve Jobs passed away on October 5, 2011, in Palo Alto, California.
"""

existing_graph_data = "..."  # Provide existing graph data in GraphML format, if available

result = agent.run(
    "Extract nodes and relationships from the following text and write them to a knowledge graph:",
    text=text,
    graph_data=existing_graph_data,
    model_name="distilgpt2",
    output_format="graphml",
)
```

This will extract nodes and relationships from the provided text using the `distilgpt2` pre-trained language model, optionally combine them with the existing knowledge graph data (if provided), and return the updated graph data in GraphML format.

Note that the quality of the extracted knowledge graph will depend on the performance of the pre-trained language model and the implementation of the `extract_nodes_and_relationships` function.

Note that the quality of the extracted knowledge graph will depend on the performance of the pre-trained language model and the implementation of the extract_nodes_and_relationships function.

# Extract Nodes and Relationships

This tool, `extract_nodes_and_relationships`, takes two arguments:

- `text` (str): The unstructured text data to extract nodes and relationships from.
- `model_name` (str, optional): The name of the pre-trained language model to use. Defaults to "distilgpt2".

To use these tools with CrewAI, you can create agents with the respective tools like this:

```python
from crewai import Agent

extractor_agent = Agent(
    role="Knowledge Graph Extractor",
    goal="Extract nodes and relationships from unstructured text",
    backstory="You are an expert in extracting structured information from unstructured data.",
    tools=[extract_nodes_and_relationships],
)
```

It loads the pre-trained language model and tokenizer, generates predicted labels from the input text, and calls the `extract_from_predicted_labels` helper function to extract nodes and relationships from the predicted labels. The extracted nodes and relationships are returned as lists of dictionaries.

# Write To Knowledge Graph

This tool, `write_to_knowledge_graph`, takes three arguments:

- `nodes` (List[Dict]): A list of dictionaries representing the nodes to be added to the graph. Each dictionary should have keys 'id' and 'type'.
- `relationships` (List[Dict]): A list of dictionaries representing the relationships to be added to the graph. Each dictionary should have keys 'source', 'target', and 'type'.
- `graph_data` (Optional[str], optional): Existing knowledge graph data in GraphML format. If provided, the new nodes and relationships will be added to the existing graph.
- `output_format` (str, optional): The output format for the graph data. Supported formats are 'graphml', 'json', and 'neo4j'. Defaults to 'graphml'.

```python
from crewai import Agent

writer_agent = Agent(
    role="Knowledge Graph Writer",
    goal="Write nodes and relationships to a knowledge graph",
    backstory="You are an expert in constructing and updating knowledge graphs.",
    tools=[write_to_knowledge_graph],
)
```

It creates or loads the knowledge graph based on the provided `graph_data`, adds the provided nodes and relationships to the graph using the `add_node` and `add_relationship` methods, and returns the updated knowledge graph data in the specified `output_format`.