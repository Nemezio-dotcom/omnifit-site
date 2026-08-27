import pytest

from app.models.core import Site
from app.scan_service import run_scan


def test_run_scan_raises_clear_error_when_root_unreachable(db_session):
    site = Site(name="Unreachable", base_url="https://this-domain-should-not-resolve.invalid/")
    db_session.add(site)
    db_session.commit()

    with pytest.raises(RuntimeError, match="Could not reach any page"):
        run_scan(db_session, site, max_pages=5)

    db_session.refresh(site)
    scan = site.scans[0]
    assert scan.status == "FAILED"
    assert scan.error
