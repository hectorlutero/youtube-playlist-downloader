from pytube import Playlist
import os

def download_playlist(playlist_url, output_path, selection='all', quality='720p'):
    playlist = Playlist(playlist_url)
    output_folder = os.path.join(output_path, 'playlists', playlist.title)
    os.makedirs(output_folder, exist_ok=True)
    if selection == 'all':
        start_index = 0
        end_index = len(playlist.videos)
    elif '-' in selection:
        start, end = map(int, selection.split('-'))
        start_index = start - 1
        end_index = end
    elif ',' in selection:
        indices = map(int, selection.split(','))
        start_index = min(indices) - 1
        end_index = max(indices) + 1
    else:
        start_index = int(selection) - 1
        end_index = len(playlist.videos)
    
    for index, video in enumerate(playlist.videos[start_index:end_index], start=start_index):
        title = video.title.replace('/', '_').replace('\\', '_')
        filename = f"{index}. {title}.mp4"
        filepath = os.path.join(output_folder, filename)
        if os.path.exists(filepath):
            print(f"'{filename}' already exists. Skipping...")
            continue
        stream = video.streams.filter(res=quality).first()
        if stream:
            try:
                print(f"Downloading '{filename}'...")
                stream.download(output_folder, filename=filename)
                print(f"'{filename}' downloaded successfully.")
            except Exception as e:
                with open('issues.log', 'a') as f:
                    f.write(f"Error downloading '{filename}': {str(e)}\n")
        else:
            print(f"No '{quality}' available for '{filename}'. Skipping...")

if __name__ == "__main__":
    playlist_url = input("Enter the URL of the YouTube playlist: ")
    output_path = input("Enter the directory where you want to save the videos: ")
    selection = input("Enter the selection (e.g., 10-*, 1,2,10, 10-15, all): ")
    selected_quality = input("Enter the desired video quality (e.g., 720p, 480p, etc.): ")
    download_playlist(playlist_url, output_path, selection, selected_quality)
