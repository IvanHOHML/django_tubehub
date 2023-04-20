from django.http import HttpResponse,FileResponse
from django.shortcuts import render
import sys
import logging
sys.path.append("..")
from services import download
from song.forms import PlaylistForm

logger = logging.getLogger('django')
def index(request):
    if request.method == "POST":
        logger.info("Client has sent a POST request. Now starts.")
        form = PlaylistForm(request.POST)
        logger.info("Identified client's input - " + request.POST["url"])
        if form.is_valid():
            logger.info("Data input is valid.")
            download_response = download.download(form)
            if download_response["status_code"] ==200:
                logger.info("200 - The Youtube Playlist has been downloaded and compressed in server host directory now.")
                logger.info("Location of zip file - " + download_response["content"])
                zip_file = open(download_response["content"], 'rb')
                logger.info("Server will now return the File Response to Client to download compressed dir.")
                return FileResponse(zip_file)
            else:
                logger.info(str(download_response["status_code"]) + "-" + download_response["content"])
                logger.info("Service has now stopped. No pending action until new request comes in.")

    context = {
        'form':PlaylistForm()
    }
    return render(request,"song/song.html",context)