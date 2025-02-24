from dataclasses import dataclass
from typing import Optional
import re

from server.models.githubUser import GitHubUser

@dataclass(frozen=True)
class Repository:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: GitHubUser
    html_url: str
    description: Optional[str]
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: Optional[str]
    size: int
    stargazers_count: int
    watchers_count: int
    language: str
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: Optional[str]
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[object]
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: object
    visibility: int
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    stargazers: object
    master_branch: str

    def __post_init__(self) -> None:
        if re.match(r"^[\w\-]+$", self.name) is None:
            raise Exception("Invalid repository name") # Raise specific exception

        if re.match(r"^[\w\-]+/[\w\-]+$", self.full_name) is None:
            raise Exception("Invalid full name") # Raise specific exception

        if re.match(r"^https://github\.com/[\w\-]+/[\w\-]+\.git$", self.clone_url) is None:
            raise Exception("Invalid clone URL") # Raise specific exception
