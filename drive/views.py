from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialToken
from .models import DriveFile, ActionRecord
import requests
from django.core.mail import send_mail
from django.template import loader
import datetime
from allauth.socialaccount.models import SocialApp


# Create your views here.

def download_files(social_user):
    endpoint = 'https://www.googleapis.com/drive/v3/files'
    max_failed_attempts = 5

    headers = {
        'Authorization': f'Bearer {SocialToken.objects.get(account_id=social_user.id).token}'
    }

    params = {
        'fields': 'nextPageToken,files/id,files/name,files/webViewLink,files/iconLink,files/createdTime,files/modifiedTime',
        'q': f'visibility="anyoneWithLink" and "{social_user.user.email}" in owners and mimeType!="application/vnd.google-apps.folder"',
    }

    do_request = True
    i = 1

    while do_request:
        response = requests.get(endpoint, headers=headers, params=params)

        if response.ok:
            json = response.json()
            for file in json['files']:
                drive_file = DriveFile(
                    user=social_user.user,
                    social_user=social_user,
                    id=file['id'],
                    name=file['name'],
                    url=file['webViewLink'],
                    icon_url=file['iconLink'],
                    created_time=file['createdTime'],
                    modified_time=file['modifiedTime'],
                )
                drive_file.save()
                print(f'{i}) {file["name"]}')
                i += 1

            if 'nextPageToken' in json:
                params['pageToken'] = json['nextPageToken']
            else:
                do_request = False
        else:
            max_failed_attempts -= 1
            if max_failed_attempts <= 0:
                raise Exception(f'Request to Drive API at \'{endpoint}\' failed too many times')

            print(f'Request failed, remaining attempts: {max_failed_attempts}')


def profile(request, *args, **kwargs):
    if str(request.user) == 'AnonymousUser':
        return redirect('/accounts/google/login/')

    try:
        social_user = SocialAccount.objects.get(user__id=request.user.id)
    except:
        return redirect('/accounts/logout/')

    # download_files(social_user)

    user = social_user.user
    files = DriveFile.objects.filter(user=user).order_by('-modified_time')
    picture = social_user.extra_data['picture']
    context = {
        'name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        'picture': picture,
        'files': files,
    }

    return render(request, 'drive/profile.html', context)


def reload(request, *args, **kwargs):
    if str(request.user) == 'AnonymousUser':
        return redirect('/accounts/google/login/')

    try:
        social_user = SocialAccount.objects.get(user__id=request.user.id)
    except:
        return redirect('/accounts/logout/')

    download_files(social_user)
    return redirect('profile')


def process(request, *args, **kwargs):
    if str(request.user) == 'AnonymousUser':
        return redirect('/accounts/google/login/')

    try:
        social_user = SocialAccount.objects.get(user__id=request.user.id)
    except:
        return redirect('/accounts/logout/')

    files_to_delete = []

    timestamp = datetime.datetime.now()

    for prop in request.POST:
        if prop[0:9] == "checkbox_":
            file_id = prop[9:]
            print(file_id)
            url = f'https://www.googleapis.com/drive/v3/files/{file_id}/permissions/anyoneWithLink'
            headers = {
                'Authorization': f'Bearer {SocialToken.objects.get(account_id=social_user.id).token}'
            }
            print(url)
            max_failed_attempts = 5

            do_request = True

            while do_request:
                response = requests.delete(url, headers=headers)

                if response.ok:
                    file = DriveFile.objects.get(id=file_id)
                    file.public = False
                    file.processed_time = timestamp
                    file.save()

                    files_to_delete.append(file)

                    ActionRecord.objects.create(file=file)

                    do_request = False
                else:
                    max_failed_attempts -= 1
                    if max_failed_attempts <= 0:
                        do_request = False
                        # raise Exception(f'Request to Drive API at \'{url}\' failed too many times')

                    print(f'Request failed, remaining attempts: {max_failed_attempts}')

    if len(files_to_delete) > 0:
        html_message = loader.render_to_string(
            'drive/email.html',
            {
                'name': f'{social_user.user.first_name} {social_user.user.last_name}',
                'files': files_to_delete
            }
        )

        send_mail(
            'Cambio de permisos en tus archivos de Google Drive',
            'message',
            'gdpermissionscontroller@gmail.com',
            [social_user.user.email],
            fail_silently=False,
            html_message=html_message,
        )

    return redirect('profile')


def archive(request, *args, **kwargs):
    social_user = SocialAccount.objects.get(user__id=request.user.id)

    context = {
        'name': f'{social_user.user.first_name} {social_user.user.last_name}',
        'email': social_user.user.email,
        'picture': social_user.extra_data['picture'],
        'records': ActionRecord.objects.filter(file__user__id=social_user.user.id).order_by('-date'),
    }
    print(social_user.extra_data['picture'])
    return render(request, 'drive/archive.html', context)

