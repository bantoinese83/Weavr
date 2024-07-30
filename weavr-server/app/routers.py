from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import schemas
from app.crud import create_user
from app.database import get_db
from app.schemas import User, UserCreate
from app.services import (
    get_user_service, update_user_service, delete_user_service,
    create_goal_service, get_goal_service, update_goal_service, delete_goal_service, get_goals_by_user_service,
    create_connection_service, get_connection_service, get_connections_for_user_service, update_connection_service,
    delete_connection_service,
    create_introduction_service, get_introduction_service, update_introduction_service,
    delete_introduction_service, get_introductions_by_user_service,
    create_group_service, get_group_service, update_group_service, delete_group_service,
    create_group_membership_service, get_group_membership_service, update_group_membership_service,
    delete_group_membership_service, get_group_memberships_by_user_service,
    create_badge_service, get_badge_service, update_badge_service, delete_badge_service,
    create_leaderboard_service, get_leaderboard_service, delete_leaderboard_service,
    create_leaderboard_entry_service, get_leaderboard_entry_service, get_leaderboard_entries_by_leaderboard_service,
    create_weavr_wisdom_service, get_weavr_wisdom_service, update_weavr_wisdom_service, delete_weavr_wisdom_service,
    create_event_service, get_event_service, update_event_service, delete_event_service,
    create_notification_service, get_notification_service, get_notifications_for_user_service,
    update_notification_service, delete_notification_service,
    create_message_service, get_message_service, get_conversation_service, update_message_service,
    delete_message_service,
    create_post_service, get_post_service, update_post_service, delete_post_service, get_all_posts_service,
    create_comment_service, get_comment_service, update_comment_service, delete_comment_service,
    get_comments_for_post_service,
    create_like_service, get_like_service, delete_like_service,
    create_user_settings_service, get_user_settings_service, update_user_settings_service,
    create_feedback_service, get_feedback_service, get_all_feedback_service,
    create_report_service, get_report_service, get_all_reports_service,
    create_notification_settings_service, get_notification_settings_service, update_notification_settings_service,
    calculate_connection_strength, get_network_proximity, get_suggested_connections_service, get_user_rank_service,
    update_leaderboard_service, get_user_streak, update_user_streak, award_badge_service, award_points_for_action,
    get_users_by_passion, are_users_connected, get_introductions_by_status, get_group_with_members,
    get_badges_for_user, search_weavr_wisdom,
)

router = APIRouter()


# --- User Routes ---
@router.post("/users/", response_model=User, tags=["users"])
async def create_user_route(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_create)


@router.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    user = get_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=schemas.User, tags=["users"])
def update_user_route(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = update_user_service(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/users/{user_id}", response_model=schemas.User, tags=["users"])
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    user = delete_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# --- Goal Routes ---
@router.post("/goals/", response_model=schemas.Goal, status_code=status.HTTP_201_CREATED, tags=["goals"])
def create_goal_route(goal_create: schemas.GoalCreate, db: Session = Depends(get_db)):
    return create_goal_service(db, goal_create, goal_create.user_id)


@router.get("/goals/{goal_id}", response_model=schemas.Goal, tags=["goals"])
def get_goal_route(goal_id: int, db: Session = Depends(get_db)):
    goal = get_goal_service(db, goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.get("/users/{user_id}/goals", response_model=List[schemas.Goal], tags=["goals"])
def get_goals_by_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_goals_by_user_service(db, user_id)


@router.put("/goals/{goal_id}", response_model=schemas.Goal, tags=["goals"])
def update_goal_route(goal_id: int, goal_update: schemas.GoalCreate, db: Session = Depends(get_db)):
    goal = update_goal_service(db, goal_id, goal_update)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.delete("/goals/{goal_id}", response_model=schemas.Goal, tags=["goals"])
def delete_goal_route(goal_id: int, db: Session = Depends(get_db)):
    goal = delete_goal_service(db, goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


# --- Connection Routes ---
@router.post("/connections/", response_model=schemas.Connection, status_code=status.HTTP_201_CREATED,
             tags=["connections"])
def create_connection_route(connection_create: schemas.ConnectionCreate, db: Session = Depends(get_db)):
    return create_connection_service(db, connection_create)


@router.get("/connections/{user_id}/{connected_user_id}", response_model=schemas.Connection, tags=["connections"])
def get_connection_route(user_id: int, connected_user_id: int, db: Session = Depends(get_db)):
    connection = get_connection_service(db, user_id, connected_user_id)
    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")
    return connection


@router.get("/users/{user_id}/connections", response_model=List[schemas.Connection], tags=["connections"])
def get_connections_for_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_connections_for_user_service(db, user_id)


@router.put("/connections/{user_id}/{connected_user_id}", response_model=schemas.Connection, tags=["connections"])
def update_connection_route(user_id: int, connected_user_id: int, connection_update: schemas.ConnectionCreate,
                            db: Session = Depends(get_db)):
    connection = update_connection_service(db, user_id, connected_user_id, connection_update)
    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")
    return connection


@router.delete("/connections/{user_id}/{connected_user_id}", response_model=schemas.Connection, tags=["connections"])
def delete_connection_route(user_id: int, connected_user_id: int, db: Session = Depends(get_db)):
    connection = delete_connection_service(db, user_id, connected_user_id)
    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")
    return connection


# --- Introduction Routes ---
@router.post("/introductions/", response_model=schemas.Introduction, status_code=status.HTTP_201_CREATED,
             tags=["introductions"])
def create_introduction_route(introduction_create: schemas.IntroductionCreate, db: Session = Depends(get_db)):
    return create_introduction_service(db, introduction_create)


@router.get("/introductions/{introduction_id}", response_model=schemas.Introduction, tags=["introductions"])
def get_introduction_route(introduction_id: int, db: Session = Depends(get_db)):
    introduction = get_introduction_service(db, introduction_id)
    if not introduction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Introduction not found")
    return introduction


@router.get("/users/{user_id}/introductions", response_model=List[schemas.Introduction], tags=["introductions"])
def get_introductions_by_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_introductions_by_user_service(db, user_id)


@router.put("/introductions/{introduction_id}", response_model=schemas.Introduction, tags=["introductions"])
def update_introduction_route(introduction_id: int, introduction_update: schemas.IntroductionCreate,
                              db: Session = Depends(get_db)):
    introduction = update_introduction_service(db, introduction_id, introduction_update)
    if not introduction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Introduction not found")
    return introduction


@router.delete("/introductions/{introduction_id}", response_model=schemas.Introduction, tags=["introductions"])
def delete_introduction_route(introduction_id: int, db: Session = Depends(get_db)):
    introduction = delete_introduction_service(db, introduction_id)
    if not introduction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Introduction not found")
    return introduction


# --- Group Routes ---
@router.post("/groups/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED, tags=["groups"])
def create_group_route(group_create: schemas.GroupCreate, db: Session = Depends(get_db)):
    return create_group_service(db, group_create)


@router.get("/groups/{group_id}", response_model=schemas.Group, tags=["groups"])
def get_group_route(group_id: int, db: Session = Depends(get_db)):
    group = get_group_service(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group


@router.put("/groups/{group_id}", response_model=schemas.Group, tags=["groups"])
def update_group_route(group_id: int, group_update: schemas.GroupCreate, db: Session = Depends(get_db)):
    group = update_group_service(db, group_id, group_update)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group


@router.delete("/groups/{group_id}", response_model=schemas.Group, tags=["groups"])
def delete_group_route(group_id: int, db: Session = Depends(get_db)):
    group = delete_group_service(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group


# --- Group Membership Routes ---
@router.post("/group_memberships/", response_model=schemas.GroupMembership, status_code=status.HTTP_201_CREATED,
             tags=["group_memberships"])
def create_group_membership_route(group_membership_create: schemas.GroupMembershipCreate,
                                  db: Session = Depends(get_db)):
    return create_group_membership_service(db, group_membership_create)


@router.get("/group_memberships/{user_id}/{group_id}", response_model=schemas.GroupMembership,
            tags=["group_memberships"])
def get_group_membership_route(user_id: int, group_id: int, db: Session = Depends(get_db)):
    group_membership = get_group_membership_service(db, user_id, group_id)
    if not group_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")
    return group_membership


@router.get("/users/{user_id}/group_memberships", response_model=List[schemas.GroupMembership],
            tags=["group_memberships"])
def get_group_memberships_by_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_group_memberships_by_user_service(db, user_id)


@router.put("/group_memberships/{user_id}/{group_id}", response_model=schemas.GroupMembership,
            tags=["group_memberships"])
def update_group_membership_route(user_id: int, group_id: int,
                                  group_membership_update: schemas.GroupMembershipCreate,
                                  db: Session = Depends(get_db)):
    group_membership = update_group_membership_service(db, user_id, group_id, group_membership_update)
    if not group_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")
    return group_membership


@router.delete("/group_memberships/{user_id}/{group_id}", response_model=schemas.GroupMembership,
               tags=["group_memberships"])
def delete_group_membership_route(user_id: int, group_id: int, db: Session = Depends(get_db)):
    group_membership = delete_group_membership_service(db, user_id, group_id)
    if not group_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")
    return group_membership


# --- Badge Routes ---
@router.post("/badges/", response_model=schemas.Badge, status_code=status.HTTP_201_CREATED, tags=["badges"])
def create_badge_route(badge_create: schemas.BadgeCreate, db: Session = Depends(get_db)):
    return create_badge_service(db, badge_create)


@router.get("/badges/{badge_id}", response_model=schemas.Badge, tags=["badges"])
def get_badge_route(badge_id: int, db: Session = Depends(get_db)):
    badge = get_badge_service(db, badge_id)
    if not badge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return badge


@router.put("/badges/{badge_id}", response_model=schemas.Badge, tags=["badges"])
def update_badge_route(badge_id: int, badge_update: schemas.BadgeCreate, db: Session = Depends(get_db)):
    badge = update_badge_service(db, badge_id, badge_update)
    if not badge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return badge


@router.delete("/badges/{badge_id}", response_model=schemas.Badge, tags=["badges"])
def delete_badge_route(badge_id: int, db: Session = Depends(get_db)):
    badge = delete_badge_service(db, badge_id)
    if not badge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return badge


@router.get("/users/{user_id}/badges", response_model=List[schemas.Badge], tags=["badges"])
def get_badges_for_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_badges_for_user(db, user_id)


# --- Leaderboard Routes ---
@router.post("/leaderboards/", response_model=schemas.Leaderboard, status_code=status.HTTP_201_CREATED,
             tags=["leaderboards"])
def create_leaderboard_route(leaderboard_create: schemas.LeaderboardCreate, db: Session = Depends(get_db)):
    return create_leaderboard_service(db, leaderboard_create)


@router.get("/leaderboards/{leaderboard_id}", response_model=schemas.Leaderboard, tags=["leaderboards"])
def get_leaderboard_route(leaderboard_id: int, db: Session = Depends(get_db)):
    leaderboard = get_leaderboard_service(db, leaderboard_id)
    if not leaderboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leaderboard not found")
    return leaderboard


@router.put("/leaderboards/{leaderboard_id}", response_model=schemas.Leaderboard, tags=["leaderboards"])
def update_leaderboard_route(leaderboard_id: int, leaderboard_update: schemas.LeaderboardCreate,
                             db: Session = Depends(get_db)):
    leaderboard = update_leaderboard_service(db, leaderboard_id, leaderboard_update)
    if not leaderboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leaderboard not found")
    return leaderboard


@router.delete("/leaderboards/{leaderboard_id}", response_model=schemas.Leaderboard, tags=["leaderboards"])
def delete_leaderboard_route(leaderboard_id: int, db: Session = Depends(get_db)):
    leaderboard = delete_leaderboard_service(db, leaderboard_id)
    if not leaderboard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leaderboard not found")
    return leaderboard


# --- Leaderboard Entry Routes ---
@router.post("/leaderboard_entries/", response_model=schemas.LeaderboardEntry, status_code=status.HTTP_201_CREATED,
             tags=["leaderboard_entries"])
def create_leaderboard_entry_route(leaderboard_entry_create: schemas.LeaderboardEntryCreate,
                                   db: Session = Depends(get_db)):
    return create_leaderboard_entry_service(db, leaderboard_entry_create)


@router.get("/leaderboard_entries/{leaderboard_entry_id}", response_model=schemas.LeaderboardEntry,
            tags=["leaderboard_entries"])
def get_leaderboard_entry_route(leaderboard_entry_id: int, db: Session = Depends(get_db)):
    leaderboard_entry = get_leaderboard_entry_service(db, leaderboard_entry_id)
    if not leaderboard_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leaderboard entry not found")
    return leaderboard_entry


@router.get("/leaderboards/{leaderboard_id}/entries", response_model=List[schemas.LeaderboardEntry],
            tags=["leaderboard_entries"])
def get_leaderboard_entries_by_leaderboard_route(leaderboard_id: int, db: Session = Depends(get_db)):
    return get_leaderboard_entries_by_leaderboard_service(db, leaderboard_id)


# --- WeavrWisdom Routes ---
@router.post("/wisdom/", response_model=schemas.WeavrWisdom, status_code=status.HTTP_201_CREATED, tags=["wisdom"])
def create_weavr_wisdom_route(weavr_wisdom_create: schemas.WeavrWisdomCreate, db: Session = Depends(get_db)):
    return create_weavr_wisdom_service(db, weavr_wisdom_create)


@router.get("/wisdom/{wisdom_id}", response_model=schemas.WeavrWisdom, tags=["wisdom"])
def get_weavr_wisdom_route(wisdom_id: int, db: Session = Depends(get_db)):
    weavr_wisdom = get_weavr_wisdom_service(db, wisdom_id)
    if not weavr_wisdom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weavr Wisdom not found")
    return weavr_wisdom


@router.put("/wisdom/{wisdom_id}", response_model=schemas.WeavrWisdom, tags=["wisdom"])
def update_weavr_wisdom_route(wisdom_id: int, weavr_wisdom_update: schemas.WeavrWisdomCreate,
                              db: Session = Depends(get_db)):
    weavr_wisdom = update_weavr_wisdom_service(db, wisdom_id, weavr_wisdom_update)
    if not weavr_wisdom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weavr Wisdom not found")
    return weavr_wisdom


@router.delete("/wisdom/{wisdom_id}", response_model=schemas.WeavrWisdom, tags=["wisdom"])
def delete_weavr_wisdom_route(wisdom_id: int, db: Session = Depends(get_db)):
    weavr_wisdom = delete_weavr_wisdom_service(db, wisdom_id)
    if not weavr_wisdom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Weavr Wisdom not found")
    return weavr_wisdom


# --- Event Routes ---
@router.post("/events/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED, tags=["events"])
def create_event_route(event_create: schemas.EventCreate, db: Session = Depends(get_db)):
    return create_event_service(db, event_create)


@router.get("/events/{event_id}", response_model=schemas.Event, tags=["events"])
def get_event_route(event_id: int, db: Session = Depends(get_db)):
    event = get_event_service(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.put("/events/{event_id}", response_model=schemas.Event, tags=["events"])
def update_event_route(event_id: int, event_update: schemas.EventCreate, db: Session = Depends(get_db)):
    event = update_event_service(db, event_id, event_update)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.delete("/events/{event_id}", response_model=schemas.Event, tags=["events"])
def delete_event_route(event_id: int, db: Session = Depends(get_db)):
    event = delete_event_service(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


# --- Notification Routes ---
@router.post("/notifications/", response_model=schemas.Notification, status_code=status.HTTP_201_CREATED,
             tags=["notifications"])
def create_notification_route(notification_create: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return create_notification_service(db, notification_create)


@router.get("/notifications/{notification_id}", response_model=schemas.Notification, tags=["notifications"])
def get_notification_route(notification_id: int, db: Session = Depends(get_db)):
    notification = get_notification_service(db, notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification


@router.get("/users/{user_id}/notifications", response_model=List[schemas.Notification], tags=["notifications"])
def get_notifications_for_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_notifications_for_user_service(db, user_id)


@router.put("/notifications/{notification_id}", response_model=schemas.Notification, tags=["notifications"])
def update_notification_route(notification_id: int, notification_update: schemas.NotificationCreate,
                              db: Session = Depends(get_db)):
    notification = update_notification_service(db, notification_id, notification_update)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification


@router.delete("/notifications/{notification_id}", response_model=schemas.Notification, tags=["notifications"])
def delete_notification_route(notification_id: int, db: Session = Depends(get_db)):
    notification = delete_notification_service(db, notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification


# --- Message Routes ---
@router.post("/messages/", response_model=schemas.Message, status_code=status.HTTP_201_CREATED, tags=["messages"])
def create_message_route(message_create: schemas.MessageCreate, db: Session = Depends(get_db)):
    return create_message_service(db, message_create)


@router.get("/messages/{message_id}", response_model=schemas.Message, tags=["messages"])
def get_message_route(message_id: int, db: Session = Depends(get_db)):
    message = get_message_service(db, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message


@router.get("/conversations/{user1_id}/{user2_id}", response_model=List[schemas.Message], tags=["messages"])
def get_conversation_route(user1_id: int, user2_id: int, skip: int = 0, limit: int = 100,
                           db: Session = Depends(get_db)):
    return get_conversation_service(db, user1_id, user2_id, skip, limit)


@router.put("/messages/{message_id}", response_model=schemas.Message, tags=["messages"])
def update_message_route(message_id: int, message_update: schemas.MessageCreate, db: Session = Depends(get_db)):
    message = update_message_service(db, message_id, message_update)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message


@router.delete("/messages/{message_id}", response_model=schemas.Message, tags=["messages"])
def delete_message_route(message_id: int, db: Session = Depends(get_db)):
    message = delete_message_service(db, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message


# --- Post Routes ---
@router.post("/posts/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED, tags=["posts"])
def create_post_route(post_create: schemas.PostCreate, db: Session = Depends(get_db)):
    return create_post_service(db, post_create, post_create.author_id)


@router.get("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def get_post_route(post_id: int, db: Session = Depends(get_db)):
    post = get_post_service(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.get("/posts/", response_model=List[schemas.Post], tags=["posts"])
def get_all_posts_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_all_posts_service(db, skip, limit)


@router.put("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def update_post_route(post_id: int, post_update: schemas.PostCreate, db: Session = Depends(get_db)):
    post = update_post_service(db, post_id, post_update)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def delete_post_route(post_id: int, db: Session = Depends(get_db)):
    post = delete_post_service(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


# --- Comment Routes ---
@router.post("/comments/", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED, tags=["comments"])
def create_comment_route(comment_create: schemas.CommentCreate, db: Session = Depends(get_db)):
    return create_comment_service(db, comment_create, comment_create.author_id, comment_create.post_id)


@router.get("/comments/{comment_id}", response_model=schemas.Comment, tags=["comments"])
def get_comment_route(comment_id: int, db: Session = Depends(get_db)):
    comment = get_comment_service(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.get("/posts/{post_id}/comments", response_model=List[schemas.Comment], tags=["comments"])
def get_comments_for_post_route(post_id: int, db: Session = Depends(get_db)):
    return get_comments_for_post_service(db, post_id)


@router.put("/comments/{comment_id}", response_model=schemas.Comment, tags=["comments"])
def update_comment_route(comment_id: int, comment_update: schemas.CommentCreate, db: Session = Depends(get_db)):
    comment = update_comment_service(db, comment_id, comment_update)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.delete("/comments/{comment_id}", response_model=schemas.Comment, tags=["comments"])
def delete_comment_route(comment_id: int, db: Session = Depends(get_db)):
    comment = delete_comment_service(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


# --- Like Routes ---
@router.post("/likes/", response_model=schemas.Like, status_code=status.HTTP_201_CREATED, tags=["likes"])
def create_like_route(like_create: schemas.LikeCreate, db: Session = Depends(get_db)):
    return create_like_service(db, like_create)


@router.get("/likes/{like_id}", response_model=schemas.Like, tags=["likes"])
def get_like_route(like_id: int, db: Session = Depends(get_db)):
    like = get_like_service(db, like_id)
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    return like


@router.delete("/likes/{like_id}", response_model=schemas.Like, tags=["likes"])
def delete_like_route(like_id: int, db: Session = Depends(get_db)):
    like = delete_like_service(db, like_id)
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    return like


# --- User Settings Routes ---
@router.post("/user_settings/", response_model=schemas.UserSettings, status_code=status.HTTP_201_CREATED,
             tags=["user_settings"])
def create_user_settings_route(user_settings_create: schemas.UserSettingsCreate, db: Session = Depends(get_db)):
    return create_user_settings_service(db, user_settings_create, user_settings_create.user_id)


@router.get("/user_settings/{user_id}", response_model=schemas.UserSettings, tags=["user_settings"])
def get_user_settings_route(user_id: int, db: Session = Depends(get_db)):
    user_settings = get_user_settings_service(db, user_id)
    if not user_settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")
    return user_settings


@router.put("/user_settings/{user_id}", response_model=schemas.UserSettings, tags=["user_settings"])
def update_user_settings_route(user_id: int, user_settings_update: schemas.UserSettingsCreate,
                               db: Session = Depends(get_db)):
    user_settings = update_user_settings_service(db, user_id, user_settings_update)
    if not user_settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")
    return user_settings


# --- Feedback Routes ---
@router.post("/feedback/", response_model=schemas.Feedback, status_code=status.HTTP_201_CREATED, tags=["feedback"])
def create_feedback_route(feedback_create: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return create_feedback_service(db, feedback_create, feedback_create.user_id)


@router.get("/feedback/{feedback_id}", response_model=schemas.Feedback, tags=["feedback"])
def get_feedback_route(feedback_id: int, db: Session = Depends(get_db)):
    feedback = get_feedback_service(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return feedback


@router.get("/feedback/", response_model=List[schemas.Feedback], tags=["feedback"])
def get_all_feedback_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_all_feedback_service(db, skip, limit)


# --- Report Routes ---
@router.post("/reports/", response_model=schemas.Report, status_code=status.HTTP_201_CREATED, tags=["reports"])
def create_report_route(report_create: schemas.ReportCreate, db: Session = Depends(get_db)):
    return create_report_service(db, report_create, report_create.user_id)


@router.get("/reports/{report_id}", response_model=schemas.Report, tags=["reports"])
def get_report_route(report_id: int, db: Session = Depends(get_db)):
    report = get_report_service(db, report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.get("/reports/", response_model=List[schemas.Report], tags=["reports"])
def get_all_reports_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_all_reports_service(db, skip, limit)


# --- Notification Settings Routes ---
@router.post("/notification_settings/", response_model=schemas.NotificationSettings,
             status_code=status.HTTP_201_CREATED, tags=["notification_settings"])
def create_notification_settings_route(notification_settings_create: schemas.NotificationSettingsCreate,
                                       db: Session = Depends(get_db)):
    return create_notification_settings_service(db, notification_settings_create,
                                                notification_settings_create.user_id)


@router.get("/notification_settings/{user_id}", response_model=schemas.NotificationSettings,
            tags=["notification_settings"])
def get_notification_settings_route(user_id: int, db: Session = Depends(get_db)):
    notification_settings = get_notification_settings_service(db, user_id)
    if not notification_settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification settings not found")
    return notification_settings


@router.put("/notification_settings/{user_id}", response_model=schemas.NotificationSettings,
            tags=["notification_settings"])
def update_notification_settings_route(user_id: int, notification_settings_update: schemas.NotificationSettingsCreate,
                                       db: Session = Depends(get_db)):
    notification_settings = update_notification_settings_service(db, user_id, notification_settings_update)
    if not notification_settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification settings not found")
    return notification_settings


# --- User Network Routes ---
@router.get("/users/{user_id}/network/proximity", response_model=schemas.NetworkProximity, tags=["network"])
def get_network_proximity_route(user_id: int, db: Session = Depends(get_db)):
    return get_network_proximity(db, user_id)


@router.get("/users/{user_id}/network/suggested_connections", response_model=List[schemas.User], tags=["network"])
def get_suggested_connections_route(user_id: int, db: Session = Depends(get_db)):
    return get_suggested_connections_service(db, user_id)


@router.get("/users/{user_id}/network/rank", response_model=schemas.UserRank, tags=["network"])
def get_user_rank_route(user_id: int, db: Session = Depends(get_db)):
    return get_user_rank_service(db, user_id)


@router.get("/users/{user_id}/network/streak", response_model=schemas.UserStreak, tags=["network"])
def get_user_streak_route(user_id: int, db: Session = Depends(get_db)):
    return get_user_streak(db, user_id)


@router.put("/users/{user_id}/network/streak", response_model=schemas.UserStreak, tags=["network"])
def update_user_streak_route(user_id: int, db: Session = Depends(get_db)):
    return update_user_streak(db, user_id)


@router.get("/users/{user_id}/network/passion", response_model=List[schemas.User], tags=["network"])
def get_users_by_passion_route(user_id: str, db: Session = Depends(get_db)):
    return get_users_by_passion(db, user_id)


@router.get("/users/{user_id}/network/connected", response_model=schemas.ConnectionStatus, tags=["network"])
def are_users_connected_route(user_id: int, other_user_id: int, db: Session = Depends(get_db)):
    return are_users_connected(db, user_id, other_user_id)


# --- Introduction Status Routes ---
@router.get("/users/{user_id}/introductions/{status}", response_model=List[schemas.Introduction],
            tags=["introductions"])
def get_introductions_by_status_route(user_id: int, status: str, db: Session = Depends(get_db)):
    return get_introductions_by_status(db, user_id, status)


# --- Group with Members Routes ---
@router.get("/groups/{group_id}/members", response_model=schemas.GroupWithMembers, tags=["groups"])
def get_group_with_members_route(group_id: int, db: Session = Depends(get_db)):
    return get_group_with_members(db, group_id)


# --- Badge Award Routes ---
@router.post("/users/{user_id}/badges/{badge_id}", response_model=schemas.Badge, status_code=status.HTTP_201_CREATED,
             tags=["badges"])
def award_badge_route(user_id: int, badge_id: str, db: Session = Depends(get_db)):
    return award_badge_service(db, user_id, badge_id)


@router.post("/users/{user_id}/points/{action}", response_model=schemas.User, status_code=status.HTTP_201_CREATED,
             tags=["network"])
def award_points_route(user_id: int, action: str, db: Session = Depends(get_db)):
    return award_points_for_action(db, user_id, action, points=1)


# --- Weavr Wisdom Search Routes ---
@router.get("/wisdom/search", response_model=List[schemas.WeavrWisdom], tags=["wisdom"])
def search_weavr_wisdom_route(query: str, db: Session = Depends(get_db)):
    return search_weavr_wisdom(db, query)


# --- Weavr Routes ---
@router.get("/weavr/calculate_connection_strength", response_model=schemas.ConnectionStrength, tags=["network"])
def calculate_connection_strength_route(db: Session = Depends(get_db)):
    return calculate_connection_strength(db, 1, 2)

