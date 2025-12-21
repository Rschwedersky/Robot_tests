import os
import xml.etree.ElementTree as ET
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def add_label(issue_number, label):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}/labels"
    requests.post(url, headers=HEADERS, json={"labels": [label]})

def parse_robot_results(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    results = {}

    for test in root.iter("test"):
        status = test.find("status").attrib["status"]
        tags = [t.text for t in test.find("tags").iter("tag")]

        for tag in tags:
            if tag.startswith("REQ-"):
                # mapeia REQ-XXX para número do Issue (você define o mapping)
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
                issue_number = issue_map.get(tag)
                if issue_number:
                    results.setdefault(issue_number, []).append(status)
    return results

def main():
    results = parse_robot_results("results/output.xml")

    for issue, statuses in results.items():
        if all(s == "PASS" for s in statuses):
            add_label(issue, "✅ pass")
        else:
            add_label(issue, "❌ fail")

if __name__ == "__main__":
    main()
