def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_and_list_site(client):
    resp = client.post("/api/sites", json={"name": "OmniFit", "base_url": "https://omnifittraining.com/"})
    assert resp.status_code == 200
    site = resp.json()
    assert site["name"] == "OmniFit"

    resp = client.get("/api/sites")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_scan_local_fixture_and_dashboard(client, fixture_server_url):
    site = client.post("/api/sites", json={"name": "OmniFit", "base_url": "https://omnifittraining.com/"}).json()

    resp = client.post(f"/api/sites/{site['id']}/scan", json={"use_local_fixture": True, "max_pages": 20})
    assert resp.status_code == 200
    scan = resp.json()
    assert scan["status"] == "COMPLETE"
    assert scan["pages_crawled"] > 0
    assert scan["overall_score"] is not None

    dash = client.get(f"/api/sites/{site['id']}/dashboard").json()
    assert dash["latest_scan"]["id"] == scan["id"]
    assert isinstance(dash["fix_next"], list)
    assert dash["site_health"]["pages_crawled"] == scan["pages_crawled"]
    assert dash["network_notice"] is not None  # local_fixture source should carry the caveat


def test_opportunity_patch(client, fixture_server_url):
    site = client.post("/api/sites", json={"name": "OmniFit", "base_url": "https://omnifittraining.com/"}).json()
    client.post(f"/api/sites/{site['id']}/scan", json={"use_local_fixture": True, "max_pages": 20})

    opps = client.get(f"/api/sites/{site['id']}/opportunities").json()
    assert len(opps) > 0
    opp_id = opps[0]["id"]

    resp = client.patch(f"/api/opportunities/{opp_id}", json={"status": "IN_PROGRESS", "notes": "working on it"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "IN_PROGRESS"
    assert resp.json()["notes"] == "working on it"


def test_generate_recommendation(client, fixture_server_url):
    site = client.post("/api/sites", json={"name": "OmniFit", "base_url": "https://omnifittraining.com/"}).json()
    client.post(f"/api/sites/{site['id']}/scan", json={"use_local_fixture": True, "max_pages": 20})
    opp_id = client.get(f"/api/sites/{site['id']}/opportunities").json()[0]["id"]

    resp = client.post(f"/api/opportunities/{opp_id}/generate-recommendation")
    assert resp.status_code == 200
    body = resp.json()
    assert body["generated_by"] == "heuristic"
    assert "caveat" in body["content"]


def test_tasks_crud(client):
    resp = client.post("/api/tasks", json={"title": "Follow up on citation"})
    assert resp.status_code == 200
    task = resp.json()
    assert task["status"] == "OPEN"

    resp = client.get("/api/tasks")
    assert len(resp.json()) == 1


def test_invalid_opportunity_status_rejected(client, fixture_server_url):
    site = client.post("/api/sites", json={"name": "OmniFit", "base_url": "https://omnifittraining.com/"}).json()
    client.post(f"/api/sites/{site['id']}/scan", json={"use_local_fixture": True, "max_pages": 20})
    opp_id = client.get(f"/api/sites/{site['id']}/opportunities").json()[0]["id"]
    resp = client.patch(f"/api/opportunities/{opp_id}", json={"status": "NOT_A_REAL_STATUS"})
    assert resp.status_code == 400
