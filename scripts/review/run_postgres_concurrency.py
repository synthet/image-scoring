"""Run selected-region interleavings against a disposable, network-isolated PostgreSQL."""

import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

HUB = Path(__file__).resolve().parents[2]


def docker(*args):
    return subprocess.check_output(["docker", *args], text=True).strip()


def main():
    name = "architecture-review-" + uuid.uuid4().hex[:12]
    container = docker("run", "--detach", "--rm", "--network", "none", "--name", name,
                       "--label", "review.campaign=architecture-2026-10-23",
                       "--tmpfs", "/var/lib/postgresql/data",
                       "--env", "POSTGRES_HOST_AUTH_METHOD=trust", "--env", "POSTGRES_DB=image_scoring_test",
                       "pgvector/pgvector:pg17")
    try:
        identity = json.loads(docker("inspect", container))[0]
        assert identity["Id"] == container
        assert identity["HostConfig"]["NetworkMode"] == "none"
        assert not identity["HostConfig"].get("PortBindings")
        assert identity["Config"]["Labels"]["review.campaign"] == "architecture-2026-10-23"
        assert not any(m["Type"] in ("bind", "volume") for m in identity["Mounts"])
        for _ in range(45):
            ready = subprocess.run(["docker", "exec", container, "pg_isready", "-U", "postgres"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if ready.returncode == 0:
                break
            time.sleep(1)
        else:
            raise RuntimeError("Disposable PostgreSQL did not become ready")
        target = docker("exec", container, "psql", "-U", "postgres", "-d", "image_scoring_test", "-Atc",
                        "SELECT current_database()")
        assert target == "image_scoring_test"
        evidence = HUB / "docs/reports/architecture-review-2026-10-23/evidence"
        (evidence / "postgres-isolation.json").write_text(json.dumps({
            "container_id": container, "image_id": identity["Image"], "network": "none",
            "published_ports": [], "persistent_or_host_mounts": [], "database": target,
            "storage": "tmpfs; destroyed when test server stops",
        }, indent=2) + "\n", encoding="utf-8")
        command = ["docker", "run", "--rm", "--read-only", "--tmpfs", "/tmp",
                   "--network", "container:" + container, "--mount",
                   f"type=bind,source={HUB.parent / 'image-scoring-pipeline'},target=/review,readonly",
                   "--workdir", "/review", "--env", "PYTHONPATH=/review", "--env", "RUN_POSTGRES_TESTS=1",
                   "--env", "POSTGRES_HOST=127.0.0.1", "--env", "POSTGRES_PORT=5432",
                   "--env", "POSTGRES_DB=image_scoring_test", "--env", "POSTGRES_USER=postgres",
                   "--env", "POSTGRES_PASSWORD=review-only", "--entrypoint", "python", "image-scoring:latest",
                   "-B", "-m", "pytest", "-q", "--tb=short", "-m", "postgres", "-o", "cache_dir=/tmp/pytest-cache",
                   "tests/integration/test_bird_bbox_selection_locking.py"]
        code = subprocess.call([sys.executable, str(HUB / "scripts/review/run_check.py"), "--receipt",
                                str(evidence / "postgres-concurrency.json"), "--timeout", "180", "--", *command], cwd=HUB)
    finally:
        # Only stop the container created above, after checking its exact identity and label.
        current = json.loads(docker("inspect", container))[0]
        assert current["Id"] == container and current["Config"]["Labels"]["review.campaign"] == "architecture-2026-10-23"
        docker("stop", container)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
