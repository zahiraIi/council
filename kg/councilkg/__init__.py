import os

KG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.environ.get("COUNCIL_ROOT", os.path.dirname(KG_DIR))
DB_PATH = os.environ.get("KG_DB", os.path.join(KG_DIR, "data", "council_kg.db"))
