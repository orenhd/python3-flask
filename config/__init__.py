import os
from dotenv import load_dotenv

load_dotenv()

app = {
    "development_mode": os.getenv("FLASK_ENV") == "development",
    "at_string": os.getenv("AT_STRING"),
    "jwt_life_span": 180
}

databases = {
    "mongodb": {
        "uri": os.getenv("MONGODB_URI"),
        "usersCollection": "meadows"
    }
}

admin_user = {
    "password": os.getenv("ADMIN_USER_PASSWORD")
}
