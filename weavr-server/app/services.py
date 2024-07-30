from datetime import date, timedelta
from typing import List, Type, Optional

from sqlalchemy.orm import Session, relationship

from app.crud import (
    create_user, get_user, update_user, delete_user,
    create_goal, get_goal, update_goal, delete_goal, get_goals_by_user,
    create_connection, get_connection, get_connections_for_user, update_connection, delete_connection,
    create_introduction, get_introduction, update_introduction, delete_introduction, get_introductions_by_user,
    create_group, get_group, update_group, delete_group,
    create_group_membership, get_group_membership, update_group_membership, delete_group_membership,
    get_group_memberships_by_user,
    create_badge, get_badge, update_badge, delete_badge,
    create_leaderboard, get_leaderboard, delete_leaderboard,
    create_leaderboard_entry, get_leaderboard_entry, get_leaderboard_entries_by_leaderboard,
    create_weavr_wisdom, get_weavr_wisdom, update_weavr_wisdom, delete_weavr_wisdom,
    create_event, get_event, update_event, delete_event,
    create_notification, get_notification, get_notifications_for_user, update_notification, delete_notification,
    create_message, get_conversation, update_message, delete_message,
    create_post, get_post, update_post, delete_post, get_all_posts,
    create_comment, get_comment, update_comment, delete_comment, get_comments_for_post,
    create_like, get_like, delete_like,
    create_user_settings, get_user_settings, update_user_settings,
    create_feedback, get_feedback, get_all_feedback,
    create_report, get_report, get_all_reports,
    create_notification_settings, get_notification_settings, update_notification_settings, get_messages_for_user
)
from app.models import (
    User, Goal, Connection, Introduction, Group, GroupMembership, Badge, Leaderboard,
    LeaderboardEntry, WeavrWisdom, Event, Notification, Message, Post, Comment,
    Like, UserSettings, Feedback, Report, NotificationSettings, user_badges, user_passions, Passion, UserActivity,
    UserPoints
)
from app.schemas import GoalType, IntroductionStatus, WeavrWisdomCategory
from app.schemas import (
    UserCreate, UserUpdate, GoalCreate, ConnectionCreate, IntroductionCreate, GroupCreate,
    GroupMembershipCreate, BadgeCreate, LeaderboardCreate, LeaderboardEntryCreate,
    WeavrWisdomCreate, EventCreate, NotificationCreate, MessageCreate, PostCreate,
    CommentCreate, LikeCreate, UserSettingsCreate, FeedbackCreate, ReportCreate,
    NotificationSettingsCreate
)


# --- User Services ---
def create_user_service(db: Session, user_create: UserCreate) -> User:
    return create_user(db, user_create)


def get_user_service(db: Session, user_id: int) -> User:
    return get_user(db, user_id)


def update_user_service(db: Session, user_id: int, user_update: UserUpdate) -> User:
    return update_user(db, user_id, user_update)


def delete_user_service(db: Session, user_id: int) -> User:
    return delete_user(db, user_id)


# --- Goal Services ---
def create_goal_service(db: Session, goal_create: GoalCreate, user_id: int) -> Goal:
    return create_goal(db, goal_create, user_id)


def get_goal_service(db: Session, goal_id: int) -> Goal:
    return get_goal(db, goal_id)


def get_goals_by_user_service(db: Session, user_id: int) -> List[Goal]:
    return get_goals_by_user(db, user_id)


def update_goal_service(db: Session, goal_id: int, goal_update: GoalCreate) -> Goal:
    return update_goal(db, goal_id, goal_update)


def delete_goal_service(db: Session, goal_id: int) -> Goal:
    return delete_goal(db, goal_id)


# --- Connection Services ---
def create_connection_service(db: Session, connection_create: ConnectionCreate) -> Connection:
    return create_connection(db, connection_create)


def get_connection_service(db: Session, user_id: int, connected_user_id: int) -> Connection:
    return get_connection(db, user_id, connected_user_id)


def get_connections_for_user_service(db: Session, user_id: int) -> List[Connection]:
    return get_connections_for_user(db, user_id)


def update_connection_service(db: Session, user_id: int, connected_user_id: int,
                              connection_update: ConnectionCreate) -> Connection:
    return update_connection(db, user_id, connected_user_id, connection_update)


def delete_connection_service(db: Session, user_id: int, connected_user_id: int) -> Connection:
    return delete_connection(db, user_id, connected_user_id)


# --- Introduction Services ---
def create_introduction_service(db: Session, introduction_create: IntroductionCreate) -> Introduction:
    return create_introduction(db, introduction_create)


def get_introduction_service(db: Session, introduction_id: int) -> Introduction:
    return get_introduction(db, introduction_id)


def get_introductions_by_user_service(db: Session, user_id: int) -> List[Introduction]:
    return get_introductions_by_user(db, user_id)


def update_introduction_service(db: Session, introduction_id: int,
                                introduction_update: IntroductionCreate) -> Introduction:
    return update_introduction(db, introduction_id, introduction_update)


def delete_introduction_service(db: Session, introduction_id: int) -> Introduction:
    return delete_introduction(db, introduction_id)


# --- Group Services ---
def create_group_service(db: Session, group_create: GroupCreate) -> Group:
    return create_group(db, group_create)


def get_group_service(db: Session, group_id: int) -> Group:
    return get_group(db, group_id)


def update_group_service(db: Session, group_id: int, group_update: GroupCreate) -> Group:
    return update_group(db, group_id, group_update)


def delete_group_service(db: Session, group_id: int) -> Group:
    return delete_group(db, group_id)


# --- GroupMembership Services ---
def create_group_membership_service(db: Session, group_membership_create: GroupMembershipCreate) -> GroupMembership:
    return create_group_membership(db, group_membership_create)


def get_group_membership_service(db: Session, user_id: int, group_id: int) -> GroupMembership:
    return get_group_membership(db, user_id, group_id)


def get_group_memberships_by_user_service(db: Session, user_id: int) -> List[GroupMembership]:
    return get_group_memberships_by_user(db, user_id)


def update_group_membership_service(db: Session, user_id: int, group_id: int,
                                    group_membership_update: GroupMembershipCreate) -> GroupMembership:
    return update_group_membership(db, user_id, group_id, group_membership_update)


def delete_group_membership_service(db: Session, user_id: int, group_id: int) -> GroupMembership:
    return delete_group_membership(db, user_id, group_id)


# --- Badge Services ---
def create_badge_service(db: Session, badge_create: BadgeCreate) -> Badge:
    return create_badge(db, badge_create)


def get_badge_service(db: Session, badge_id: int) -> Badge:
    return get_badge(db, badge_id)


def update_badge_service(db: Session, badge_id: int, badge_update: BadgeCreate) -> Badge:
    return update_badge(db, badge_id, badge_update)


def delete_badge_service(db: Session, badge_id: int) -> Badge:
    return delete_badge(db, badge_id)


# --- Leaderboard Services ---
def create_leaderboard_service(db: Session, leaderboard_create: LeaderboardCreate) -> Leaderboard:
    return create_leaderboard(db, leaderboard_create)


def get_leaderboard_service(db: Session, leaderboard_id: int) -> Leaderboard:
    return get_leaderboard(db, leaderboard_id)


def delete_leaderboard_service(db: Session, leaderboard_id: int) -> Leaderboard:
    return delete_leaderboard(db, leaderboard_id)


# --- LeaderboardEntry Services ---
def create_leaderboard_entry_service(db: Session, leaderboard_entry_create: LeaderboardEntryCreate) -> LeaderboardEntry:
    return create_leaderboard_entry(db, leaderboard_entry_create)


def get_leaderboard_entry_service(db: Session, leaderboard_entry_id: int) -> LeaderboardEntry:
    return get_leaderboard_entry(db, leaderboard_entry_id)


def get_leaderboard_entries_by_leaderboard_service(db: Session, leaderboard_id: int) -> List[LeaderboardEntry]:
    return get_leaderboard_entries_by_leaderboard(db, leaderboard_id)


# --- WeavrWisdom Services ---
def create_weavr_wisdom_service(db: Session, weavr_wisdom_create: WeavrWisdomCreate) -> WeavrWisdom:
    return create_weavr_wisdom(db, weavr_wisdom_create)


def get_weavr_wisdom_service(db: Session, wisdom_id: int) -> WeavrWisdom:
    return get_weavr_wisdom(db, wisdom_id)


def update_weavr_wisdom_service(db: Session, wisdom_id: int, weavr_wisdom_update: WeavrWisdomCreate) -> WeavrWisdom:
    return update_weavr_wisdom(db, wisdom_id, weavr_wisdom_update)


def delete_weavr_wisdom_service(db: Session, wisdom_id: int) -> WeavrWisdom:
    return delete_weavr_wisdom(db, wisdom_id)


# --- Event Services ---
def create_event_service(db: Session, event_create: EventCreate) -> Event:
    return create_event(db, event_create)


def get_event_service(db: Session, event_id: int) -> Event:
    return get_event(db, event_id)


def update_event_service(db: Session, event_id: int, event_update: EventCreate) -> Event:
    return update_event(db, event_id, event_update)


def delete_event_service(db: Session, event_id: int) -> Event:
    return delete_event(db, event_id)


# --- Notification Services ---
def create_notification_service(db: Session, notification_create: NotificationCreate) -> Notification:
    return create_notification(db, notification_create)


def get_notification_service(db: Session, notification_id: int) -> Notification:
    return get_notification(db, notification_id)


def get_notifications_for_user_service(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[
    Notification]:
    return get_notifications_for_user(db, user_id, skip, limit)


def update_notification_service(db: Session, notification_id: int,
                                notification_update: NotificationCreate) -> Notification:
    return update_notification(db, notification_id, notification_update)


def delete_notification_service(db: Session, notification_id: int) -> Notification:
    return delete_notification(db, notification_id)


# --- Message Services ---
def create_message_service(db: Session, message_create: MessageCreate) -> Message:
    return create_message(db, message_create)


def get_message_service(db: Session, message_id: int) -> list[Message]:
    return get_messages_for_user(db, message_id)


def get_conversation_service(db: Session, user1_id: int, user2_id: int, skip: int = 0,
                             limit: int = 100) -> List[Message]:
    return get_conversation(db, user1_id, user2_id, skip, limit)


def update_message_service(db: Session, message_id: int, message_update: MessageCreate) -> list[Message]:
    return update_message(db, message_id, message_update)


def delete_message_service(db: Session, message_id: int) -> list[Message]:
    return delete_message(db, message_id)


# --- Post Services ---
def create_post_service(db: Session, post_create: PostCreate, author_id: int) -> Post:
    return create_post(db, post_create, author_id)


def get_post_service(db: Session, post_id: int) -> Post:
    return get_post(db, post_id)


def get_all_posts_service(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Post]]:
    return get_all_posts(db, skip, limit)


def update_post_service(db: Session, post_id: int, post_update: PostCreate) -> Post:
    return update_post(db, post_id, post_update)


def delete_post_service(db: Session, post_id: int) -> Post:
    return delete_post(db, post_id)


# --- Comment Services ---
def create_comment_service(db: Session, comment_create: CommentCreate, author_id: int, post_id: int) -> Comment:
    return create_comment(db, comment_create, author_id, post_id)


def get_comment_service(db: Session, comment_id: int) -> Comment:
    return get_comment(db, comment_id)


def get_comments_for_post_service(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
    return get_comments_for_post(db, post_id, skip, limit)


def update_comment_service(db: Session, comment_id: int, comment_update: CommentCreate) -> Comment:
    return update_comment(db, comment_id, comment_update)


def delete_comment_service(db: Session, comment_id: int) -> Comment:
    return delete_comment(db, comment_id)


# --- Like Services ---
def create_like_service(db: Session, like_create: LikeCreate) -> Like:
    return create_like(db, like_create)


def get_like_service(db: Session, user_id: int, post_id: int = None, comment_id: int = None) -> Like:
    return get_like(db, user_id, post_id, comment_id)


def delete_like_service(db: Session, like_id: int) -> Like:
    return delete_like(db, like_id)


# --- User Settings Services ---
def create_user_settings_service(db: Session, user_settings_create: UserSettingsCreate, user_id: int) -> UserSettings:
    return create_user_settings(db, user_settings_create, user_id)


def get_user_settings_service(db: Session, user_id: int) -> UserSettings:
    return get_user_settings(db, user_id)


def update_user_settings_service(db: Session, user_id: int, user_settings_update: UserSettingsCreate) -> UserSettings:
    return update_user_settings(db, user_id, user_settings_update)


# --- Feedback Services ---
def create_feedback_service(db: Session, feedback_create: FeedbackCreate, user_id: int) -> Feedback:
    return create_feedback(db, feedback_create, user_id)


def get_feedback_service(db: Session, feedback_id: int) -> Feedback:
    return get_feedback(db, feedback_id)


def get_all_feedback_service(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Feedback]]:
    return get_all_feedback(db, skip, limit)


# --- Report Services ---
def create_report_service(db: Session, report_create: ReportCreate, user_id: int) -> Report:
    return create_report(db, report_create, user_id)


def get_report_service(db: Session, report_id: int) -> Report:
    return get_report(db, report_id)


def get_all_reports_service(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Report]]:
    return get_all_reports(db, skip, limit)


# --- Notification Settings Services ---
def create_notification_settings_service(db: Session, notification_settings_create: NotificationSettingsCreate,
                                         user_id: int) -> NotificationSettings:
    return create_notification_settings(db, notification_settings_create, user_id)


def get_notification_settings_service(db: Session, user_id: int) -> NotificationSettings:
    return get_notification_settings(db, user_id)


def update_notification_settings_service(db: Session, user_id: int,
                                         notification_settings_update: NotificationSettingsCreate) -> NotificationSettings:
    return update_notification_settings(db, user_id, notification_settings_update)


# --- New Function: Get User with Passions and Goals ---
def get_user_with_passions_and_goals(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user object along with their associated passions and goals.
    """
    return db.query(User).options(
        relationship("passions"), relationship("goals")
    ).filter(User.id == user_id).first()


# --- New Function:  Get Users with a Specific Passion ---
def get_users_by_passion(db: Session, passion_name: str) -> List[User]:
    """
    Get all users who have a specific passion.
    """
    return db.query(User).join(user_passions).join(Passion).filter(Passion.name == passion_name).all()


# --- New Function: Check if Two Users are Connected ---
def are_users_connected(db: Session, user_id1: int, user_id2: int) -> bool:
    """
    Check if two users are directly connected.
    """
    return get_connection(db, user_id1, user_id2) is not None


# --- New Function: Get Introductions by Status ---
def get_introductions_by_status(db: Session, user_id: int, status: IntroductionStatus) -> List[Introduction]:
    """
    Get introductions for a user filtered by status (pending, accepted, rejected).
    """
    return db.query(Introduction).filter(Introduction.target_user_id == user_id, Introduction.status == status).all()


# --- New Function:  Get Group with Members ---
def get_group_with_members(db: Session, group_id: int) -> Optional[Group]:
    """
    Get a group object along with its members.
    """
    return db.query(Group).options(relationship("members")).filter(Group.id == group_id).first()


# --- New Function:  Get Badges for a User ---
def get_badges_for_user(db: Session, user_id: int) -> list[Type[Badge]]:
    """
    Get all badges earned by a user.
    """
    return db.query(Badge).join(user_badges).filter(user_badges.c.user_id == user_id).all()


# --- New Function: Search Weavr Wisdom ---
def search_weavr_wisdom(db: Session, query: str, category: Optional[WeavrWisdomCategory] = None) -> list[
    Type[WeavrWisdom]]:
    """
    Search the Weavr Wisdom knowledge base by keyword and optionally filter by category.
    """
    search_query = db.query(WeavrWisdom).filter(WeavrWisdom.content.ilike(f"%{query}%"))
    if category:
        search_query = search_query.filter(WeavrWisdom.category == category)
    return search_query.all()


# --- Connection Strength Calculation ---
def calculate_connection_strength(db: Session, user1_id: int, user2_id: int) -> int:
    """
    Calculate the connection strength between two users.
    """
    strength = 0

    # Shared Passions
    user1_passions = {passion.id for passion in get_user_service(db, user1_id).passions}
    user2_passions = {passion.id for passion in get_user_service(db, user2_id).passions}
    shared_passions = len(user1_passions.intersection(user2_passions))
    strength += shared_passions * 2

    # Goal Alignment
    user1_goals = get_goals_by_user_service(db, user1_id)
    for goal in user1_goals:
        if goal.goal_type in (GoalType.collaboration, GoalType.mentorship):
            for passion_name in user2_passions:
                if passion_name.lower() in goal.description.lower():
                    strength += 3

    # Network Proximity -  Call the optimized function
    strength += (5 - get_network_proximity(user1_id, user2_id, db))  # Higher proximity = lower degree

    # Activity & Engagement (add more factors as needed)
    user1_group_ids = {membership.group_id for membership in get_group_memberships_by_user_service(db, user1_id)}
    user2_group_ids = {membership.group_id for membership in get_group_memberships_by_user_service(db, user2_id)}
    shared_group_ids = len(user1_group_ids.intersection(user2_group_ids))
    strength += shared_group_ids * 2

    return min(strength, 5)  # Cap the strength at 5


# --- Network Proximity (Optimized) ---
def get_network_proximity(user1_id: int, user2_id: int, db: Session) -> int:
    """
    Calculate network proximity using sets for efficiency.
    Lower number means closer proximity.
    Returns 999 if no connection is found within 3 degrees.
    """

    # 1st-Degree Connection
    if get_connection(db, user1_id, user2_id) is not None:
        return 1

    # Get all connection IDs for both users
    user1_connections = {conn.connected_user_id for conn in get_connections_for_user_service(db, user1_id)}
    user2_connections = {conn.connected_user_id for conn in get_connections_for_user_service(db, user2_id)}

    # 2nd-Degree Connection (mutual connection)
    if user1_connections.intersection(user2_connections):
        return 2

    # 3rd-Degree Connection (connection of a connection)
    for intermediate_user in user1_connections:
        intermediate_connections = {conn.connected_user_id for conn in
                                    get_connections_for_user_service(db, intermediate_user)}
        if user2_id in intermediate_connections:
            return 3

    return 999  # Not connected within 3 degrees


# --- Gamification & User Engagement Services ---

def award_badge_service(db: Session, user_id: int, badge_name: str) -> Badge:
    """
    Awards a badge to a user.
    """
    badge = db.query(Badge).filter(Badge.name == badge_name).first()
    if not badge:
        raise ValueError(f"Badge with name '{badge_name}' not found.")

    user = get_user_service(db, user_id)
    user.badges.append(badge)
    db.commit()
    return badge


def get_user_rank_service(db: Session, user_id: int, leaderboard_id: int) -> Optional[int]:
    """
    Get the rank of a user on a specific leaderboard.
    """
    entry = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.leaderboard_id == leaderboard_id,
        LeaderboardEntry.user_id == user_id
    ).first()
    return entry.rank if entry else None


def update_leaderboard_service(db: Session, leaderboard_name: str) -> Leaderboard:
    """
    Update the leaderboard by recalculating scores and ranks.
    """
    leaderboard = get_leaderboard_service(db, leaderboard_name)
    entries = get_leaderboard_entries_by_leaderboard_service(db, leaderboard.id)

    for entry in entries:
        entry.score = calculate_leaderboard_score(db, entry.user_id, leaderboard.criteria)

    entries.sort(key=lambda x: x.score, reverse=True)
    for rank, entry in enumerate(entries, start=1):
        entry.rank = rank

    db.commit()
    return leaderboard


def calculate_leaderboard_score(db: Session, user_id: int, criteria: str) -> int:
    """
    Calculate a user's score for a leaderboard based on the defined criteria.
    """
    if criteria == "Weavr Reputation":
        # Example: Base score on number of connections + bonus for intro success
        user = get_user_service(db, user_id)
        score = len(user.connections)
        score += sum(1 for intro in user.introductions_made if intro.status == IntroductionStatus.accepted)
        return score
    elif criteria == "Introductions Made":
        # Example: Score based on number of accepted introductions
        return len([intro for intro in get_introductions_by_user_service(db, user_id) if
                    intro.status == IntroductionStatus.accepted])
    else:
        raise ValueError(f"Unsupported leaderboard criteria: {criteria}")


def get_user_streak(db: Session, user_id: int) -> int:
    today = date.today()
    activities = db.query(UserActivity).filter(UserActivity.user_id == user_id).order_by(UserActivity.date.desc()).all()

    streak = 0
    for activity in activities:
        if activity.date == today - timedelta(days=streak):
            streak += 1
        else:
            break
    return streak


def update_user_streak(db: Session, user_id: int) -> int:
    today = date.today()
    last_activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).order_by(
        UserActivity.date.desc()).first()

    if last_activity and last_activity.date == today:
        return get_user_streak(db, user_id)

    new_activity = UserActivity(user_id=user_id, date=today)
    db.add(new_activity)
    db.commit()
    return get_user_streak(db, user_id)


def award_points_for_action(db: Session, user_id: int, action_type: str, points: int):
    today = date.today()
    new_points = UserPoints(user_id=user_id, action_type=action_type, points=points, date=today)
    db.add(new_points)
    db.commit()


def get_suggested_connections_service(db: Session, user_id: int, limit: int = 5) -> List[User]:
    """
    Get a list of suggested connections for a user based on shared passions and goals.
    """
    user = get_user_service(db, user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")

    # Get all users with shared passions
    shared_passion_users = set()
    for passion in user.passions:
        shared_passion_users.update(get_users_by_passion(db, passion.name))

    # Get all users with shared goals
    shared_goal_users = set()
    for goal in user.goals:
        if goal.goal_type in (GoalType.collaboration, GoalType.mentorship):
            shared_goal_users.update(get_users_by_passion(db, goal.description))

    # Combine and filter out existing connections
    suggested_users = shared_passion_users.union(shared_goal_users) - {user}
    existing_connections = {conn.connected_user_id for conn in get_connections_for_user_service(db, user_id)}
    suggested_users = [suggested_user for suggested_user in suggested_users if suggested_user.id not in existing_connections]

    return suggested_users[:limit]