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



