"""End-to-end: create site -> scan -> findings -> opportunities -> dashboard Fix Next."""


def test_full_flow(client, fixture_server_url):
    site = client.post("/api/sites", json={"name": "OmniFit Performance", "base_url": "https://omnifittraining.com/"}).json()

    scan_resp = client.post(f"/api/sites/{site['id']}/scan", json={"use_local_fixture": True})
    assert scan_resp.status_code == 200
    scan = scan_resp.json()
    assert scan["status"] == "COMPLETE"
    assert scan["pages_crawled"] > 5

    findings = client.get(f"/api/sites/{site['id']}/findings").json()
    assert len(findings) > 0

    opportunities = client.get(f"/api/sites/{site['id']}/opportunities").json()
    assert len(opportunities) > 0
    assert all("priority_score" in o for o in opportunities)

    dashboard = client.get(f"/api/sites/{site['id']}/dashboard").json()
    assert 1 <= len(dashboard["fix_next"]) <= 3
    # Fix Next must be the highest-priority OPEN opportunities, in order.
    scores = [o["priority_score"] for o in dashboard["fix_next"]]
    assert scores == sorted(scores, reverse=True)
    assert dashboard["biggest_strength"] is not None
    assert dashboard["biggest_weakness"] is not None

    # Simulate fixing the top opportunity, then rescanning should not resurrect it
    # unless the underlying issue still exists.
    top_id = dashboard["fix_next"][0]["id"]
    client.patch(f"/api/opportunities/{top_id}", json={"status": "IN_PROGRESS"})
    updated = client.get(f"/api/sites/{site['id']}/opportunities/top").json()
    assert all(o["id"] != top_id for o in updated)  # no longer OPEN, so it drops out of Fix Next
