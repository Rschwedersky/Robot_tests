import os
from github import Github
from github.Auth import Token

# ---- CONFIG -------------------------------------------------

PROCEDURE_REQUIREMENTS = {
    "PROC-001": [
        "REQ-AUTH-001",
        "REQ-PROD-001",
        "REQ-CART-001",
        "REQ-CART-004",
        "REQ-CHK-001",
        "REQ-CHK-006",
    ],
    # PROC-002, PROC-003...
}

ISSUE_MAP = {
    "REQ-AUTH-001": 2,
    "REQ-PROD-001": 4,
    "REQ-CART-001": 9,
    "REQ-CART-004": 12,
    "REQ-CHK-001": 13,
    "REQ-CHK-006": 18,
}

LABEL_PASS = "✅ Pass"
LABEL_FAIL = "❌ Fail"

# ------------------------------------------------------------

def main():
    token = os.getenv("GH_PAT")
    procedure = os.getenv("PROCEDURE")
    result = os.getenv("RESULT")
    run_id = os.getenv("GITHUB_RUN_ID")
    repo_name = os.getenv("GITHUB_REPOSITORY")

    if not token:
        raise RuntimeError("GH_PAT not provided")

    requirements = PROCEDURE_REQUIREMENTS.get(procedure)
    if not requirements:
        print(f"[INFO] No requirements mapped for {procedure}")
        return

    g = Github(auth=Token(token))
    repo = g.get_repo(repo_name)

    run_url = f"https://github.com/{repo_name}/actions/runs/{run_id}"
    label = LABEL_PASS if result == "pass" else LABEL_FAIL

    for req in requirements:
        issue_number = ISSUE_MAP.get(req)
        if not issue_number:
            print(f"[WARN] No issue mapped for {req}")
            continue

        issue = repo.get_issue(number=issue_number)

        # Atualiza label
        issue.set_labels(label)

        # Comenta com evidência
        issue.create_comment(
            f"""🧪 **Manual Test Execution**

**Procedure:** `{procedure}`  
**Result:** {label}

📎 **Evidence (workflow artifacts):**  
{run_url}
"""
        )

        print(f"[INFO] Issue #{issue_number} updated")

if __name__ == "__main__":
    main()
