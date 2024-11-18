from models.engine.file_storage import FileStorage

# Create a single instance of FileStorage
storage = FileStorage()

# Load any objects from the JSON file into memory
storage.reload()
