#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from github import Github, Auth

# --------------------
# Configurações
# --------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = "Rschwedersky/Robot_tests"

# Mapeamento de tags do Robot Framework para número da issue
issue_map = {
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
    "REQ-CHK-005": 17
}

# Labels
PASS_LABEL = "✅ Pass"
FAIL_LABEL = "❌ Fail"

# --------------------
# Funções
# --------------------
def parse_robot_results(path):
    import xml.etree.ElementTree as ET
    tree = ET.parse(path)
    root = tree.getroot()
    results = {}
    for test in root.findall(".//test"):
        tags = [t.text for t in test.findall("tag")]  # <- aqui pegamos direto
        status = test.get("result")
        for tag in tags:
            issue_number = issue_map.get(tag)
            if issue_number:
                results.setdefault(issue_number, []).append(status)
    return results



def determine_issue_label(status_list):
    """Se todos PASS -> Pass, senão Fail"""
    return PASS_LABEL if all(s == "PASS" for s in status_list) else FAIL_LABEL


def main():
    g = Github(auth=Auth.Token(GITHUB_TOKEN))
    repo = g.get_repo(REPO_NAME)

    results = parse_robot_results()
    if not results:
        print("[INFO] No tests found to update.")
        return

    for issue_number, statuses in results.items():
        try:
            issue = repo.get_issue(number=issue_number)
            label_to_add = determine_issue_label(statuses)

            # Remove label oposta, se existir
            remove_label = FAIL_LABEL if label_to_add == PASS_LABEL else PASS_LABEL
            if remove_label in [l.name for l in issue.labels]:
                issue.remove_from_labels(remove_label)

            # Adiciona label atual
            if label_to_add not in [l.name for l in issue.labels]:
                issue.add_to_labels(label_to_add)

            print(f"[INFO] Issue #{issue_number} updated with label '{label_to_add}'")
        except Exception as e:
            print(f"[ERROR] Could not update issue #{issue_number}: {e}")


if __name__ == "__main__":
    main()
