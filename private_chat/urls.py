""" Definitions of url patterns for the private chat"""
# pylint: disable=E1101
from django.urls import path
from . import views


urlpatterns = [
    # Get number of messages between request.user and another team
    # member in the private chat
    path(
        "private-chat-message-count/<int:team_id>/<int:recipient_id>",
        views.PrivateChatMessageCount.as_view(),
    ),
    # Get messages between request.user and another user
    # The parameters are passed as GET-parameters
    # @GET-parameter : team_id
    # @GET-parameter: from_user_id
    path(
        "private-chat-list/",
        views.PrivateChatList.as_view(),
    ),
    # Post a message in the private chat
    path(
        "private-chat-post/<int:team_id>/<int:recipient_id>",
        views.PrivateChatPost.as_view(),
    ),
    # Update a message in the private chat
    path(
        "private-chat-put/<int:message_id>",
        views.PrivateChatPut.as_view(),
    ),
    # Delete a message in the private chat
    path("private-chat-delete/<int:message_id>", views.PrivateChatDelete.as_view()),
]
