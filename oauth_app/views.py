# oauth_app/views.py
import boto3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from mysite import settings

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
from django.shortcuts import get_object_or_404, render


@login_required
def index(request):
    context = {
        'is_site_admin': request.user.groups.filter(name='Site Admins').exists()
    }
    if request.user.groups.filter(name='Site Admins').exists():
        return render(request, 'admin_user.html')
    else:
        return render(request, 'user.html')

def file_upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the file here. For example, save it to the database or the file system
            #handle_uploaded_file(request.FILES['file'])

            uploaded_file = UploadedFile()
            uploaded_file.incident_type = form.cleaned_data['question_1']
            uploaded_file.organizations_involved = form.cleaned_data['question_2']
            uploaded_file.injuries = form.cleaned_data['question_4']
            uploaded_file.date_and_time = form.cleaned_data['question_5']
            uploaded_file.additional_info = form.cleaned_data['additional_info']
            uploaded_file.who_was_involved = form.cleaned_data['question_3']

            if 'file' in request.FILES:
                uploaded_file.file = request.FILES['file']
            # Associate the file with the current user if authenticated
            uploaded_file.user = request.user if request.user.is_authenticated else None

            # Now save the instance to the database
            uploaded_file.save()
            if request.user.is_authenticated:
                uploaded_file.user = request.user
            else:
                user = get_user_model()
                anonymous_user, created = user.objects.get_or_create(username='anonymous')
                uploaded_file.user = anonymous_user
            uploaded_file.save()
            return HttpResponseRedirect('/success/')  # Redirect to a new URL
    else:
        form = UploadFileForm()  # An empty form for a GET request
    context = {
        'form': form,
        'is_site_admin': request.user.groups.filter(name='Site Admins').exists()
    }
    return render(request, 'file_upload.html', {'form': form})

"""
def handle_uploaded_file(f):
    with open('file_name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)"""

def add_is_site_admin(request):
    return {
        'is_site_admin': request.user.groups.filter(name='Site Admins').exists() if request.user.is_authenticated else False
    }

def list_files_view(request):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2'
    )
    pre_signed_urls = []

    for file in UploadedFile.objects.all():
        user_name = file.user.username if file.user else "Anonymous"
        pre_signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': "static/"+file.file.name,
            },
            ExpiresIn=3600
        )
        pre_signed_urls.append((pre_signed_url, file.file.name, user_name))

    return render(request, 'list_files.html', {'file_urls': pre_signed_urls})


def list_submissions_view(request):
    submissions = UploadedFile.objects.all().order_by('-upload_time')
    return render(request, 'list_submissions.html', {'submissions': submissions})

#changed
def user_submissions_view(request):
    submissions = UploadedFile.objects.filter(user=request.user).order_by('-upload_time')
    return render(request, 'user_submissions.html', {'submissions': submissions})

def delete_submission(request, submission_id):
    submission = UploadedFile.objects.get(id=submission_id)
    if request.user == submission.user: #only deletes if this is the user who submitted it
        submission.delete()
    return redirect('view-my-submissions')


def submission_detail_view(request, submission_id):
    admin = request.user.groups.filter(name='Site Admins').exists()
    submission = UploadedFile.objects.get(id=submission_id)
    is_user = submission.user == request.user

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2'
    )

    file_url = None
    if submission.file:
        file_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': "static/"+submission.file.name,
            },
            ExpiresIn=3600
        )

    if request.method == 'POST':
        status = request.POST.get('status')
        comment = request.POST.get('comment')
        # Update submission status and comment
        submission.status = status
        submission.comment = comment
        submission.save()
        return redirect('list_files')  # Redirect back to the list of submissions after updating
    
    if submission.status == 'New':
        submission.status = 'In Progress'
        submission.save()

    return render(request, 'submission_detail.html', {
        'submission': submission,
        'file_url': file_url,
        'status': submission.status,  # Pass status back to the template
        'comment': submission.comment,  # Pass comment back to the template
        'admin':admin,
        'is_user': is_user
    })
   # return render(request, 'submission_detail.html', {'submission': submission})


def resources_view(request):
    return render(request, 'resources.html')
