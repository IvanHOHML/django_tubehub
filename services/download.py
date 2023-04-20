from datetime import datetime
from pytube import Playlist
from moviepy.editor import *
import os
import shutil
import re
import glob
import logging
logger = logging.getLogger('django')
def download(form):
    try:
        # 1. Update DB record
        print("Step 1 - DB entry")
        logger.info("Creating database entry to record this request.")
        playlist = form.save(commit=False)
        p = Playlist(playlist.url)
        logger.info("Completed - Database entry creation.")

        # 2. Clean up dir
        logger.info("Cleaning up output dir.")
        output_path = directory_cleanup()
        zip_dir_path = output_path + "TubeHubPlaylist"
        logger.info("Completed - Directory clean up.")

        # 3. Donwload songs from playlist to new
        logger.info("Downloading all songs in playlist through PyTube services.")
        download_service(p, zip_dir_path)
        logger.info("Completed - Download")

        # 4. Zip the directory
        logger.info("Compressing output dir for user to download as HTTP request")
        shutil.make_archive(zip_dir_path, 'zip', zip_dir_path)
        output_zip = zip_dir_path + ".zip"
        logger.info("Completed - Compressing output file.")

        # 5. Return Zip File and pass to View
        return return_process(playlist, 200, output_zip)
    except Exception as e:
        logger.error(e)
        return return_process(playlist, 404, e)

def download_service(p,output_path):
    for video in p.videos:
        try:
            st = video.streams.get_audio_only(subtype='mp3')
            title = re.sub('[^0-9a-zA-Z\u4e00-\u9fff]+', '_', video.title)
            full_file_path = output_path + "/" + title
            logger.info("Downloading MP3 - " + title)
            try:
                st.download(filename=full_file_path + ".mp3")
            except Exception as e:
                try:
                    logger.info("Exception found - No MP3 version is found. Now downloading MP4 version.")
                    st = video.streams.get_audio_only(subtype='mp4')
                    st.download(filename=full_file_path + ".mp4")
                    logger.info("MP4 version has been downloaded successfully. Now converting MP4 file to MP3 file.")
                    mp4_to_mp3(full_file_path)
                    logger.info("Conversion for " + title + " has been completed successfully.")
                except Exception as e2:
                    logger.info("Unexpected Error found. Will skip this song - " + title)
                    continue
        except Exception as e3:
            logger.info("Unexpected Error found. Will skip this song - " + title)
            continue
def mp4_to_mp3(title):
    try:
        FILETOCONVERT = AudioFileClip(title+ ".mp4")
        FILETOCONVERT.write_audiofile(title + ".mp3")
        os.remove(title + ".mp4")
        FILETOCONVERT.close()
    except Exception as e:
        print(e)
        try:
            FILETOCONVERT = AudioFileClip(title)
            FILETOCONVERT.write_audiofile(title + ".mp3")
            os.remove(title)
            FILETOCONVERT.close()
        except Exception as e2:
            print("Failure (MP4 to MP3) - " + title)
            return
def return_process(playlist, status_code, response_content="Unknown Error"):
    # Update DB
    playlist.pub_date = datetime.now()
    playlist.status_code = status_code
    playlist.save()
    return {
        "status_code":status_code,
        "content":response_content
    }
def directory_cleanup():
    dir_path = os.getcwd() + "/song/output/"
    files_inside = glob.glob(dir_path + "TubeHubPlaylist/*")
    files_outside = glob.glob(dir_path + "*")
    for f in files_inside:
        os.remove(f)
    for f in files_outside:
        if os.path.isfile(f):
            os.remove(f)
    return dir_path
