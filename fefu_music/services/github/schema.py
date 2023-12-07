from typing import Optional, Union

from pydantic import BaseModel, EmailStr, HttpUrl


class Plan(BaseModel):
    """DTO to represent a GitHub plan."""

    collaborators: int
    name: str
    space: int
    private_repos: int


class User(BaseModel):
    """DTO to represent a GitHub base user."""

    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: Optional[str] = None
    url: HttpUrl
    html_url: HttpUrl
    followers_url: HttpUrl
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: HttpUrl
    organizations_url: HttpUrl
    repos_url: HttpUrl
    events_url: str
    received_events_url: HttpUrl
    type: str
    site_admin: bool
    name: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: Optional[EmailStr]
    hireable: Optional[bool] = None
    bio: Optional[str] = None
    twitter_username: Optional[str] = None
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str
    plan: Plan
    suspended_at: Optional[str] = None


class PrivateUser(User):
    """DTO to represent a GitHub private user."""

    private_gists: int
    total_private_repos: int
    owned_private_repos: int
    disk_usage: int
    collaborators: int
    two_factor_authentication: bool
    business_plus: bool
    ldap_dn: str


class PublicUser(User):
    """DTO to represent a GitHub public user."""

    private_gists: int
    total_private_repos: int
    owned_private_repos: int
    disk_usage: int
    collaborators: int


GithubUser = Union[PrivateUser, PublicUser]
