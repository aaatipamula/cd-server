from dataclasses import dataclass
from typing import Optional, List, Literal

from server.models.base import Base
from server.models.githubUser import GitHubUser

class InvalidFormat(BaseException): ...

@dataclass(frozen=True)
class PullRequestLabel(Base):
    id: int
    node_id: str
    url: str
    color: str
    default: bool
    description: Optional[str] = None

@dataclass()
class PullRequestMilestone(Base):
    url: str
    html_url: str
    labels_url: str
    id: int
    node_id: str
    number: str
    state: Literal["open", "closed"]
    title: str
    description: str
    creator: GitHubUser
    open_issues: int
    closed_issues: int
    created_at: str
    updated_at: str
    closed_at: Optional[str] = None
    due_on: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.creator, dict):
            self.creator = GitHubUser(**self.creator)

@dataclass()
class PullRequest(Base):
    url: str
    id: int
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    number: int
    state: str
    locked: bool
    title: str
    user: GitHubUser
    body: str
    labels: List[PullRequestLabel]
    milestone: PullRequestMilestone
    created_at: str
    updated_at: str
    closed_at: str
    merged_at: str
    assignee: GitHubUser
    head: object
    base: object
    _links: object
    author_association: Literal[
        "COLLABORATOR",
        "CONTRIBUTOR",
        "FIRST_TIMER",
        "FIRST_TIME_CONTRIBUTOR",
        "MANEQUIN",
        "MEMBER",
        "NONE",
        "OWNER"
    ]
    auto_merge: object
    merged: bool
    mergeable_state: str
    merged_by: GitHubUser
    comments: int
    review_comments: int
    maintainer_can_modify: bool
    commits: int
    additions: int
    deletions: int
    changed_files: int
    mergeable: bool
    draft: Optional[bool] = None
    rebaseable: Optional[bool] = None
    merge_commit_sha: Optional[str] = None
    allow_auto_merge: Optional[bool] = None
    requested_teams: Optional[object] = None
    active_lock_reason: Optional[str] = None
    allow_update_branch: Optional[bool] = None
    assignees: Optional[List[GitHubUser]] = None
    delete_branch_on_merge: Optional[bool] = None
    requested_reviewers: Optional[List[GitHubUser]] = None
    merge_commit_message: Optional[Literal["PR_TITLE", "PR_BODY", "BLANK"]] = None
    merge_commit_title: Optional[Literal["PR_TITLE", "MERGE_MESSAGE"]] = None
    squash_merge_commit_message: Optional[Literal["PR_BODY", "COMMIT_MESSAGES", "BLANK"]] = None
    squash_merge_commit_title: Optional[Literal["PR_TITLE", "COMMIT_OR_PR_TITLE"]] = None
    use_squash_pr_title_as_default: Optional[bool] = None

    def __post_init__(self):
        if isinstance(self.user, dict):
            self.user = GitHubUser(**self.user)
        else: raise InvalidFormat("Invalid formatting for GitHubUser")

        if self.labels and isinstance(self.labels[0], dict):
            self.labels = list(map(lambda label: PullRequestLabel(**label), self.labels))

        if isinstance(self.milestone, dict):
            self.milestone = PullRequestMilestone(**self.milestone)

        if isinstance(self.assignee, dict):
            self.assignee = GitHubUser(**self.assignee)
        
        if self.assignees and isinstance(self.assignees[0], dict):
            self.assignees = list(map(lambda user: GitHubUser(**user), self.assignees))

        if self.requested_reviewers and isinstance(self.requested_reviewers[0], dict):
            self.requested_reviewers = list(map(lambda user: GitHubUser(**user), self.requested_reviewers))

        if isinstance(self.merged_by, dict):
            self.merged_by = GitHubUser(**self.merged_by)

