import os
import subprocess

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Retogen")

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "db")

collections = [
    ("user",          "Retogen.user.json"),
    ("article",       "Retogen.article.json"),
    ("comment",       "Retogen.comment.json"),
    ("rating",        "Retogen.rating.json"),
    ("report_article","Retogen.article_report.json"),
    ("report_user",   "Retogen.user_report.json"),
]

for collection, filename in collections:
    filepath = os.path.join(DB_DIR, filename)
    result = subprocess.run([
        "mongoimport",
        "--host", MONGO_HOST,
        "--port", MONGO_PORT,
        "--db", MONGO_DB_NAME,
        "--collection", collection,
        "--file", filepath,
        "--jsonArray",
        "--drop"
    ], capture_output=True, text=True)
    print(f"{collection}: {result.stdout.strip() or result.stderr.strip()}")