<h2>Search and Extract Content</h2>
<p>To make this tool available for agents to use within CrewAI, you would then assign this tool to an agent like so:</p>
<p><strong>Install Dependencies:</strong> Ensure you have installed both CrewAI and Undetected Chrome Driver as outlined in the previous steps.
<br>
<strong>Define the Tool Class:</strong> The GoogleSearchTool class should be defined within your project. Make sure it includes the necessary functionality to perform Google searches and extract content as you desire.</p>

<p>Integrate with CrewAI:</p>

```python
from crewai import CrewAI, Agent, Task
from langchain.agents import Tool
from path.to.google_search_tool import GoogleSearchTool

# Define the GoogleSearchTool as a Tool object
google_search_tool = Tool(
    name="GoogleSearchTool",
    func=GoogleSearchTool,
    description="Performs a Google search and extracts content from the search results."
)

# Define a CrewAI agent that includes the GoogleSearchTool
google_search_agent = Agent(
    role='SearchEngineUser',
    goal='Perform Google searches and extract content',
    backstory='An agent tasked with searching Google and extracting content for analysis.',
    tools=[google_search_tool],
    verbose=True
)

# Initialize the CrewAI framework and add the agent
crew_ai = CrewAI()
crew_ai.register_agent(google_search_agent)

```

<p><strong>Define and Assign Tasks:</strong> Now that the google_search_agent is equipped with the GoogleSearchTool, you can define tasks and assign them to the agent for execution.</p>


```python

# Define a task with the search query
search_query = "your search query"
google_search_task = Task(
    name="GoogleSearchTask",
    func=google_search_agent.tools.GoogleSearchTool.execute,
    args=[search_query]
)

# Assign the task to the agent and execute
crew_ai.assign_task(google_search_task, google_search_agent.name)
results = crew_ai.execute()

# Print the results (file path to the saved search results)
print("Search Results File Path:")
print(results)

```

<p><strong>Execute Tasks and Retrieve Results:</strong> After assigning tasks to the agent and executing them, you can retrieve the results. In this example, we print the file path to the saved search results.
<br><br>
<strong>Run the Code:</strong> Execute your Python script containing the CrewAI integration code. Make sure all paths and configurations are correctly set.
<br><br>
With these steps, you should be able to integrate the GoogleSearchTool with CrewAI and utilize it to perform Google searches and extract content. Adjust the code and configurations as needed to fit your specific use case and environment.</p>

<br><BR>