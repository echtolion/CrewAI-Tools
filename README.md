# CrewAI-Tools

<h2>Auto Skills</h2>
```python
# Tools for CrewAI

# To make this tool available for agents to use within CrewAI, you would then assign this tool to an agent like so:

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

