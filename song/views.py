from django.http import HttpResponse,FileResponse
from django.shortcuts import render
import sys

sys.path.append("..")
from services import download
from song.forms import PlaylistForm

def index(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            download_response = download.download(form)
            if download_response["status_code"] ==200:
                zip_file = open(download_response["content"], 'rb')
                return FileResponse(zip_file)
            else:
                print(download_response)
    context = {
        'form':PlaylistForm()
    }
    return render(request,"song/song.html",context)