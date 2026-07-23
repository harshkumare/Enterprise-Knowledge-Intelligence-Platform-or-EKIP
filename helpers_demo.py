from app.utils.helpers import (
    ensure_directory,
    save_json,
    load_json,
    current_timestamp,
)

ensure_directory("temp")

data = {
    "project": "EKIP",
    "author": "Harsh"
}

save_json(data, "temp/sample.json")

loaded = load_json("temp/sample.json")

print(loaded)
print(current_timestamp())