import os
import subprocess

CONTAINER = os.getenv("MONGO_CONTAINER", "retogen-db")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Retogen")

SEED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed"))

collections = [
    ("user",          "Retogen.user.json"),
    ("article",       "Retogen.article.json"),
    ("comment",       "Retogen.comment.json"),
    ("rating",        "Retogen.rating.json"),
    ("report_article","Retogen.article_report.json"),
    ("report_user",   "Retogen.user_report.json"),
]

for collection, filename in collections:
    result = subprocess.run([
        "docker", "exec", CONTAINER,
        "mongoimport",
        "--host", "localhost",
        "--db", MONGO_DB_NAME,
        "--collection", collection,
        "--file", f"/seed/{filename}",
        "--jsonArray",
        "--drop"
    ], capture_output=True, text=True)

    print(f"{collection}: {result.stdout.strip() or result.stderr.strip()}")
