from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .Forms import SignUP, groupform, msg, Group_msg, UserF, ProfileF
from.models import profile, Group, group_message, Notification, message
from .filters import Search
import time


def sign_up(request):
    if request.method == 'POST':
        Form = SignUP(request.POST)
        if Form.is_valid():
            Form.save()
            username = Form.cleaned_data['username']
            password = Form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(f'/accounts/{username}')
    else:
        Form = SignUP()
    return render(request, 'registration/sign_up.html', {'Form': Form})


@login_required
def Edit_profile(request, slug):
    Profile = profile.objects.get(user=request.user)
    profileid = profile.objects.get(slug=slug)
    if profileid == Profile:
        if request.method == 'POST':
            user_form = UserF(request.POST, request.FILES, instance=request.user)
            profile_form = ProfileF(request.POST, request.FILES, instance=Profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                my_profile = profile_form.save(commit=False)
                my_profile.user = request.user
                my_profile.save()
                return redirect('/Ziscord/Home')
        else:
            user_form = UserF(instance=request.user)
            profile_form = ProfileF(instance=Profile)
        return render(request, 'accounts/edit_profile.html',
                  {
                      'userform': user_form,
                      'profileform': profile_form,
                      'profile': Profile,
                      'profileid': profileid,
                  }
                  )
    else:
        return render(request, 'accounts/edit_profile.html',
                      {
                          'profileid': profileid,
                          'profile': Profile
                      }
                      )


@login_required
def start(request):
    return redirect("/Ziscord/Home")


@login_required
def main(request):
    profiles = profile.objects.all()
    userprofile = profile.objects.get(user=request.user)
    groups = Group.objects.all()
    group_messages = group_message.objects.all()
    mymessage = message.objects.filter(receiver=userprofile)
    Msg = message.objects.filter(receiver=userprofile, sent=False)
    Filter = Search(request.GET, queryset=profiles)
    profiles = Filter.qs
    notifications = Notification.objects.filter(reciever=userprofile, read=False)
    my_messages = Msg.count
    context = {
        "profile": userprofile,
        "groups": groups,
        "profiles": profiles,
        'filter': Filter,
        'messages': my_messages,
        'all_messages': mymessage,
        'notifications': notifications,
        'group_messages': group_messages
    }
    return render(request, "accounts/home.html", context)


@login_required
def newgroup(request):
    userprofile = profile.objects.get(user=request.user)
    if request.method == "POST":
        Form = groupform(request.POST, request.FILES)
        if Form.is_valid():
            myform = Form.save(commit=False)
            myform.admin = userprofile
            myform.save()
            return redirect(f"/accounts/group/{myform.slug}/add")
    else:
        Form = groupform()

    context = {
        'user': userprofile,
        'form': Form
    }
    return render(request, 'accounts/Create_group.html', context)


@login_required
def join(request, slug):
    userprofile = profile.objects.get(user=request.user)
    group = Group.objects.get(slug=slug)
    if userprofile in group.members.all():
        group.members.remove(userprofile)
    else:
        group.members.add(userprofile)
    return redirect(f"/accounts/group/{group.slug}/info")


@login_required
def chat(request, slug):
    profiles = profile.objects.all()
    groups = Group.objects.all()
    group_messages = group_message.objects.all()
    Filter = Search(request.GET, queryset=profiles)
    profiles = Filter.qs
    profileid = profile.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    Msg = message.objects.all()
    message.objects.filter(receiver=userprofile, Sender=profileid).update(read=True, sent=True)
    msgs = message.objects.filter(receiver=userprofile, sent=False)
    notifications = Notification.objects.filter(reciever=userprofile, read=False)
    message_notifications = msgs.count
    if request.method == 'POST':
        form_data = msg(request.POST, request.FILES)
        if form_data.is_valid():
            myform = form_data.save()
            myform.receiver = profileid
            myform.Sender = userprofile
            message.objects.filter(Sender=userprofile).update(sent=True)
            myform.save()
            profileid.chatters.add(userprofile)
            userprofile.chatters.add(profileid)
            return redirect(f"/Ziscord/profile/{profileid.slug}/chat")
    else:
        form_data = msg()
    context = {
        'receiver': profileid,
        'profile': userprofile,
        'messages': Msg,
        'Message_Form': form_data,
        "profiles": profiles,
        "groups": groups,
        "filter": Filter,
        "messages_notifications": message_notifications,
        'notifications': notifications,
        'group_messages': group_messages
    }
    print(message_notifications)
    return render(request, 'accounts/Chat.html', context)


@login_required
def msg_reply(request, slug, msgid):
    replied_message = message.objects.get(id=msgid)
    profiles = profile.objects.all()
    groups = Group.objects.all()
    group_messages = group_message.objects.all()
    Filter = Search(request.GET, queryset=profiles)
    profiles = Filter.qs
    profileid = profile.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    Msg = message.objects.all()
    message.objects.filter(receiver=userprofile, Sender=profileid).update(read=True, sent=True)
    msgs = message.objects.filter(receiver=userprofile, sent=False)
    notifications = Notification.objects.filter(reciever=userprofile, read=False)
    message_notifications = msgs.count
    if request.method == 'POST':
        form_data = msg(request.POST, request.FILES)
        if form_data.is_valid():
            myform = form_data.save()
            myform.receiver = profileid
            myform.Sender = userprofile
            myform.reply = replied_message
            message.objects.filter(Sender=userprofile).update(sent=True)
            myform.save()
            profileid.chatters.add(userprofile)
            userprofile.chatters.add(profileid)
            return redirect(f"/Ziscord/profile/{profileid.slug}/chat")
    else:
        form_data = msg()
    context = {
        'receiver': profileid,
        'profile': userprofile,
        'messages': Msg,
        'Message_Form': form_data,
        "profiles": profiles,
        "groups": groups,
        "filter": Filter,
        "messages_notifications": message_notifications,
        'notifications': notifications,
        'message': replied_message,
        'group_messages': group_messages
    }
    print(message_notifications)
    return render(request, 'accounts/msg_reply.html', context)


@login_required
def search(request):
    profiles = profile.objects.all()
    userprofile = profile.objects.get(user=request.user)
    Filter = Search(request.GET, queryset=profiles)
    profiles = Filter.qs
    context = {
        "profile": userprofile,
        "profiles": profiles,
        'filter': Filter
    }
    return render(request, "accounts/search.html", context)


@login_required
def confirm_account_deletion(request):
    return render(request, "accounts/confirm.html")


@login_required
def delete_account(request):
    Profile = profile.objects.get(user=request.user)
    Profile.delete()
    return redirect("/accounts/login")


@login_required
def friend_requests(request):
    userprofile = profile.objects.get(user=request.user)
    context = {
        "profile": userprofile
    }
    Notification.objects.filter(reciever=userprofile).update(read=True)
    return render(request, "accounts/friend requests.html", context)


@login_required
def friend_request(request, slug):
    userprofile = profile.objects.get(user=request.user)
    profileid = profile.objects.get(slug=slug)
    if userprofile in profileid.pending.all():
        profileid.pending.remove(userprofile)
        Notification.objects.filter(sender=userprofile, reciever=profileid, read=False).update(read=True)
    else:
        profileid.pending.add(userprofile)
        Notification.objects.create(sender=userprofile, reciever=profileid, read=False)
    return redirect(f"/accounts/{slug}")


@login_required
def accept_request(request, slug):
    userprofile = profile.objects.get(user=request.user)
    profileid = profile.objects.get(slug=slug)
    profileid.friends.add(userprofile)
    userprofile.friends.add(profileid)
    userprofile.pending.remove(profileid)
    return redirect("/accounts/profile/Notifications")


@login_required
def decline_request(request, slug):
    profileid = profile.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    userprofile.pending.remove(profileid)
    return redirect("/accounts/profile/Notifications")


@login_required
def unfriend(request, slug):
    userprofile = profile.objects.get(user=request.user)
    profileid = profile.objects.get(slug=slug)
    userprofile.friends.remove(profileid)
    profileid.friends.remove(userprofile)
    return redirect("/Ziscord/Home")


@login_required
def delete_chat(request, slug):
    userprofile = profile.objects.get(user=request.user)
    profileid = profile.objects.get(slug=slug)
    userprofile.chatters.remove(profileid)
    return redirect("/Ziscord/Home")


@login_required
def not_found(request):
    return render(request, "accounts/not_found.html")


@login_required
def delete_message(request, slug, msgid):
    userprofile = profile.objects.get(user=request.user)
    Msg = message.objects.get(id=msgid)
    if Msg.Sender != userprofile:
        return redirect("/Ziscord/NotFound")
    else:
        Msg.delete()
        return redirect(f"/Ziscord/profile/{slug}/chat")


@login_required
def group_info(request, slug):
    group = Group.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    online_members = group.members.filter(online=True)
    context = {
        'group': group,
        'profile': userprofile,
        'online': online_members
    }
    return render(request, "accounts/group info.html", context)


@login_required
def group_chat(request, slug):
    group = Group.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    messages = group_message.objects.all()
    profiles = profile.objects.all()
    chats = message.objects.all()
    groups = Group.objects.all()
    Filter = Search(request.GET, queryset=profiles)
    profiles = Filter.qs
    unread_messages = group_message.objects.filter(group=group)
    msgs = message.objects.filter(receiver=userprofile, sent=False)
    notifications = Notification.objects.filter(reciever=userprofile, read=False)
    message_notifications = msgs.count
    unread_messages.exclude(readers=userprofile).update(readers=userprofile)
    if request.method == "POST":
        form = Group_msg(request.POST, request.FILES)
        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.sender = userprofile
            my_form.group = group
            my_form.save()
            my_form.readers.add(userprofile)
            return redirect(f"/accounts/group/{slug}")
    else:
        form = Group_msg()
    context = {
        'profile': userprofile,
        'receiver': group,
        'messages': messages,
        'Message_Form': form,
        'groups': groups,
        'profiles': profiles,
        "messages_notifications": message_notifications,
        'notifications': notifications,
        'filter': Filter,
        'all_messages': chats,
        'group_messages': messages,
        }
    return render(request, "accounts/group_chat.html", context)


@login_required
def remove_members(request, slug, memberid):
    group = Group.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    profileid = profile.objects.get(id=memberid)
    if userprofile != group.admin:
        return redirect("/Ziscord/NotFound")
    else:
        group.members.remove(profileid)
        return redirect(f"/accounts/group/{group.slug}/info")


@login_required
def invite(request, slug):
    userprofile = profile.objects.get(user=request.user)
    group = Group.objects.get(slug=slug)
    context = {
        'group': group,
        'profile': userprofile
    }
    return render(request, "accounts/add_members.html", context)


@login_required
def edit_group(request, slug):
    group = Group.objects.get(slug=slug)
    Profile = profile.objects.get(user=request.user)
    if request.method == "POST":
        form = groupform(request.POST, request.FILES, instance=group)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.id = group.id
            myform.save()
            return redirect(f"/accounts/group/{group.slug}/info")
    else:
        form = groupform(instance=group)

    context = {
        "form": form,
        "profile": Profile,
        "group": group,
    }
    return render(request, "accounts/edit_group.html", context)


@login_required
def delete_group(request, slug):
    group = Group.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    if group.admin == userprofile:
        group.delete()
        return redirect("/Ziscord/Home")
    else:
        return redirect("/Ziscord/NotFound")


@login_required
def delete_group_message(request, slug, msgid):
    userprofile = profile.objects.get(user=request.user)
    Msg = group_message.objects.get(id=msgid)
    if Msg.sender != userprofile:
        return redirect("/Ziscord/NotFound")
    else:
        Msg.delete()
        return redirect(f"/accounts/group/{slug}")


@login_required
def add_member(request, slug, memberid):
    group = Group.objects.get(slug=slug)
    profileid = profile.objects.get(id=memberid)
    userprofile = profile.objects.get(user=request.user)
    if profileid in userprofile.friends.all():
        group.members.add(profileid)
        return redirect(f"/accounts/group/{group.slug}/add")
    else:
        return redirect("/Ziscord/NotFound")


@login_required
def group_msg_rely(request, slug, msgid):
    mymsg = group_message.objects.get(id=msgid)
    group = Group.objects.get(slug=slug)
    userprofile = profile.objects.get(user=request.user)
    messages = group_message.objects.all()
    profiles = profile.objects.all()
    chats = message.objects.all()
    groups = Group.objects.all()
    Filter = Search(request.GET, queryset=profiles)
    profiles = Filter.qs
    msgs = message.objects.filter(receiver=userprofile, sent=False)
    notifications = Notification.objects.filter(reciever=userprofile, read=False)
    message_notifications = msgs.count
    if request.method == "POST":
        form = Group_msg(request.POST, request.FILES)
        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.sender = userprofile
            my_form.group = group
            my_form.reply = mymsg
            my_form.save()
            return redirect(f"/accounts/group/{slug}")
    else:
        form = Group_msg()
    context = {
        'profile': userprofile,
        'receiver': group,
        'messages': messages,
        'Message_Form': form,
        'groups': groups,
        'profiles': profiles,
        "messages_notifications": message_notifications,
        'notifications': notifications,
        'filter': Filter,
        'all_messages': chats,
        'message': mymsg,
        'group_messages': messages
        }
    return render(request, "accounts/group_msg_reply.html", context)
# Create your views here.
