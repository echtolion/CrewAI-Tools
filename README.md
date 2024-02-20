<h1>CrewAI-Tools</h1>
<p>All untested for now, will test when I can and fix them.</p>
<br>
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
<br>

<br>
<h2> Screen Shot Website </h2>
<p>To make this tool available for agents to use within CrewAI, you would then assign this tool to an agent like so:</p>

```python

from crewai import CrewAI, Agent, Task
from my_screenshot_tool import MyScreenshotTool  # Import your tool class

# Define the ScreenshotTask which utilizes the take_screenshots_from_excel tool
class ScreenshotTask(Task):
    def __init__(self, file_path, save_path):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path

    def execute(self, agent: Agent):
        # Use the take_screenshots_from_excel tool from the agent's toolbox
        return agent.tools.take_screenshots_from_excel(self.file_path, self.save_path)

# Define a CrewAI agent that includes the take_screenshots_from_excel tool
class ScreenshotAgent(Agent):
    def __init__(self):
        super().__init__(name="ScreenshotAgent")
        self.tools.register("take_screenshots_from_excel", MyScreenshotTool.take_screenshots_from_excel)  # Register the tool

# Initialize the CrewAI framework and add the agent
crew_ai = CrewAI()
screenshot_agent = ScreenshotAgent()
crew_ai.register_agent(screenshot_agent)

# Define a task with the file path and save path for screenshots
file_path = "path/to/your/excel/file.xlsx"  # Replace with the actual file path
save_path = "path/to/save/screenshots"  # Replace with the actual save path
screenshot_task = ScreenshotTask(file_path, save_path)

# Assign the task to the agent and execute
crew_ai.assign_task(screenshot_task, screenshot_agent.name)
results = crew_ai.execute()

# Print the file paths to the saved screenshots
print("Screenshot Results:")
for idx, screenshot_path in enumerate(results):
    print(f"Screenshot {idx + 1}: {screenshot_path}")

```

<p>or you can do this.</p>

```python

from crewai import Agent
from langchain.agents import Tool
from my_screenshot_tool import MyScreenshotTool  # Import your tool class

# Create the screenshot_tool as a Tool object
screenshot_tool = Tool(
    name="TakeScreenshotsTool",
    func=MyScreenshotTool.take_screenshots_from_excel,
    description="Takes screenshots of websites listed in an Excel file."
)

# Define an agent and assign the screenshot_tool
screenshot_agent = Agent(
    role='Screenshot Taker',
    goal='Capture screenshots of websites',
    backstory='An agent tasked with capturing screenshots of websites listed in an Excel file.',
    tools=[screenshot_tool],
    verbose=True
)

# In this setup, screenshot_agent is an agent that has been equipped with the screenshot_tool.
# This agent can now use this tool to capture screenshots of websites autonomously as part of its tasks within a CrewAI setup.
```

<h2>Search and Extract Content</h2>
<p>To make this tool available for agents to use within CrewAI, you would then assign this tool to an agent like so:</p>

```python
from crewai import Agent
from langchain.agents import Tool
from path.to.google_search_tool import GoogleSearchTool

# Create the GoogleSearchTool as a Tool object
google_search_tool = Tool(
    name="GoogleSearchTool",
    func=GoogleSearchTool,
    description="Performs a Google search and extracts content from the search results."
)

# Define an agent and assign the GoogleSearchTool
google_search_agent = Agent(
    role='SearchEngineUser',
    goal='Perform Google searches and extract content',
    backstory='An agent tasked with searching Google and extracting content for analysis.',
    tools=[google_search_tool],
    verbose=True
)

# In this setup, google_search_agent is an agent equipped with the GoogleSearchTool.
# This agent can now use this tool to perform Google searches and extract content as part of its tasks within a CrewAI setup.

```

<p>or with langchain like this</p>

```python

from langchain import LangChain, Agent, Task
from langchain.tools import Tool
from path.to.google_search_tool import GoogleSearchTool

# Define the GoogleSearchTask which utilizes the GoogleSearchTool
class GoogleSearchTask(Task):
    def __init__(self, search_query, save_path='./', filename='search_results.json'):
        super().__init__()
        self.search_query = search_query
        self.save_path = save_path
        self.filename = filename

    def execute(self, agent: Agent):
        # Use the GoogleSearchTool from the agent's toolbox
        return agent.tools.GoogleSearchTool.execute(self.search_query, self.save_path, self.filename)

# Define a LangChain agent that includes the GoogleSearchTool
class GoogleSearchAgent(Agent):
    def __init__(self):
        super().__init__(name="GoogleSearchAgent")
        self.tools.register("GoogleSearchTool", GoogleSearchTool())  # Register the tool

# Initialize the LangChain framework and add the agent
lang_chain = LangChain()
google_search_agent = GoogleSearchAgent()
lang_chain.register_agent(google_search_agent)

# Define a task with the search query and save path for search results
search_query = "your search query"
save_path = "path/to/save/search_results"
search_results_filename = "search_results.json"
google_search_task = GoogleSearchTask(search_query, save_path, search_results_filename)

# Assign the task to the agent and execute
lang_chain.assign_task(google_search_task, google_search_agent.name)
results = lang_chain.execute()

# Print the file path to the saved search results
print("Search Results File Path:")
print(results)

```
