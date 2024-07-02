from dataclasses import dataclass
from typing import Optional, List

from server.models.githubRepo import Repository
from server.models.githubUser import GitHubUser

@dataclass()
class PushPayload:
    after: str
    base_ref: Optional[str]
    before: str
    commits: List[object]
    compare: str
    created: bool
    deleted: bool
    enterprise: Optional[object]
    forced: bool
    head_commit: Optional[object]
    installation: Optional[object]
    organization: Optional[object]
    pusher: Optional[object]
    ref: str
    repository: Repository
    sender: GitHubUser
    enterprise: Optional[object]
    installation: Optional[object]

    def __post_init__(self):
        if isinstance(self.repository, dict):
            self.repository = Repository(**self.repository)

        if isinstance(self.sender, dict):
            self.sender = GitHubUser(**self.sender)

