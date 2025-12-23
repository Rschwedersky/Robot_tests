import os
import sys
import xml.etree.ElementTree as ET
from github import Github
from github import Auth


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
# PARSE ROBOT OUTPUT
# =========================

def parse_robot_results(path: str):
    if not os.path.exists(path):
        print(f"[ERROR] Robot output not found: {path}")
        sys.exit(1)

    tree = ET.parse(path)
    root = tree.getroot()

    results = {}  # issue_number -> [PASS, FAIL]

    for test in root.iter("test"):
        status_node = test.find("status")
        if status_node is None:
            continue

        status = status_node.attrib.get("status")  # PASS / FAIL

        tags_node = test.find("tags")
        if tags_node is None:
            continue

        tags = [t.text for t in tags_node.iter("tag")]

        for tag in tags:
            if tag in ISSUE_MAP:
                issue_number = ISSUE_MAP[tag]
                results.setdefault(issue_number, []).append(status)

    return results


# =========================
# DECISION LOGIC
# =========================

def decide_label(statuses):
    """
    Requisito:
    - FAIL se pelo menos 1 teste falhar
    - PASS se todos passarem
    - None se nenhum teste encontrado
    """
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

    results = parse_robot_results(RESULTS_PATH)

    if not results:
        print("[INFO] No tests found to update.")
        return

    auth = Auth.Token(token)
    gh = Github(auth=auth)

    repo_name = os.getenv("GITHUB_REPOSITORY")
    if not repo_name:
        print("[ERROR] GITHUB_REPOSITORY not available")
        sys.exit(1)

    repo = gh.get_repo(repo_name)

    for issue_number, statuses in results.items():
        label = decide_label(statuses)
        if not label:
            continue

        try:
            issue = repo.get_issue(number=issue_number)

            # Remove labels antigos de status
            existing_labels = [l.name for l in issue.labels]
            new_labels = [
                l for l in existing_labels
                if l not in (LABEL_PASS, LABEL_FAIL)
            ]
            new_labels.append(label)

            issue.set_labels(*new_labels)

            print(f"[INFO] Issue #{issue_number} -> {label}")

        except Exception as e:
            print(f"[ERROR] Could not update issue #{issue_number}: {e}")


if __name__ == "__main__":
    main()
