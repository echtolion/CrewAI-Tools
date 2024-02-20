<h1>CrewAI-Tools</h1>

<h2>Auto Skills</h2>
<p>To make this tool available for agents to use within CrewAI, you would then assign this tool to an agent like so:</p>

```python
# python

from crewai import Agent
from langchain.agents import Tool

# Create the autogen_skill_tool as a Tool object
autogen_skill = Tool(
    name="AutogenSkillTool",
    func=autogen_skill_tool,
    description="Generates Python code for a tool based on a skill description."
)

# Define an agent and assign the autogen_skill_tool
developer_agent = Agent(
    role='Developer',
    goal='Generate Python tools based on skill descriptions',
    backstory='An AI developer capable of translating skill descriptions into executable Python tools.',
    tools=[autogen_skill],
    verbose=True
)

# In this setup, developer_agent is an agent that has been equipped with the autogen_skill_tool. This agent can now use this tool to generate Python functions based on skill descriptions autonomously as part of its tasks within a CrewAI setup.
```

<br>
<h2>Google People Also Searched</h2>
<p>To make this tool available for agents to use within CrewAI, you would then assign this tool to an agent like so:</p>
<br>

```python

from crewai import CrewAI, Agent, Task

# Define the SearchAndAnalyzeTask which utilizes the search_and_analyze tool
class SearchAndAnalyzeTask(Task):
    def __init__(self, keywords):
        super().__init__()
        self.keywords = keywords

    def execute(self, agent: Agent):
        # Use the search_and_analyze tool from the agent's toolbox
        return agent.tools.search_and_analyze(self.keywords)

# Define a CrewAI agent that includes the search_and_analyze tool
class SearchAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(name="SearchAnalysisAgent")
        self.tools.register("search_and_analyze", search_and_analyze)  # Register the tool

# Initialize the CrewAI framework and add the agent
crew_ai = CrewAI()
search_analysis_agent = SearchAnalysisAgent()
crew_ai.register_agent(search_analysis_agent)

# Define a task with a list of keywords to search
keywords = ["OpenAI", "Langchain", "CrewAI"]
search_task = SearchAndAnalyzeTask(keywords)

# Assign the task to the agent and execute
crew_ai.assign_task(search_task, search_analysis_agent.name)
results = crew_ai.execute()

# Print the analysis results
print("Search and Analysis Results:")
for keyword, analysis in results.items():
    print(f"Keyword: {keyword}, Analysis: {analysis}")
```
<br><br>
<h2> Screen Shot Website </h2>
<p>To make this tool available for agents to use within CrewAI, you would then assign this tool to an agent like so:</p>

```python

from crewai import Agent
from my_screenshot_tool import MyScreenshotTool  # Import your tool class

# Set the file path to the Excel file containing URLs
file_path = "path/to/your/excel/file.xlsx"  # Replace with the actual file path

# Set the directory path where screenshots will be saved
save_path = "path/to/save/screenshots"  # Replace with the actual save path

# Create an instance of MyScreenshotTool
my_tool = MyScreenshotTool()

# Define your agent
agent = Agent(
    role='Screenshot Taker',
    goal='Capture screenshots of websites',
    backstory='An agent tasked with capturing screenshots of websites listed in an Excel file.',
    tools=[my_tool.take_screenshots_from_excel],  # Assign your tool to the agent
    verbose=True
)

# Use the tool within the agent
result = agent.use_tool("Take website screenshots", file_path, save_path)

# Print the file paths to the saved screenshots
print(result)
```
