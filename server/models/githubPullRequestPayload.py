from dataclasses import dataclass
from typing import Optional

from server.models.githubPullRequest import PullRequest
from server.models.githubRepo import Repository
from server.models.githubUser import GitHubUser

@dataclass()
class PullRequestPayload:
    action: str
    number: int
    sender: GitHubUser
    repository: Repository
    pull_request: PullRequest
    enterprise: Optional[object] = None
    organization: Optional[object] = None
    installation: Optional[object] = None

    def __post_init__(self):
        if isinstance(self.pull_request, dict):
            self.pull_request = PullRequest(**self.pull_request)

        if isinstance(self.repository, dict):
            self.repository = Repository(**self.repository)

        if isinstance(self.sender, dict):
            self.sender = GitHubUser(**self.sender)

