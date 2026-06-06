import requests

BASE_URL = "http://127.0.0.1:8000"

# ── Day 01 Tests ───────────────────────────────────────────────────────────

print("=" * 50)
print("DAY 01 — Core CRUD")
print("=" * 50)

print("\n── Creating notes ──")

r = requests.post(f"{BASE_URL}/notes", json={
    "title": "FastAPI is great",
    "content": "I am learning FastAPI and it is going well",
    "tag": "learning",
    "pinned": True
})
print(r.status_code, r.json())   # 201

r = requests.post(f"{BASE_URL}/notes", json={
    "title": "Buy groceries",
    "content": "Tomatoes, onions, coconut, rice",
    "tag": "personal"
})
print(r.status_code, r.json())   # 201

r = requests.post(f"{BASE_URL}/notes", json={
    "title": "Project ideas",
    "content": "Build a notes API, then an ecommerce API",
    "tag": "ideas",
    "pinned": True
})
print(r.status_code, r.json())   # 201

r = requests.post(f"{BASE_URL}/notes", json={
    "title": "Work meeting notes",
    "content": "Discussed Q3 targets and roadmap",
    "tag": "work"
})
print(r.status_code, r.json())   # 201

r = requests.post(f"{BASE_URL}/notes", json={
    "title": "Archived old note",
    "content": "This note is old and should be archived",
    "tag": "general",
    "archived": True
})
print(r.status_code, r.json())   # 201


print("\n── Get note by ID ──")
r = requests.get(f"{BASE_URL}/notes/1")
print(r.status_code, r.json())   # 200

print("\n── Get note that doesn't exist ──")
r = requests.get(f"{BASE_URL}/notes/999")
print(r.status_code, r.json())   # 404

print("\n── Update note id=2 ──")
r = requests.put(f"{BASE_URL}/notes/2", json={
    "title": "Buy groceries — updated",
    "content": "Tomatoes, onions, coconut, rice, bread, milk",
    "tag": "personal",
    "pinned": False,
    "archived": False
})
print(r.status_code, r.json())   # 200

print("\n── Update note that doesn't exist ──")
r = requests.put(f"{BASE_URL}/notes/999", json={
    "title": "Ghost note",
    "content": "This does not exist",
    "tag": "general",
    "pinned": False,
    "archived": False
})
print(r.status_code, r.json())   # 404

print("\n── Delete note id=4 ──")
r = requests.delete(f"{BASE_URL}/notes/4")
print(r.status_code)   # 204

print("\n── Delete note that doesn't exist ──")
r = requests.delete(f"{BASE_URL}/notes/999")
print(r.status_code, r.json())   # 404


# ── Day 02 Tests ───────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("DAY 02 — List Endpoint With Filtering and Search")
print("=" * 50)

print("\n── All notes (archived hidden by default) ──")
r = requests.get(f"{BASE_URL}/notes")
print(r.status_code, r.json())

print("\n── All notes including archived ──")
r = requests.get(f"{BASE_URL}/notes", params={"archived": "true"})
print(r.status_code, r.json())

print("\n── Filter by tag=learning ──")
r = requests.get(f"{BASE_URL}/notes", params={"tag": "learning"})
print(r.status_code, r.json())

print("\n── Filter by pinned=true ──")
r = requests.get(f"{BASE_URL}/notes", params={"pinned": "true"})
print(r.status_code, r.json())

print("\n── Filter by pinned=false ──")
r = requests.get(f"{BASE_URL}/notes", params={"pinned": "false"})
print(r.status_code, r.json())

print("\n── Search by keyword 'FastAPI' ──")
r = requests.get(f"{BASE_URL}/notes", params={"search": "FastAPI"})
print(r.status_code, r.json())

print("\n── Search by keyword that doesn't match anything ──")
r = requests.get(f"{BASE_URL}/notes", params={"search": "blockchain"})
print(r.status_code, r.json())   # empty list

print("\n── Pagination — skip=1 limit=2 ──")
r = requests.get(f"{BASE_URL}/notes", params={"skip": 1, "limit": 2})
print(r.status_code, r.json())


# ── Day 03 Tests ───────────────────────────────────────────────────────────

# print("\n" + "=" * 50)
# print("DAY 03 — Action Endpoints and Business Rules")
# print("=" * 50)

# print("\n── Pin note id=2 ──")
# r = requests.put(f"{BASE_URL}/notes/2/pin")
# print(r.status_code, r.json())   # pinned should be True

# print("\n── Unpin note id=1 ──")
# r = requests.put(f"{BASE_URL}/notes/1/unpin")
# print(r.status_code, r.json())   # pinned should be False

# print("\n── Archive note id=2 ──")
# r = requests.put(f"{BASE_URL}/notes/2/archive")
# print(r.status_code, r.json())   # archived should be True

# print("\n── Confirm archived note hidden in default list ──")
# r = requests.get(f"{BASE_URL}/notes")
# print(r.status_code, r.json())   # id=2 should not appear

# print("\n── Empty title validation ──")
# r = requests.post(f"{BASE_URL}/notes", json={
#     "title": "",
#     "content": "This should fail"
# })
# print(r.status_code, r.json())   # 400

# print("\n── Empty content validation ──")
# r = requests.post(f"{BASE_URL}/notes", json={
#     "title": "Valid title",
#     "content": ""
# })
# print(r.status_code, r.json())   # 400

# print("\n── Confirm pinned notes appear first ──")
# r = requests.get(f"{BASE_URL}/notes")
# print(r.status_code, r.json())   # pinned notes at the top

# print("\n── Pin note that doesn't exist ──")
# r = requests.put(f"{BASE_URL}/notes/999/pin")
# print(r.status_code, r.json())   # 404