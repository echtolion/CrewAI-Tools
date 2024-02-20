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
<h2>Take Screenshots from Excel</h2>
<p>Define the <strong>ScreenshotTask</strong> which utilizes the <em>take_screenshots_from_excel</em> tool.</p>

```python

from crewai import CrewAI, Agent, Task
from my_screenshot_tool import MyScreenshotTool  # Import your tool class

class ScreenshotTask(Task):
    def __init__(self, file_path, save_path):
        super().__init__()
        self.file_path = file_path
        self.save_path = save_path

    def execute(self, agent: Agent):
        return agent.tools.take_screenshots_from_excel(self.file_path, self.save_path)

class ScreenshotAgent(Agent):
    def __init__(self):
        super().__init__(name="ScreenshotAgent")
        self.tools.register("take_screenshots_from_excel", MyScreenshotTool.take_screenshots_from_excel)  # Register the tool

crew_ai = CrewAI()
screenshot_agent = ScreenshotAgent()
crew_ai.register_agent(screenshot_agent)

file_path = "path/to/your/excel/file.xlsx"
save_path = "path/to/save/screenshots"
screenshot_task = ScreenshotTask(file_path, save_path)

crew_ai.assign_task(screenshot_task, screenshot_agent.name)
results = crew_ai.execute()

print("Screenshot Results:")
for idx, screenshot_path in enumerate(results):
    print(f"Screenshot {idx + 1}: {screenshot_path}")

```

<br>

<h2>Capture Screenshots of Websites</h2>
<p>Define an agent and assign the <em>screenshot_tool</em>.</p>

```python

from crewai import Agent
from langchain.agents import Tool
from my_screenshot_tool import MyScreenshotTool  # Import your tool class

screenshot_tool = Tool(
    name="TakeScreenshotsTool",
    func=MyScreenshotTool.take_screenshots_from_excel,
    description="Takes screenshots of websites listed in an Excel file."
)

screenshot_agent = Agent(
    role='Screenshot Taker',
    goal='Capture screenshots of websites',
    backstory='An agent tasked with capturing screenshots of websites listed in an Excel file.',
    tools=[screenshot_tool],
    verbose=True
)
```


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
