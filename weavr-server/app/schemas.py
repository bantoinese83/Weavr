from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


# Enumerations
class IntroductionStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class GoalType(str, Enum):
    career = "career"
    mentorship = "mentorship"
    collaboration = "collaboration"
    other = "other"


class GroupPrivacy(str, Enum):
    public = "public"
    private = "private"


class WeavrWisdomCategory(str, Enum):
    networking = "networking"
    career = "career"
    community = "community"
    other = "other"


class RSVPStatus(str, Enum):
    going = "going"
    interested = "interested"
    not_going = "not_going"


class GroupMemberRole(str, Enum):
    member = "member"
    admin = "admin"
    moderator = "moderator"


# --- User Schemas ---
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    location: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    remember_me: Optional[bool] = False


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(UserBase):
    password_hash: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attribute = True


# --- Goal Schemas ---
class GoalBase(BaseModel):
    description: str
    goal_type: Optional[GoalType] = GoalType.other


class GoalCreate(GoalBase):
    user_id: int


class Goal(GoalBase):
    id: int
    user_id: int  # Include user_id in the response
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attribute = True


# --- Connection Schemas ---
class ConnectionBase(BaseModel):
    user_id: int
    connected_user_id: int
    connection_strength: Optional[int] = 1


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    created_at: datetime

    class Config:
        from_attribute = True


# --- Introduction Schemas ---
class IntroductionBase(BaseModel):
    introducer_id: int
    introduced_user_id: int
    target_user_id: int
    message: Optional[str] = None
    status: Optional[IntroductionStatus] = IntroductionStatus.pending


class IntroductionCreate(IntroductionBase):
    pass


class Introduction(IntroductionBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


# --- Group Schemas ---
class GroupBase(BaseModel):
    name: str
    description: str
    privacy: Optional[GroupPrivacy] = GroupPrivacy.public
    rules: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


# --- Group Membership Schemas ---
class GroupMembershipBase(BaseModel):
    user_id: int
    group_id: int
    role: Optional[GroupMemberRole] = GroupMemberRole.member


class GroupMembershipCreate(GroupMembershipBase):
    pass


class GroupMembership(GroupMembershipBase):
    joined_at: datetime

    class Config:
        from_attribute = True


# --- Badge Schemas ---
class BadgeBase(BaseModel):
    name: str
    description: str
    icon_url: Optional[str] = None


class BadgeCreate(BadgeBase):
    pass


class Badge(BadgeBase):
    id: int

    class Config:
        from_attribute = True


# --- Leaderboard Schemas ---
class LeaderboardBase(BaseModel):
    name: str
    criteria: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class LeaderboardCreate(LeaderboardBase):
    pass


class Leaderboard(LeaderboardBase):
    id: int

    class Config:
        from_attribute = True


# --- LeaderboardEntry Schemas ---
class LeaderboardEntryBase(BaseModel):
    leaderboard_id: int
    user_id: int
    score: Optional[int] = None
    rank: Optional[int] = None


class LeaderboardEntryCreate(LeaderboardEntryBase):
    pass


class LeaderboardEntry(LeaderboardEntryBase):
    id: int

    class Config:
        from_attribute = True


# --- WeavrWisdom Schemas ---
class WeavrWisdomBase(BaseModel):
    title: str
    content: str
    category: Optional[WeavrWisdomCategory] = WeavrWisdomCategory.other
    tags: Optional[str] = None


class WeavrWisdomCreate(WeavrWisdomBase):
    author_id: int


class WeavrWisdom(WeavrWisdomBase):
    id: int
    author_id: int  # Include author_id in the response
    created_at: datetime
    updated_at: Optional[datetime] = None
    up_votes: Optional[int] = 0
    down_votes: Optional[int] = 0

    class Config:
        from_attribute = True


# --- Event Schemas ---
class EventBase(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    start_time: datetime
    end_time: datetime


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attribute = True


# --- Notification Schemas ---
class NotificationBase(BaseModel):
    user_id: int
    message: str
    is_read: Optional[bool] = False


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


# --- Message Schemas ---
class MessageBase(BaseModel):
    sender_id: int
    receiver_id: int  # Corrected field name from "recipient_id"
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime
    is_read: bool = False  # Added is_read field

    class Config:
        from_attribute = True


# --- Post Schemas ---
class PostBase(BaseModel):
    author_id: int  # Use author_id for consistency
    content: str
    visibility: Optional[str] = 'public'


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attribute = True


# --- Comment Schemas ---
class CommentBase(BaseModel):
    post_id: int
    author_id: int  # Use author_id for consistency
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


# --- Like Schemas ---
class LikeBase(BaseModel):
    post_id: int
    user_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


# --- UserSettings Schemas ---
class UserSettingsBase(BaseModel):
    theme: Optional[str] = 'light'
    notifications_enabled: Optional[bool] = True


class UserSettingsCreate(UserSettingsBase):
    user_id: int


class UserSettings(UserSettingsBase):
    id: int
    user_id: int  # Include user_id in response

    class Config:
        from_attribute = True


# --- Feedback Schemas ---
class FeedbackBase(BaseModel):
    user_id: int
    message: str  # Changed field name from "content" for clarity


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


# --- Report Schemas ---
class ReportBase(BaseModel):
    user_id: int
    reported_user_id: int
    reason: str
    details: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class Report(ReportBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


# --- NotificationSettings Schemas ---
class NotificationSettingsBase(BaseModel):
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    sms_notifications: Optional[bool] = False


class NotificationSettingsCreate(NotificationSettingsBase):
    user_id: int


class NotificationSettings(NotificationSettingsBase):
    id: int
    user_id: int  # Include user_id in response

    class Config:
        from_attribute = True


class NetworkProximity(BaseModel):
    user_id: int
    connected_user_id: int
    proximity: int
    created_at: datetime

    class Config:
        from_attribute = True


class UserRank(BaseModel):
    user_id: int
    rank: int
    score: int
    created_at: datetime

    class Config:
        from_attribute = True


class UserStreak(BaseModel):
    user_id: int
    streak: int
    created_at: datetime

    class Config:
        from_attribute = True


class ConnectionStatus(BaseModel):
    user_id: int
    connected_user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attribute = True


class GroupWithMembers(BaseModel):
    id: int
    name: str
    description: str
    privacy: GroupPrivacy
    rules: Optional[str] = None
    created_at: datetime
    members: int

    class Config:
        from_attribute = True


class ConnectionStrength(BaseModel):
    user_id: int
    connected_user_id: int
    connection_strength: int
    created_at: datetime

    class Config:
        from_attribute = True