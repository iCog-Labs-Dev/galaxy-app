<div align="center">
  <img src="https://media.hswstatic.com/eyJidWNrZXQiOiJjb250ZW50Lmhzd3N0YXRpYy5jb20iLCJrZXkiOiJnaWZcL2dldHR5aW1hZ2VzLTU0MTM4NTg1Ni5qcGciLCJlZGl0cyI6eyJyZXNpemUiOnsid2lkdGgiOjgyOH19fQ==" width="400"/>
</div>

# 🌌 Galaxy App

**Galaxy App** is a Python library that simplifies interaction with a Galaxy server — a powerful platform for accessible, reproducible, and transparent computational biomedical research.

This library helps developers easily create applications or workflows that communicate with Galaxy instances through a Pythonic interface.

---

##  Installation

You can install the `galaxy-app` package using pip:

```bash
pip install galaxy-app
```

>  **Note**: It is strongly recommended to install this package inside a virtual environment to avoid conflicts.

### Create and activate a virtual environment (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Linux/macOS)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

Then install:

```bash
pip install galaxy-app
```

---

##  Quick Start

Here’s a simple example to connect to a Galaxy instance and list available tools:

```python
from galaxy.app import GalaxyApp

# Connect to your Galaxy instance
app = GalaxyApp("https://usegalaxy.org", api_key="YOUR_API_KEY")

# List all tools
tools = app.tools.list()
for tool in tools:
    print(tool["name"])
```

> 💡 Replace `"YOUR_API_KEY"` with your actual Galaxy API key. You can get this from your Galaxy user account (usually under "User > Preferences > API key").

---
## Or install from GitHub:
 
```bash
git clone https://github.com/iCog-Labs-Dev/galaxy-app.git
cd galaxy-app
pip install .
```
Then 
``` bash
python -m galaxy_app
```

## Features

* Connect to any Galaxy instance using API key
* List available tools and workflows
* Submit jobs to Galaxy tools
* Retrieve job status and results
* Manage datasets, histories, and workflows

---

## Documentation

Currently, the package has limited documentation. You can start by exploring:

* [Galaxy API docs](https://docs.galaxyproject.org/en/latest/api_doc.html)
* [Source code](https://github.com/mbevand/galaxy-app) (GitHub page if available)
* [PyPI page](https://pypi.org/project/galaxy-app/)

---

## Troubleshooting

* **Authentication error**: Make sure your API key is valid.
* **Connection error**: Ensure your Galaxy server URL is correct and accessible.
* **Missing dependencies**: Ensure you are using a compatible Python version (usually Python 3.6+).

---

## 🤝 Contributing

As of now, contributions may not be open, but if any issue open, feel free to fork the project and explore the code.

---



##  Need Help?

If you're new to Galaxy or bioinformatics pipelines in general, consider reading:

* [Galaxy Training Network](https://training.galaxyproject.org/)
* [Galaxy Community Hub](https://galaxyproject.org/)
