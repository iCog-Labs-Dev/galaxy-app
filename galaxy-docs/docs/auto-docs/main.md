# Documentation for `main`

## Functions

### Function `root` (line 28)
- Arguments: None
- Calls: app.get
_No docstring provided._

### Function `list_tools` (line 33)
- Arguments: None
- Calls: app.get, galaxy_app.toolbox.tools_by_id.items, tools.append
_No docstring provided._

### Function `run_tool_with_dataset` (line 45)
- Arguments: req
- Calls: app.post, galaxy_app.toolbox.get_tool, History, galaxy_app.model.context.add, galaxy_app.model.context.flush, Dataset, galaxy_app.model.context.add, galaxy_app.model.context.flush, HistoryDatasetAssociation, hda_input.init_meta, hda_input.set_dataset_state, galaxy_app.model.context.add, galaxy_app.model.context.flush, galaxy_app.object_store.create, galaxy_app.object_store.update_from_file, galaxy_app.model.context.flush, tool.execute, galaxy_app.object_store.get_filename, HTTPException, os.path.exists, HTTPException, list, os.path.exists, HTTPException, open, f.read, Text, result.outputs.values
_No docstring provided._

### Function `custom_openapi` (line 105)
- Arguments: None
- Calls: get_openapi
_No docstring provided._
