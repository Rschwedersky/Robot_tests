import os
import re
from github import Github
from github.Auth import Token

REQ_PATTERN = re.compile(r"(REQ-[A-Z]+-\d+)")

LABEL_PASS = "✅ Pass"
LABEL_FAIL = "❌ Fail"


def extract_requirements_from_procedure(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return sorted(set(REQ_PATTERN.findall(content)))


def build_issue_map(repo):
    issue_map = {}

    for issue in repo.get_issues(state="all"):
        match = REQ_PATTERN.search(issue.title)
        if match:
            issue_map[match.group(1)] = issue

    return issue_map


def main():
    token = os.getenv("GH_PAT")
    procedure = os.getenv("PROCEDURE")          # ex: PROC-001
    result = os.getenv("RESULT")                # pass / fail
    run_id = os.getenv("GITHUB_RUN_ID")
    repo_name = os.getenv("GITHUB_REPOSITORY")

    if not token:
        raise RuntimeError("GH_PAT not provided")

    procedure_path = f"procedures/{procedure}.md"
    if not os.path.exists(procedure_path):
        raise RuntimeError(f"Procedure file not found: {procedure_path}")

    requirements = extract_requirements_from_procedure(procedure_path)

    if not requirements:
        print("[INFO] No requirements found in procedure")
        return

    g = Github(auth=Token(token))
    repo = g.get_repo(repo_name)

    issue_map = build_issue_map(repo)

    run_url = f"https://github.com/{repo_name}/actions/runs/{run_id}"
    label = LABEL_PASS if result.lower() == "pass" else LABEL_FAIL

    for req in requirements:
        issue = issue_map.get(req)

        if not issue:
            print(f"[WARN] Requirement issue not found: {req}")
            continue

        issue.set_labels(label)

        issue.create_comment(
            f"""🧪 **Manual Test Execution**

**Procedure:** `{procedure}`  
**Requirement:** `{req}`  
**Result:** {label}

📎 **Evidence (workflow artifacts):**  
{run_url}
"""
        )

        print(f"[INFO] Issue #{issue.number} ({req}) updated")


if __name__ == "__main__":
    main()
