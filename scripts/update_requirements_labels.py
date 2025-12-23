import os
import sys
from robot.api import ExecutionResult
from github import Github, Auth


# =========================
# CONFIG
# =========================

RESULTS_PATH = "results/output.xml"

ISSUE_MAP = {
    "REQ-AUTH-001": 2,
    "REQ-AUTH-002": 3,
    "REQ-PROD-001": 4,
    "REQ-PROD-002": 5,
    "REQ-PROD-003": 6,
    "REQ-PROD-004": 7,
    "REQ-PROD-005": 8,
    "REQ-CART-001": 9,
    "REQ-CART-002": 10,
    "REQ-CART-003": 11,
    "REQ-CART-004": 12,
    "REQ-CHK-001": 13,
    "REQ-CHK-002": 14,
    "REQ-CHK-003": 15,
    "REQ-CHK-004": 16,
    "REQ-CHK-005": 17,
}

LABEL_PASS = "✅ Pass"
LABEL_FAIL = "❌ Fail"


# =========================
# PARSE ROBOT RESULTS
# =========================

def parse_robot_results(path):
    if not os.path.exists(path):
        print(f"[ERROR] output.xml not found: {path}")
        sys.exit(1)

    result = ExecutionResult(path)
    result.configure(statistics=False, timeline=False)

    results = {}  # issue_number -> [PASS, FAIL]

    for test in result.suite.tests:
        status = test.status  # PASS / FAIL
        tags = test.tags

        for tag in tags:
            if tag in ISSUE_MAP:
                issue_number = ISSUE_MAP[tag]
                results.setdefault(issue_number, []).append(status)

    return results


# =========================
# DECISION LOGIC
# =========================

def decide_label(statuses):
    if not statuses:
        return None
    if "FAIL" in statuses:
        return LABEL_FAIL
    return LABEL_PASS


# =========================
# MAIN
# =========================

def main():
    token = os.getenv("GH_PAT")
    if not token:
        print("[ERROR] GH_PAT not defined")
        sys.exit(1)

    repo_name = os.getenv("GITHUB_REPOSITORY")
    if not repo_name:
        print("[ERROR] GITHUB_REPOSITORY not available")
        sys.exit(1)

    results = parse_robot_results(RESULTS_PATH)

    if not results:
        print("[INFO] No tests found to update.")
        return

    gh = Github(auth=Auth.Token(token))
    repo = gh.get_repo(repo_name)

    for issue_number, statuses in results.items():
        label = decide_label(statuses)
        if not label:
            continue

        try:
            issue = repo.get_issue(number=issue_number)

            existing = [l.name for l in issue.labels]
            new_labels = [
                l for l in existing
                if l not in (LABEL_PASS, LABEL_FAIL)
            ]
            new_labels.append(label)

            issue.set_labels(*new_labels)
            print(f"[INFO] Issue #{issue_number} -> {label}")

        except Exception as e:
            print(f"[ERROR] Issue #{issue_number}: {e}")


if __name__ == "__main__":
    main()
