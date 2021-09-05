import sys
import json
import requests
api_key = "Your api key here"
from apiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=api_key)
print(youtube)
def get_channel_videos(channel_id):
    
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    print(res)
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    videos = []
    stats=[]
    next_page_token = None
    
    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        #print(json.dumps(res,indent=4))
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    
    return videos
def getStastics(id,api_key):
    statsurl="https://www.googleapis.com/youtube/v3/videos?part=statistics%2CcontentDetails&id="+id+"&key="+api_key
    response_API = requests.get(statsurl)
    newdata=response_API.text
    parse_json=json.loads(newdata)
    return parse_json
videos = get_channel_videos('UCRFbs3bAolgx0Qih5bGSaIw')
sys.stdout = open("filename.txt", "w",encoding="utf-8")
for video in videos:
        print("Title: ",video['snippet']['title'])
        videoUrl='https://www.youtube.com/watch?v='
        id=video['snippet']['resourceId']['videoId']
        #viewCount=x["stastics"]["viewCount"]
        x=getStastics(id,api_key)
        #print(x)
        print("Video URL: ", videoUrl+id)
        print("Description: " ,video['snippet']['description'] )
        print("Upload Date: ", video['snippet']['publishedAt'])
        print("Thumbnail URL: ", video['snippet']['thumbnails']['default']['url'])
        print("ViewCount: ",x['items'][0]['statistics']['viewCount'])
        print("Duration: ",(x['items'][0]['contentDetails']['duration'])[2:])
        #print(viewCount)
        print("\n")
sys.stdout.close()
