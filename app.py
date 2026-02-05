import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

from langchain.chat_models import init_chat_model
model = init_chat_model("google_genai:gemini-2.5-flash")

import requests
import pathlib 
url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists.")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"{local_path} downloaded")
    else:
        print(f"failed to download. Status Code {response.status_code}")


from langchain_community.utilities import SQLDatabase 
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(f"Dilect{db.dialect}")
print(f"Available Tables{db.get_usable_table_names()}")
print(f"Sample Output{db.run('SELECT * FROM Artist LIMIT 5;')}")

from langchain_community.agent_toolkits import SQLDatabaseToolkit 
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()
for tool in tools:
    print(f"{tool.name}: {tool.description}")

system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables. 
""".format(
    dialect = db.dialect,
    top_k = 5,
)


from langchain.agents import create_agent 
agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)

question = "Which genre on average has the longest tracks?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()

