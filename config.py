import os

environment = "development" if os.environ.get("ENV", "PRODUCTION").lower() == "dev" else "production"
api_version = "v1"