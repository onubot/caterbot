import os

environment = (
    "development"
    if os.environ.get("ENV", "PRODUCTION").lower() == "dev"
    else "production"
)
api_version = "v1"

mongo_host = "18.141.11.47" if environment == "production" else "localhost"
