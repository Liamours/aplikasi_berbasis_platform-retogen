import os
import subprocess

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Retogen")

SEED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "db", "seed")

collections = [
    ("user",          "Retogen.user.json"),
    ("article",       "Retogen.article.json"),
    ("comment",       "Retogen.comment.json"),
    ("rating",        "Retogen.rating.json"),
    ("report_article","Retogen.article_report.json"),
    ("report_user",   "Retogen.user_report.json"),
]

for collection, filename in collections:
    filepath = os.path.join(SEED_DIR, filename)

    # Try local mongoimport first, fall back to running inside Docker container
    result = subprocess.run([
        "mongoimport",
        "--host", f"{MONGO_HOST}:{MONGO_PORT}",
        "--db", MONGO_DB_NAME,
        "--collection", collection,
        "--file", filepath,
        "--jsonArray",
        "--drop"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        # mongoimport not available locally — run through Docker
        abs_filepath = os.path.abspath(filepath)
        container_path = abs_filepath.replace("\\", "/")
        result = subprocess.run([
            "docker", "exec", "retogen-db",
            "mongoimport",
            "--host", "localhost",
            "--db", MONGO_DB_NAME,
            "--collection", collection,
            "--file", f"/seed/{filename}",
            "--jsonArray",
            "--drop"
        ], capture_output=True, text=True)

    print(f"{collection}: {result.stdout.strip() or result.stderr.strip()}")
