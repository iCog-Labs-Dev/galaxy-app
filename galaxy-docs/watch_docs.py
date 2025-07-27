# File: galaxy-docs/watch_docs.py
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from update_mkdocs_nav import update_mkdocs_yml  # Add this import
from generate_docs import generate_docs


class PythonFileChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_dir: Path):
        self.watch_dir = watch_dir


    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".py"):
            print(f"\n Detected change: {event.event_type} - {event.src_path}")
            print(" Regenerating documentation...")
            try:
                generate_docs()
                update_mkdocs_yml()  # <== ADDED
            except Exception as e:
                print(" Error during documentation generation:", e)



def start_watch():
    source_dir = Path(__file__).parent.parent / "galaxy_app"
    print(f" Watching for changes in: {source_dir.resolve()}")

    event_handler = PythonFileChangeHandler(source_dir)
    observer = Observer()
    observer.schedule(event_handler, str(source_dir), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(" Stopped watching.")

    observer.join()


if __name__ == "__main__":
    start_watch()
