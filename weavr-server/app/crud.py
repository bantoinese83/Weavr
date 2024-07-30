from typing import List, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models import (User, Goal, Introduction, Group, GroupMembership, Badge, Leaderboard,
                        LeaderboardEntry, WeavrWisdom, Event, Notification, Message, Post,
                        Comment, Like, UserSettings, Feedback, Report, NotificationSettings,
                        Connection)
from app.schemas import (UserCreate, UserUpdate, GoalCreate, IntroductionCreate, GroupCreate,
                         GroupMembershipCreate, BadgeCreate, LeaderboardCreate, LeaderboardEntryCreate,
                         WeavrWisdomCreate, EventCreate, NotificationCreate, MessageCreate, PostCreate,
                         CommentCreate, LikeCreate, UserSettingsCreate, FeedbackCreate, ReportCreate,
                         NotificationSettingsCreate, ConnectionCreate)


# --- User CRUD operations ---
async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    db_user = User(**user_create.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[Type[User]]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():  # Exclude unset values
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# --- Goal CRUD operations ---
def create_goal(db: Session, goal: GoalCreate, user_id: int) -> Goal:  # Need user_id
    db_goal = Goal(**goal.dict(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def get_goal(db: Session, goal_id: int) -> Optional[Goal]:
    return db.query(Goal).filter(Goal.id == goal_id).first()


def get_goals_by_user(db: Session, user_id: int) -> List[Goal]:
    return db.query(Goal).filter(Goal.user_id == user_id).all()


def update_goal(db: Session, goal_id: int, goal_update: GoalCreate) -> Optional[Goal]:
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal:
        for key, value in goal_update.dict(exclude_unset=True).items():
            setattr(db_goal, key, value)
        db.commit()
        db.refresh(db_goal)
    return db_goal


def delete_goal(db: Session, goal_id: int) -> Optional[Goal]:
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
    return db_goal


# --- Connection CRUD Operations ---
def create_connection(db: Session, connection: ConnectionCreate) -> Connection:
    db_connection = Connection(**connection.dict())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


def get_connection(db: Session, user_id: int, connected_user_id: int) -> Optional[Connection]:
    return db.query(Connection).filter(Connection.user_id == user_id,
                                       Connection.connected_user_id == connected_user_id).first()


def get_connections_for_user(db: Session, user_id: int) -> List[Connection]:
    return db.query(Connection).filter(
        (Connection.user_id == user_id) | (Connection.connected_user_id == user_id)).all()


def update_connection(db: Session, user_id: int, connected_user_id: int, connection_update: ConnectionCreate) -> \
        Optional[Connection]:
    db_connection = get_connection(db, user_id, connected_user_id)
    if db_connection:
        for key, value in connection_update.dict(exclude_unset=True).items():
            setattr(db_connection, key, value)
        db.commit()
        db.refresh(db_connection)
    return db_connection


def delete_connection(db: Session, user_id: int, connected_user_id: int) -> Optional[Connection]:
    db_connection = get_connection(db, user_id, connected_user_id)
    if db_connection:
        db.delete(db_connection)
        db.commit()
    return db_connection


# --- Introduction CRUD operations ---
def create_introduction(db: Session, introduction: IntroductionCreate) -> Introduction:
    db_introduction = Introduction(**introduction.dict())
    db.add(db_introduction)
    db.commit()
    db.refresh(db_introduction)
    return db_introduction


def get_introduction(db: Session, introduction_id: int) -> Optional[Introduction]:
    return db.query(Introduction).filter(Introduction.id == introduction_id).first()


def get_introductions_by_user(db: Session, user_id: int) -> List[Introduction]:
    return db.query(Introduction).filter(
        (Introduction.introducer_id == user_id) | (Introduction.target_user_id == user_id)
    ).all()


def update_introduction(db: Session, introduction_id: int, introduction_update: IntroductionCreate) -> Optional[
    Introduction]:
    db_introduction = get_introduction(db, introduction_id)
    if db_introduction:
        for key, value in introduction_update.dict(exclude_unset=True).items():
            setattr(db_introduction, key, value)
        db.commit()
        db.refresh(db_introduction)
    return db_introduction


def delete_introduction(db: Session, introduction_id: int) -> Optional[Introduction]:
    db_introduction = get_introduction(db, introduction_id)
    if db_introduction:
        db.delete(db_introduction)
        db.commit()
    return db_introduction


# --- Group CRUD operations ---
def create_group(db: Session, group: GroupCreate) -> Group:
    db_group = Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_group(db: Session, group_id: int) -> Optional[Group]:
    return db.query(Group).filter(Group.id == group_id).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Group]]:
    return db.query(Group).offset(skip).limit(limit).all()


def update_group(db: Session, group_id: int, group_update: GroupCreate) -> Optional[Group]:
    db_group = get_group(db, group_id)
    if db_group:
        for key, value in group_update.dict(exclude_unset=True).items():
            setattr(db_group, key, value)
        db.commit()
        db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int) -> Optional[Group]:
    db_group = get_group(db, group_id)
    if db_group:
        db.delete(db_group)
        db.commit()
    return db_group


# --- GroupMembership CRUD operations ---
def create_group_membership(db: Session, group_membership: GroupMembershipCreate) -> GroupMembership:
    db_group_membership = GroupMembership(**group_membership.dict())
    db.add(db_group_membership)
    db.commit()
    db.refresh(db_group_membership)
    return db_group_membership


def get_group_membership(db: Session, user_id: int, group_id: int) -> Optional[GroupMembership]:
    return db.query(GroupMembership).filter(GroupMembership.user_id == user_id,
                                            GroupMembership.group_id == group_id).first()


def get_group_memberships_by_user(db: Session, user_id: int) -> List[GroupMembership]:
    return db.query(GroupMembership).filter(GroupMembership.user_id == user_id).all()


def update_group_membership(db: Session, user_id: int, group_id: int, group_membership_update: GroupMembershipCreate) -> \
        Optional[GroupMembership]:
    db_group_membership = get_group_membership(db, user_id, group_id)
    if db_group_membership:
        for key, value in group_membership_update.dict(exclude_unset=True).items():
            setattr(db_group_membership, key, value)
        db.commit()
        db.refresh(db_group_membership)
    return db_group_membership


def delete_group_membership(db: Session, user_id: int, group_id: int) -> Optional[GroupMembership]:
    db_group_membership = get_group_membership(db, user_id, group_id)
    if db_group_membership:
        db.delete(db_group_membership)
        db.commit()
    return db_group_membership


# --- Badge CRUD operations ---
def create_badge(db: Session, badge: BadgeCreate) -> Badge:
    db_badge = Badge(**badge.dict())
    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)
    return db_badge


def get_badge(db: Session, badge_id: int) -> Optional[Badge]:
    return db.query(Badge).filter(Badge.id == badge_id).first()


def get_badges(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Badge]]:
    return db.query(Badge).offset(skip).limit(limit).all()


def update_badge(db: Session, badge_id: int, badge_update: BadgeCreate) -> Optional[Badge]:
    db_badge = get_badge(db, badge_id)
    if db_badge:
        for key, value in badge_update.dict(exclude_unset=True).items():
            setattr(db_badge, key, value)
        db.commit()
        db.refresh(db_badge)
    return db_badge


def delete_badge(db: Session, badge_id: int) -> Optional[Badge]:
    db_badge = get_badge(db, badge_id)
    if db_badge:
        db.delete(db_badge)
        db.commit()
    return db_badge


# --- Leaderboard CRUD operations ---
def create_leaderboard(db: Session, leaderboard: LeaderboardCreate) -> Leaderboard:
    db_leaderboard = Leaderboard(**leaderboard.dict())
    db.add(db_leaderboard)
    db.commit()
    db.refresh(db_leaderboard)
    return db_leaderboard


def get_leaderboard(db: Session, leaderboard_id: int) -> Optional[Leaderboard]:
    return db.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).first()


def get_leaderboards(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Leaderboard]]:
    return db.query(Leaderboard).offset(skip).limit(limit).all()


def update_leaderboard(db: Session, leaderboard_id: int, leaderboard_update: LeaderboardCreate) -> Optional[
    Leaderboard]:
    db_leaderboard = get_leaderboard(db, leaderboard_id)
    if db_leaderboard:
        for key, value in leaderboard_update.dict(exclude_unset=True).items():
            setattr(db_leaderboard, key, value)
        db.commit()
        db.refresh(db_leaderboard)
    return db_leaderboard


def delete_leaderboard(db: Session, leaderboard_id: int) -> Optional[Leaderboard]:
    db_leaderboard = get_leaderboard(db, leaderboard_id)
    if db_leaderboard:
        db.delete(db_leaderboard)
        db.commit()
    return db_leaderboard


# --- LeaderboardEntry CRUD operations ---
def create_leaderboard_entry(db: Session, leaderboard_entry: LeaderboardEntryCreate) -> LeaderboardEntry:
    db_leaderboard_entry = LeaderboardEntry(**leaderboard_entry.dict())
    db.add(db_leaderboard_entry)
    db.commit()
    db.refresh(db_leaderboard_entry)
    return db_leaderboard_entry


def get_leaderboard_entry(db: Session, leaderboard_entry_id: int) -> Optional[LeaderboardEntry]:
    return db.query(LeaderboardEntry).filter(LeaderboardEntry.id == leaderboard_entry_id).first()


def get_leaderboard_entries_by_leaderboard(db: Session, leaderboard_id: int) -> List[LeaderboardEntry]:
    return db.query(LeaderboardEntry).filter(LeaderboardEntry.leaderboard_id == leaderboard_id).all()


# ... (Add update and delete operations for LeaderboardEntry if needed)

# --- WeavrWisdom CRUD operations ---
def create_weavr_wisdom(db: Session, weavr_wisdom: WeavrWisdomCreate) -> WeavrWisdom:
    db_weavr_wisdom = WeavrWisdom(**weavr_wisdom.dict())
    db.add(db_weavr_wisdom)
    db.commit()
    db.refresh(db_weavr_wisdom)
    return db_weavr_wisdom


def get_weavr_wisdom(db: Session, wisdom_id: int) -> Optional[WeavrWisdom]:
    return db.query(WeavrWisdom).filter(WeavrWisdom.id == wisdom_id).first()


def get_all_weavr_wisdom(db: Session, skip: int = 0, limit: int = 100) -> list[Type[WeavrWisdom]]:
    return db.query(WeavrWisdom).offset(skip).limit(limit).all()


# ... (Add update and delete operations for WeavrWisdom)

# --- Event CRUD Operations ---
def create_event(db: Session, event: EventCreate) -> Event:
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()


def get_all_events(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Event]]:
    return db.query(Event).offset(skip).limit(limit).all()


# ... (Add update and delete operations for Event)

# --- Notification CRUD Operations ---
def create_notification(db: Session, notification: NotificationCreate) -> Notification:
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_notification(db: Session, notification_id: int) -> Optional[Notification]:
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_notifications_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
    return db.query(Notification).filter(Notification.user_id == user_id).offset(skip).limit(limit).all()


# ... (Add update and delete operations for Notification)

# --- Message CRUD Operations ---
def create_message(db: Session, message: MessageCreate) -> Message:
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_conversation(db: Session, user1_id: int, user2_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
    return db.query(Message).filter(
        ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
        ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
    ).offset(skip).limit(limit).all()


def get_messages_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
    return db.query(Message).filter(Message.sender_id == user_id).offset(skip).limit(limit).all()


def update_message(db: Session, message_id: int, message_update: MessageCreate) -> list[Message]:
    db_message = get_messages_for_user(db, message_id)
    if db_message:
        for key, value in message_update.dict(exclude_unset=True).items():
            setattr(db_message, key, value)
        db.commit()
        db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int) -> list[Message]:
    db_message = get_messages_for_user(db, message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message


# --- Post CRUD Operations ---
def create_post(db: Session, post: PostCreate, author_id: int) -> Post:
    db_post = Post(**post.dict(), author_id=author_id)  # Pass author_id here
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()


def get_all_posts(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Post]]:
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def update_post(db: Session, post_id: int, post_update: PostCreate) -> Optional[Post]:
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in post_update.dict(exclude_unset=True).items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> Optional[Post]:
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post


# --- Comment CRUD Operations ---
def create_comment(db: Session, comment: CommentCreate, author_id: int, post_id: int) -> Comment:
    db_comment = Comment(**comment.dict(), author_id=author_id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int) -> Optional[Comment]:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_comments_for_post(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).offset(skip).limit(
        limit).all()


def update_comment(db: Session, comment_id: int, comment_update: CommentCreate) -> Optional[Comment]:
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment_update.dict(exclude_unset=True).items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int) -> Optional[Comment]:
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment


# --- Like CRUD Operations ---
def create_like(db: Session, like: LikeCreate) -> Like:
    db_like = Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def get_like(db: Session, user_id: int, post_id: int = None, comment_id: int = None) -> Optional[Like]:
    query = db.query(Like).filter(Like.user_id == user_id)
    if post_id:
        query = query.filter(Like.post_id == post_id)
    if comment_id:
        query = query.filter(Like.comment_id == comment_id)
    return query.first()


def delete_like(db: Session, like_id: int) -> Optional[Like]:
    db_like = db.query(Like).filter(Like.id == like_id).first()
    if db_like:
        db.delete(db_like)
        db.commit()
    return db_like


# --- UserSettings CRUD operations ---
def create_user_settings(db: Session, user_settings: UserSettingsCreate, user_id: int) -> UserSettings:
    db_settings = UserSettings(**user_settings.dict(), user_id=user_id)
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings


def get_user_settings(db: Session, user_id: int) -> Optional[UserSettings]:
    return db.query(UserSettings).filter(UserSettings.user_id == user_id).first()


def update_user_settings(db: Session, user_id: int, user_settings_update: UserSettingsCreate) -> Optional[UserSettings]:
    db_settings = get_user_settings(db, user_id)
    if db_settings:
        for key, value in user_settings_update.dict(exclude_unset=True).items():
            setattr(db_settings, key, value)
        db.commit()
        db.refresh(db_settings)
    return db_settings


# --- Feedback CRUD operations ---
def create_feedback(db: Session, feedback: FeedbackCreate, user_id: int) -> Feedback:
    db_feedback = Feedback(**feedback.dict(), user_id=user_id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def get_feedback(db: Session, feedback_id: int) -> Optional[Feedback]:
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()


def get_all_feedback(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Feedback]]:
    return db.query(Feedback).offset(skip).limit(limit).all()


# --- Report CRUD operations ---
def create_report(db: Session, report: ReportCreate, user_id: int) -> Report:
    db_report = Report(**report.dict(), user_id=user_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report(db: Session, report_id: int) -> Optional[Report]:
    return db.query(Report).filter(Report.id == report_id).first()


def get_all_reports(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Report]]:
    return db.query(Report).offset(skip).limit(limit).all()


# --- NotificationSettings CRUD operations ---
def create_notification_settings(db: Session, notification_settings: NotificationSettingsCreate,
                                 user_id: int) -> NotificationSettings:
    db_notification_settings = NotificationSettings(**notification_settings.dict(), user_id=user_id)
    db.add(db_notification_settings)
    db.commit()
    db.refresh(db_notification_settings)
    return db_notification_settings


def get_notification_settings(db: Session, user_id: int) -> Optional[NotificationSettings]:
    return db.query(NotificationSettings).filter(NotificationSettings.user_id == user_id).first()


def update_notification_settings(db: Session, user_id: int, notification_settings_update: NotificationSettingsCreate) -> \
        Optional[NotificationSettings]:
    db_notification_settings = get_notification_settings(db, user_id)
    if db_notification_settings:
        for key, value in notification_settings_update.dict(exclude_unset=True).items():
            setattr(db_notification_settings, key, value)
        db.commit()
        db.refresh(db_notification_settings)
    return db_notification_settings


def update_weavr_wisdom(db: Session, wisdom_id: int, weavr_wisdom_update: WeavrWisdomCreate) -> Optional[WeavrWisdom]:
    db_weavr_wisdom = get_weavr_wisdom(db, wisdom_id)
    if db_weavr_wisdom:
        for key, value in weavr_wisdom_update.dict(exclude_unset=True).items():
            setattr(db_weavr_wisdom, key, value)
        db.commit()
        db.refresh(db_weavr_wisdom)
    return db_weavr_wisdom


def delete_weavr_wisdom(db: Session, wisdom_id: int) -> Optional[WeavrWisdom]:
    db_weavr_wisdom = get_weavr_wisdom(db, wisdom_id)
    if db_weavr_wisdom:
        db.delete(db_weavr_wisdom)
        db.commit()
    return db_weavr_wisdom


def update_event(db: Session, event_id: int, event_update: EventCreate) -> Optional[Event]:
    db_event = get_event(db, event_id)
    if db_event:
        for key, value in event_update.dict(exclude_unset=True).items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int) -> Optional[Event]:
    db_event = get_event(db, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event


def update_notification(db: Session, notification_id: int, notification_update: NotificationCreate) -> Optional[
    Notification]:
    db_notification = get_notification(db, notification_id)
    if db_notification:
        for key, value in notification_update.dict(exclude_unset=True).items():
            setattr(db_notification, key, value)
        db.commit()
        db.refresh(db_notification)
    return db_notification


def delete_notification(db: Session, notification_id: int) -> Optional[Notification]:
    db_notification = get_notification(db, notification_id)
    if db_notification:
        db.delete(db_notification)
        db.commit()
    return db_notification
