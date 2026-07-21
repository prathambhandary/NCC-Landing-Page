import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    # Add these lines at the end of the class
    UNIT_NAME = os.getenv("UNIT_NAME", "Manipal Jnanasudha NCC Naval Sub Unit")
    PARENT_UNIT = os.getenv("PARENT_UNIT", "6 Kar Naval Unit NCC")
    DIRECTORATE = os.getenv("DIRECTORATE", "Karnataka & Goa Directorate, NCC")
    CADET_STRENGTH = int(os.getenv("CADET_STRENGTH", 100))