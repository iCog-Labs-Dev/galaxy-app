# galaxy_app/main.py

import os
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from galaxy_app.models.schemas import RunToolRequest, RunToolResponse
from galaxy.app import UniverseApplication
from galaxy.model import Dataset, History, HistoryDatasetAssociation
from galaxy.datatypes.data import Text

app = FastAPI(
    title="Galaxy Web API",
    description="Interact with the Galaxy backend: list tools, run tools, and retrieve output.",
    version="1.0.0"
)

# === Load Galaxy configuration ===
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "workflow", "galaxy.yml")
DATA_PATH = os.path.join(ROOT_DIR, "data", "input.txt")

# === Initialize Galaxy backend ===
galaxy_app = UniverseApplication(global_conf={'__file__': CONFIG_PATH})
print(" Galaxy backend initialized.")

# === Default root path ===
@app.get("/", tags=["Status"])
def root():
    return {"message": " Tesfalegn Galaxy App is running correctly."}

# === List available tools ===
@app.get("/tools", tags=["Tools"])
def list_tools():
    tools = []
    for tool_id, tool in galaxy_app.toolbox.tools_by_id.items():
        tools.append({
            "id": tool_id,
            "name": tool.name,
            "description": tool.description,
        })
    return tools

# === Run a tool with uploaded dataset ===
@app.post("/run", response_model=RunToolResponse, tags=["Execution"])
def run_tool_with_dataset(req: RunToolRequest):
    tool = galaxy_app.toolbox.get_tool(req.tool_id)
    if tool is None:
        raise HTTPException(status_code=404, detail=" Tool not found")

    # Step 1: Create history
    history = History(name="Web API History")
    galaxy_app.model.context.add(history)
    galaxy_app.model.context.flush()

    # Step 2: Load input.txt
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=400, detail=" input.txt not found in /data")

    dataset = Dataset(extension="txt")
    galaxy_app.model.context.add(dataset)
    galaxy_app.model.context.flush()

    hda_input = HistoryDatasetAssociation(
        name="API Input",
        extension="txt",
        history=history,
        dataset=dataset,
        visible=True,
        state="ok",
        datatype=Text()
    )
    hda_input.init_meta()
    hda_input.set_dataset_state()
    galaxy_app.model.context.add(hda_input)
    galaxy_app.model.context.flush()

    galaxy_app.object_store.create(hda_input)
    galaxy_app.object_store.update_from_file(hda_input, DATA_PATH)
    galaxy_app.model.context.flush()

    # Step 3: Run the tool
    params = {"input1": {"src": "hda", "id": hda_input.id}}
    result = tool.execute(galaxy_app, tool_inputs=params, history=history)

    # Step 4: Fetch output
    output_hda = list(result.outputs.values())[0]
    output_file = galaxy_app.object_store.get_filename(output_hda)

    if not os.path.exists(output_file):
        raise HTTPException(status_code=500, detail=" Output file not found")

    with open(output_file, "r") as f:
        output_text = f.read()

    return {
        "message": " Tool executed and output fetched successfully.",
        "tool_id": req.tool_id,
        "history_id": history.id,
        "input_dataset_id": hda_input.id,
        "output_dataset_id": output_hda.id,
        "output": output_text
    }

# === Customize Swagger Docs ===
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Galaxy App API",
        version="1.0.0",
        description="This API lets you interact with Galaxy: list tools, run a tool, and get results.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
