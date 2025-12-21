import os
import xml.etree.ElementTree as ET
from github import Github

# -----------------------------
# Configurações
# -----------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # GitHub Actions secret
REPO_NAME = "Rschwedersky/Robot_tests"
ROBOT_RESULTS_XML = "results/output.xml"

# Labels
PASS_LABEL = "✅ pass"
FAIL_LABEL = "❌ fail"

# Mapeamento de tags de teste para números de issues
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

# -----------------------------
# Funções
# -----------------------------
def parse_robot_results(xml_path):
    """Parseia o output.xml do Robot Framework e retorna um dicionário
    {issue_number: [status1, status2, ...]}
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = {}

    for suite in root.iter("suite"):
        for test in suite.iter("test"):
            # status do teste
            status_elem = test.find("status")
            status = status_elem.attrib.get("status") if status_elem is not None else "FAIL"

            # tags do teste
            tags_elem = test.find("tags")
            tags = [t.text for t in tags_elem.iter("tag")] if tags_elem is not None else []

            # mapear tags para issues
            for tag in tags:
                issue_number = issue_map.get(tag)
                if issue_number:
                    results.setdefault(issue_number, []).append(status)

    return results

def update_github_labels(results):
    """Atualiza labels no GitHub Issues com base nos resultados do Robot Framework"""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    for issue_number, statuses in results.items():
        issue = repo.get_issue(number=issue_number)
        # decidir label final: se todos os testes passarem, pass; se algum falhar, fail
        if all(s == "PASS" for s in statuses):
            label_to_add = PASS_LABEL
            label_to_remove = FAIL_LABEL
        else:
            label_to_add = FAIL_LABEL
            label_to_remove = PASS_LABEL

        # remover label oposta se existir
        if label_to_remove in [l.name for l in issue.labels]:
            issue.remove_from_labels(label_to_remove)

        # adicionar label correto
        if label_to_add not in [l.name for l in issue.labels]:
            issue.add_to_labels(label_to_add)
        print(f"Issue #{issue_number} updated: {label_to_add}")


def main():
    results = parse_robot_results(ROBOT_RESULTS_XML)
    update_github_labels(results)

if __name__ == "__main__":
    main()

