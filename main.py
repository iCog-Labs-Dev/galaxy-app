# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from galaxy.app import UniverseApplication
from galaxy.model import Dataset, History, HistoryDatasetAssociation
from galaxy.datatypes.data import Text

app = FastAPI(title="Galaxy Web API")

# Load Galaxy backend
config_path = os.path.join(os.path.dirname(__file__), "galaxy.yml")
galaxy_app = UniverseApplication(global_conf={'__file__': config_path})


@app.get("/tools")
def list_tools():
    tools = []
    for tool_id, tool in galaxy_app.toolbox.tools_by_id.items():
        tools.append({
            "id": tool_id,
            "name": tool.name,
            "description": tool.description,
        })
    return tools


class RunToolRequest(BaseModel):
    tool_id: str

## Return Output
@app.post("/run")
def run_tool_with_dataset(req: RunToolRequest):
    tool = galaxy_app.toolbox.get_tool(req.tool_id)
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    # Step 1: Create history
    history = History(name="Web API History")
    galaxy_app.model.context.add(history)
    galaxy_app.model.context.flush()

    # Step 2: Upload input.txt
    file_path = os.path.join(os.path.dirname(__file__), "input.txt")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="input.txt not found")

    dataset = Dataset(extension="txt")
    galaxy_app.model.context.add(dataset)
    galaxy_app.model.context.flush()

    hda_input = HistoryDatasetAssociation(name="API Input", extension="txt", history=history, dataset=dataset)
    hda_input.visible = True
    hda_input.state = "ok"
    hda_input.datatype = Text()
    hda_input.init_meta()
    hda_input.set_dataset_state()
    galaxy_app.model.context.add(hda_input)
    galaxy_app.model.context.flush()

    galaxy_app.object_store.create(hda_input)
    galaxy_app.object_store.update_from_file(hda_input, file_path)
    galaxy_app.model.context.flush()

    # Step 3: Run the tool
    params = {"input1": {"src": "hda", "id": hda_input.id}}
    result = tool.execute(galaxy_app, tool_inputs=params, history=history)

    # Step 4: Extract output HDA
    output_hda = list(result.outputs.values())[0]  # usually first output
    output_file = galaxy_app.object_store.get_filename(output_hda)

    # Step 5: Read output content
    if not os.path.exists(output_file):
        raise HTTPException(status_code=500, detail="Output file not found")

    with open(output_file, "r") as f:
        output_text = f.read()

    return {
        "message": "Tool executed and output fetched successfully.",
        "tool_id": req.tool_id,
        "history_id": history.id,
        "input_dataset_id": hda_input.id,
        "output_dataset_id": output_hda.id,
        "output": output_text
    }
