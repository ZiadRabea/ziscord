from django.urls import path
from .views import sign_up, Edit_profile, newgroup, join, search, confirm_account_deletion, delete_account, \
    friend_requests, decline_request, accept_request, group_chat, group_info, delete_group, edit_group, \
    delete_group_message, group_msg_rely, remove_members, invite, add_member

urlpatterns = [
    path("sign_up/", sign_up),
    path("<str:slug>/", Edit_profile),
    path("groups/create/", newgroup),
    path("group/<str:slug>/join", join),
    path("group/<str:slug>/info", group_info),
    path("group/<str:slug>/delete", delete_group),
    path("group/<str:slug>/edit", edit_group),
    path("group/<str:slug>/add", invite),
    path("group/<str:slug>/<int:memberid>/remove", remove_members),
    path("group/<str:slug>/<int:memberid>/add", add_member),
    path("group/<str:slug>/<int:msgid>/reply", group_msg_rely),
    path("group/<str:slug>/<int:msgid>/delete", delete_group_message),
    path("group/<str:slug>/", group_chat),
    path("Search", search),
    path("profile/delete", confirm_account_deletion),
    path("profile/delete_account", delete_account),
    path("profile/Notifications", friend_requests),
    path("profile/Notifications/<str:slug>/accept", accept_request),
    path("profile/Notifications/<str:slug>/decline", decline_request),
]
