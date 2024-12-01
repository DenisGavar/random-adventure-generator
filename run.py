import os
from app import create_app
from dotenv import load_dotenv

load_dotenv(override=True)

app = create_app(os.getenv("CONFIG_MODE"))

if __name__ == '__main__':
    app.run()
