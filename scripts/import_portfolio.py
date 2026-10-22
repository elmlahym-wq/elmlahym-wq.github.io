import hashlib, json, pathlib, urllib.request, time
base = "https://mohamed-creative-portfolio.peachypearl17.chatgpt.site/"
manifest = json.loads(pathlib.Path("migration-manifest.json").read_text())
for name, expected in manifest.items():
    path = pathlib.Path(name)
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == expected:
        continue
    for attempt in range(4):
        try:
            req = urllib.request.Request(base + name, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError("Hash mismatch: " + name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            print("Imported", name, len(data), flush=True)
            break
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3)
pathlib.Path(".nojekyll").touch()
