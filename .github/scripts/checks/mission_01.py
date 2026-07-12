"""Mission 01 -- First real commit: a feature branch with a real commit message."""

from lib import git_inspect

PLACEHOLDER_MESSAGES = {"wip", "update", "fix", "changes", "commit", "test", "asdf"}


def check(context: dict) -> tuple[bool, str]:
    branches = git_inspect.remote_branches()
    if not branches:
        return False, (
            "No feature branch found yet. Create one (e.g. "
            "`git switch -c feature/add-category-field`), make a real change to "
            "relnotes, commit it, and push it."
        )

    branch = branches[0]
    ahead = git_inspect.commit_count(f"origin/{branch}", since_ref="origin/main")
    if ahead == 0:
        return False, f"Branch '{branch}' exists but has no commits ahead of main yet."

    messages = git_inspect.commit_messages(f"origin/{branch}", n=ahead)
    if all(m.strip().lower() in PLACEHOLDER_MESSAGES for m in messages):
        return False, (
            f"Found commit(s) on '{branch}', but the message(s) ({', '.join(messages)}) "
            "don't say anything about *why*. Rewrite it with a message that explains the change."
        )

    context["state"]["feature_branch"] = branch
    return True, f"Found a real commit on '{branch}': \"{messages[0]}\". On to Mission 02."
