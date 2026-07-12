"""
gh_api.py -- thin GitHub API wrapper for mission checkers.

Uses the ambient GITHUB_TOKEN and GITHUB_REPOSITORY env vars every
Actions job gets for free -- no PAT, no maintainer-provisioned secret.
All checks inspect real API state; nothing here is mocked.
"""

from __future__ import annotations

import os

from github import Auth, Github
from github.PullRequest import PullRequest
from github.Repository import Repository
from github.WorkflowRun import WorkflowRun


def get_client() -> Github:
    token = os.environ["GITHUB_TOKEN"]
    return Github(auth=Auth.Token(token))


def get_repo(client: Github | None = None) -> Repository:
    client = client or get_client()
    repo_name = os.environ["GITHUB_REPOSITORY"]
    return client.get_repo(repo_name)


def all_pulls(repo: Repository) -> list[PullRequest]:
    return list(repo.get_pulls(state="all", sort="created", direction="desc"))


def latest_pull(repo: Repository) -> PullRequest | None:
    pulls = all_pulls(repo)
    return pulls[0] if pulls else None


def pull_for_branch(repo: Repository, branch: str) -> PullRequest | None:
    for pr in all_pulls(repo):
        if pr.head.ref == branch:
            return pr
    return None


def workflow_runs_for_sha(
    repo: Repository, sha: str, workflow_name: str | None = None
) -> list[WorkflowRun]:
    runs = [run for run in repo.get_workflow_runs() if run.head_sha == sha]
    if workflow_name is not None:
        runs = [run for run in runs if run.name == workflow_name]
    return runs


def environment_exists(repo: Repository, name: str) -> bool:
    try:
        repo.get_environment(name)
        return True
    except Exception:
        return False


def environment_has_required_reviewer(repo: Repository, name: str) -> bool:
    env = repo.get_environment(name)
    protection_rules = getattr(env, "protection_rules", None) or []
    return any(getattr(rule, "type", None) == "required_reviewers" for rule in protection_rules)


def environment_has_secret(repo: Repository, env_name: str, secret_name: str) -> bool:
    # PyGithub doesn't expose environment secrets directly; hit the REST
    # endpoint via the low-level requester instead.
    status, _, data = repo._requester.requestJson(
        "GET", f"{repo.url}/environments/{env_name}/secrets"
    )
    if status != 200:
        return False
    import json

    secrets = json.loads(data).get("secrets", [])
    return any(s["name"] == secret_name for s in secrets)


def latest_artifacts(repo: Repository) -> list[str]:
    return [a.name for a in repo.get_artifacts()]


def latest_pages_deployment_status(repo: Repository) -> str | None:
    deployments = repo.get_deployments(environment="production")
    deployments = list(deployments)
    if not deployments:
        return None
    latest = deployments[0]
    statuses = list(latest.get_statuses())
    return statuses[0].state if statuses else None


def read_repo_file(repo: Repository, path: str, ref: str = "main") -> str | None:
    """
    Read a file's content from a specific branch via the API -- not the
    local checkout, which may be on a different branch (a feature branch
    or PR that forked before this file last changed on `ref`).
    """
    try:
        content_file = repo.get_contents(path, ref=ref)
    except Exception:
        return None
    return content_file.decoded_content.decode("utf-8")


def write_repo_file(
    repo: Repository, path: str, content: str, message: str, ref: str = "main"
) -> None:
    """
    Create or update a file directly on `ref` via the API -- this is how
    progress state gets persisted, deliberately independent of whichever
    branch triggered the check that produced it.
    """
    try:
        existing = repo.get_contents(path, ref=ref)
        repo.update_file(path, message, content, existing.sha, branch=ref)
    except Exception:
        repo.create_file(path, message, content, branch=ref)
