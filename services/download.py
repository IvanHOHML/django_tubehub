from datetime import datetime
from pytube import Playlist
from moviepy.editor import *
import os
import shutil
import re
import glob

def download(form):
    try:
        # 1. Update DB record
        print("Step 1 - DB entry")
        playlist = form.save(commit=False)
        p = Playlist(playlist.url)
        print("Step 1 - Completed")

        # 2. Create a new directory
        print("Step 2 - Directory creation now")
        output_path = directory_cleanup()
        zip_dir_path = output_path + "TubeHubPlaylist"
        print("Step 2 - Completed")

        # 3. Donwload songs from playlist to new
        print("Step 3 - Download playlist")
        download_service(p, zip_dir_path)
        print("Step 3 - Completed")

        # 4. Zip the directory
        print("Step 4 - Compress")
        shutil.make_archive(zip_dir_path, 'zip', zip_dir_path)
        output_zip = zip_dir_path + ".zip"
        print("Step 4 - Completed")

        # 5. Return Zip File and pass to View
        return return_process(playlist, 200, output_zip)
    except KeyError:
        return return_process(playlist, 404, "Error - Playlist not found")

def download_service(p,output_path):
    for video in p.videos:
        try:
            st = video.streams.get_audio_only(subtype='mp3')
            title = re.sub('[^0-9a-zA-Z\u4e00-\u9fff]+', '_', video.title)
            full_file_path = output_path + "/" + title
            print("now attemp to download mp3")
            print(full_file_path + ".mp3")
            try:
                st.download(filename=full_file_path + ".mp3")
            except Exception as e:
                try:
                    st = video.streams.get_audio_only(subtype='mp4')
                    print("Exception found - try to download mp4")
                    print(full_file_path)
                    st.download(filename=full_file_path + ".mp4")
                    print("mp4 has been downloaded successfully.")
                    print("Now proceed to convert MP4 to MP3")
                    mp4_to_mp3(full_file_path)
                    print("Download MP4 Successfully - ")
                except Exception as e2:
                    print("Failure - " + title)
                    continue
            # video.streams.first().download()
        except Exception as e3:
            print(e3)
            # print("Failure - " + title)
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
