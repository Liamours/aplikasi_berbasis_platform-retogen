#!/bin/bash
DB="Retogen"

for file in /docker-entrypoint-initdb.d/seed/*.json; do
  [ -f "$file" ] || continue
  filename=$(basename "$file")
  collection=$(echo "$filename" | sed 's/^Retogen\.//; s/\.json$//')
  echo "Importing $collection..."
  mongoimport --host localhost --db "$DB" --collection "$collection" --file "$file" --jsonArray --drop
done

echo "Seed complete."
