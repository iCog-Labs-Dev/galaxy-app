# explorer.py
import os
from galaxy.app import UniverseApplication
from galaxy.model import Dataset, History, HistoryDatasetAssociation


def list_tools(app, keyword=None):
    print("\n Matching Tools:\n")
    for tool_id, tool in app.toolbox.tools_by_id.items():
        if keyword is None or keyword.lower() in tool_id.lower() or keyword.lower() in tool.name.lower():
            print(f"  ID: {tool_id}")
            print(f"  Name: {tool.name}")
            print(f"  Description: {tool.description}")
            print("   ─" * 10)


def run_tool_with_dataset(app):
    tool_id = input("\n Enter Tool ID to run (e.g., cat1): ").strip()
    tool = app.toolbox.get_tool(tool_id)
    if tool is None:
        print(" Tool not found.")
        return

    # Step 1: Create a history
    history = History(name="Test History")
    app.model.context.add(history)
    app.model.context.flush()
    print(f" Created history: {history.name} (ID: {history.id})")

    # Step 2: Upload a dummy dataset
    file_path = os.path.join(os.path.dirname(__file__), "input.txt")
    if not os.path.exists(file_path):
        print(" input.txt not found.")
        return

    dataset = Dataset()
    dataset.extension = "txt"
    app.model.context.add(dataset)
    app.model.context.flush()

    hda = HistoryDatasetAssociation(name="Test Input", extension="txt", history=history, dataset=dataset)
    hda.visible = True
    hda.state = "ok"
    hda.init_meta()
    app.model.context.add(hda)
    app.model.context.flush()

    app.object_store.create(hda)
    app.object_store.update_from_file(hda, file_path)
    app.model.context.flush()

    print(f" Uploaded dataset: {hda.name} (ID: {hda.id})")

    # Step 3: Run the tool (FIXED HERE)
    print(" Running tool with uploaded dataset...")
    params = {"input1": {"src": "hda", "id": hda.id}}
    result = tool.execute(app, incoming=params, history=history)

    print(" Tool execution result:")
    print(result)


def main():
    config_path = os.path.join(os.path.dirname(__file__), "galaxy.yml")
    print(" Starting Galaxy backend...")
    app = UniverseApplication(global_conf={'__file__': config_path})
    print(" Galaxy backend loaded.\n")

    while True:
        print("\n MENU")
        print("1. List all tools")
        print("2. Search tool by keyword")
        print("3. Run tool with dataset")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            list_tools(app)
        elif choice == "2":
            keyword = input("Enter keyword to search: ")
            list_tools(app, keyword)
        elif choice == "3":
            run_tool_with_dataset(app)
        elif choice == "4":
            print(" Exiting Tool Explorer.")
            break
        else:
            print(" Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
