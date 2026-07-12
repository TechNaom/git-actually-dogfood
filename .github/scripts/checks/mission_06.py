"""Mission 06 -- Real code review: leave feedback, then address it with a new commit."""



def check(context: dict) -> tuple[bool, str]:
    repo = context["repo"]
    pr_number = context["state"].get("pr_number")
    if not pr_number:
        return False, "Complete Missions 04-05 first."

    pr = repo.get_pull(pr_number)
    comments = list(pr.get_issue_comments()) + list(pr.get_review_comments())
    reviews = [r for r in pr.get_reviews() if r.submitted_at]

    if not comments and not reviews:
        return False, (
            "No review comment found yet on this PR. Leave one (yourself, or from a "
            "second account) that names a real issue, explains why it matters, and "
            "suggests a fix -- then address it with a new commit."
        )

    feedback_times = [c.created_at for c in comments] + [r.submitted_at for r in reviews]
    earliest_feedback = min(feedback_times)

    commits = list(pr.get_commits())
    later_commits = [c for c in commits if c.commit.author.date > earliest_feedback]
    if not later_commits:
        return False, (
            "Found feedback on this PR, but no new commit after it. Address the "
            "feedback with a fresh commit (not an amend/force-push) and push again."
        )

    return True, (
        f"Feedback left and addressed with a new commit on PR #{pr_number}. "
        "On to Mission 07 -- merge & clean up."
    )
