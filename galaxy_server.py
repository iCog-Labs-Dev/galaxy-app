from galaxy.app import UniverseApplication

# You need a Galaxy config file or minimal dict config
app = UniverseApplication(global_conf={
    '__file__': 'galaxy.yml'
})

print("✅ Galaxy backend initialized.")
