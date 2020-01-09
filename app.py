from src import create_app
import config

app = create_app()

if config.environment == "production":
    if __name__ == "__main__":
        app.run(debug=True)
