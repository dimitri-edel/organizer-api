""" Definitions of url patterns """
# pylint: disable=E1101
from django.urls import path
from . import views


urlpatterns = [
    path(
        "private-chat-message-count/<int:team_id>/<int:recipient_id>",
        views.PrivateChatMessageCount.as_view(),
    ),
    path(
        "private-chat-list/",
        views.PrivateChatList.as_view(),
    ),
    path(
        "private-chat-post/<int:team_id>/<int:recipient_id>",
        views.PrivateChatPost.as_view(),
    ),
    path(
        "private-chat-put/<int:message_id>",
        views.PrivateChatPut.as_view(),
    ),
]
