from dataclasses import dataclass
from typing import Optional, List

from server.models.base import Base
from server.models.githubRepo import Repository
from server.models.githubUser import GitHubUser

@dataclass()
class PushPayload(Base):
    after: str
    base_ref: Optional[str]
    before: str
    commits: List[object]
    compare: str
    created: bool
    deleted: bool
    forced: bool
    head_commit: Optional[object]
    pusher: Optional[object]
    ref: str
    repository: Repository
    sender: GitHubUser
    enterprise: Optional[object] = None
    installation: Optional[object] = None
    organization: Optional[object] = None

    def __post_init__(self):
        if isinstance(self.repository, dict):
            self.repository = Repository(**self.repository)

        if isinstance(self.sender, dict):
            self.sender = GitHubUser(**self.sender)

