import enum
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum, Table, Index, Date
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# --- Enumerated Types ---
class IntroductionStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class GoalType(enum.Enum):
    career = "career"
    mentorship = "mentorship"
    collaboration = "collaboration"
    other = "other"


class GroupPrivacy(enum.Enum):
    public = "public"
    private = "private"


class WeavrWisdomCategory(enum.Enum):
    networking = "networking"
    career = "career"
    community = "community"
    other = "other"


class RSVPStatus(enum.Enum):
    going = "going"
    interested = "interested"
    not_going = "not_going"


class GroupMemberRole(enum.Enum):
    member = "member"
    admin = "admin"
    moderator = "moderator"


# --- Models ---

# Connection Model
class Connection(Base):
    def __init__(self, **kw: Any):
        super().__init__(**kw)
        self.strength = None

    __tablename__ = "connections"
    __table_args__ = (
        Index('connection_idx', 'user_id', 'connected_user_id', unique=True),
    )

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    connected_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    connection_strength = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="connections")
    connected_user = relationship("User", foreign_keys=[connected_user_id], back_populates="connected_to")


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    location = Column(String)
    headline = Column(String)
    bio = Column(Text)
    profile_picture_url = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    remember_me = Column(Boolean, default=False)

    passions = relationship("Passion", secondary="user_passions", back_populates="users")
    goals = relationship("Goal", back_populates="user")
    connections = relationship("Connection", primaryjoin=id == Connection.user_id, back_populates="user")
    connected_to = relationship("Connection", primaryjoin=id == Connection.connected_user_id, back_populates="connected_user")
    introductions_made = relationship("Introduction", foreign_keys="Introduction.introducer_id", back_populates="introducer")
    introductions_received = relationship("Introduction", foreign_keys="Introduction.target_user_id", back_populates="target_user")
    badges = relationship("Badge", secondary="user_badges", back_populates="users")
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user")
    wisdom_entries = relationship("WeavrWisdom", back_populates="author")
    group_memberships = relationship("GroupMembership", back_populates="user", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    notification_settings = relationship("NotificationSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", secondary="event_attendees", back_populates="attendees")
    activity_level = relationship("UserActivity", back_populates="user", overlaps="activities")
    endorsements = relationship("UserPoints", back_populates="user")
    activities = relationship("UserActivity", back_populates="user", overlaps="activity_level")


# UserActivity Model
class UserActivity(Base):
    __tablename__ = 'user_activity'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    activity_level = Column(Integer, nullable=False)

    user = relationship("User", back_populates="activities")



# UserPoints Model
class UserPoints(Base):
    __tablename__ = 'user_points'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action_type = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="endorsements")



# Passion Model
class Passion(Base):
    __tablename__ = "passions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    users = relationship("User", secondary="user_passions", back_populates="passions")


# User-Passion Association Table
user_passions = Table(
    "user_passions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), index=True),
    Column("passion_id", Integer, ForeignKey("passions.id"), index=True),
)


# Goal Model
class Goal(Base):
    __tablename__ = "goals"

    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    description = Column(Text, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    goal_type = Column(SQLAlchemyEnum(GoalType), default=GoalType.other)

    user = relationship("User", back_populates="goals")


# Introduction Model
class Introduction(Base):
    __tablename__ = "introductions"

    id = Column(Integer, primary_key=True, index=True)
    introducer_id = Column(Integer, ForeignKey("users.id"), index=True)
    introduced_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    target_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message = Column(Text)
    status = Column(Enum(IntroductionStatus), default=IntroductionStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    introducer = relationship("User", foreign_keys=[introducer_id], back_populates="introductions_made")
    introduced_user = relationship("User", foreign_keys=[introduced_user_id])
    target_user = relationship("User", foreign_keys=[target_user_id], back_populates="introductions_received")


# Group Model
class GroupMembership(Base):
    __tablename__ = "group_memberships"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    role = Column(SQLAlchemyEnum(GroupMemberRole), default=GroupMemberRole.member)

    user = relationship("User", back_populates="group_memberships")
    group = relationship("Group", back_populates="members")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    privacy = Column(SQLAlchemyEnum(GroupPrivacy), default=GroupPrivacy.public)

    members = relationship("GroupMembership", back_populates="group", cascade="all, delete-orphan")

# Badge Model
class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon_url = Column(String)

    users = relationship("User", secondary="user_badges", back_populates="badges")


# User-Badge Association Table
user_badges = Table(
    "user_badges",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), index=True),
    Column("badge_id", Integer, ForeignKey("badges.id"), index=True),
    Column("earned_at", DateTime, default=datetime.utcnow),
)


# Leaderboard Model
class Leaderboard(Base):
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    criteria = Column(String, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    entries = relationship("LeaderboardEntry", back_populates="leaderboard")


# Leaderboard Entry Model
class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    leaderboard_id = Column(Integer, ForeignKey("leaderboards.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    score = Column(Integer)
    rank = Column(Integer)

    user = relationship("User", back_populates="leaderboard_entries")
    leaderboard = relationship("Leaderboard", back_populates="entries")


# Weavr Wisdom Model
class WeavrWisdom(Base):
    __tablename__ = "weavr_wisdom"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(Enum(WeavrWisdomCategory), default=WeavrWisdomCategory.other)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    up_votes = Column(Integer, default=0)
    down_votes = Column(Integer, default=0)
    tags = Column(String)

    author = relationship("User", back_populates="wisdom_entries")


# Event Model
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String)
    longitude = Column(String)
    latitude = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    attendees = relationship("User", secondary="event_attendees", back_populates="events")


# Event-Attendee Association Table
event_attendees = Table(
    "event_attendees",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), index=True),
    Column("user_id", Integer, ForeignKey("users.id"), index=True),
    Column("rsvp_status", Enum(RSVPStatus), default=RSVPStatus.interested),
    Column("attended_at", DateTime),  # Make attended_at nullable, as not everyone who RSVPs will attend
)


# Notification Model
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


# Message Model
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), index=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), index=True)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")


# Post Model
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")


# Comment Model
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), index=True)
    author_id = Column(Integer, ForeignKey("users.id"), index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    likes = relationship("Like", back_populates="comment", cascade="all, delete-orphan")


# Like Model
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), index=True)  # Add this line
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")
    comment = relationship("Comment", back_populates="likes")  # And this line


# UserSettings Model
class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    dark_mode = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="settings")


# Feedback Model
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedback")


# Report Model
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    reason = Column(String, nullable=False)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")


# NotificationSettings Model
class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)

    user = relationship("User", back_populates="notification_settings")
