from app.database import engine
from app.models import (
    Base, User, Goal, Connection, Introduction, Group, GroupMembership, Badge, Leaderboard,
    LeaderboardEntry, WeavrWisdom, Event, Notification, Message, Post, Comment,
    Like, UserSettings, Feedback, Report, NotificationSettings, UserActivity, UserPoints, Passion
)


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)