from instagrapi import Client
import os
import json
from googleapiclient.discovery import build
from pytube import YouTube

def login_to_instagram(username, password, session_file='session.json'):
    client = Client()

    # Cargar la sesión si el archivo existe
    if os.path.exists(session_file):
        client.load_settings(session_file)
        try:
            client.login(username, password)
            print("Sesión cargada exitosamente.")
        except Exception as e:
            print("Error al cargar la sesión:", e)
            client = Client()
            client.login(username, password)
            client.dump_settings(session_file)
            print("Nueva sesión guardada.")
    else:
        client.login(username, password)
        client.dump_settings(session_file)
        print("Sesión guardada exitosamente.")

    return client

def get_top_reels_links(client, target_username, num_reels_to_return, num_reels_to_check, json_key, json_filename='reels_links.json'):
    user_id = client.user_id_from_username(target_username)
    medias = client.user_medias(user_id, amount=num_reels_to_check)
    reels = []

    for media in medias:
        if media.media_type == 2:  # Tipo 2 es para Reels
            media_info = client.media_info(media.id)
            views = media_info.view_count
            reels.append((views, f"https://www.instagram.com/reel/{media.code}/"))

    # Ordenar los reels por la cantidad de vistas en orden descendente
    reels.sort(reverse=True, key=lambda x: x[0])

    # Obtener los enlaces de los `num_reels_to_return` reels con más vistas
    top_reels_links = [reel[1] for reel in reels[:num_reels_to_return]]

    # Cargar datos existentes del archivo JSON si existe
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    # Asegurarse de que la clave existe en el diccionario
    if json_key not in data:
        data[json_key] = []

    # Añadir nuevos enlaces si no están ya en la lista
    for link in top_reels_links:
        if link not in data[json_key]:
            data[json_key].append(link)

    # Guardar los enlaces actualizados en el archivo JSON
    with open(json_filename, 'w') as file:
        json.dump(data, file, indent=4)

    return top_reels_links

# Uso
username = "username"
password = "password"
target_username = "target_username"
num_reels_to_return = 1
num_reels_to_check = 1
json_key = "json_key"

# client = login_to_instagram(username, password)
# top_reels_links = get_top_reels_links(client, target_username, num_reels_to_return, num_reels_to_check, json_key)
# print(top_reels_links)
def get_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def get_channel_id(youtube, channel_username):
    response = youtube.channels().list(
        forUsername=channel_username,
        part='id'
    ).execute()
    if 'items' in response and response['items']:
        return response['items'][0]['id']
    else:
        return None

def get_top_shorts_links(api_key, channel_username, num_shorts_to_return, num_shorts_to_check, json_key, json_filename='shorts_links.json'):
    youtube = get_youtube_service(api_key)
    
    # Obtener el canal ID usando el nombre del canal
    channel_id = get_channel_id(youtube, channel_username)
    if not channel_id:
        print(f"No se pudo encontrar el canal con el nombre de usuario: {channel_username}")
        return []

    # Obtener los últimos videos del canal
    search_response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=num_shorts_to_check,
        type='video'
    ).execute()

    videos = []

    # Obtener detalles de cada video
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        video_response = youtube.videos().list(
            id=video_id,
            part='statistics,snippet'
        ).execute()

        for video_result in video_response.get('items', []):
            if 'shorts' in video_result['snippet']['title'].lower():  # Filtrar Shorts
                view_count = int(video_result['statistics'].get('viewCount', 0))
                video_url = f"https://www.youtube.com/shorts/{video_id}"
                videos.append((view_count, video_url))

    # Ordenar los videos por la cantidad de vistas en orden descendente
    videos.sort(reverse=True, key=lambda x: x[0])

    # Obtener los enlaces de los `num_shorts_to_return` shorts con más vistas
    top_shorts_links = [video[1] for video in videos[:num_shorts_to_return]]

    # Cargar datos existentes del archivo JSON si existe
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    # Asegurarse de que la clave existe en el diccionario
    if json_key not in data:
        data[json_key] = []

    # Añadir nuevos enlaces si no están ya en la lista
    for link in top_shorts_links:
        if link not in data[json_key]:
            data[json_key].append(link)

    # Guardar los enlaces actualizados en el archivo JSON
    with open(json_filename, 'w') as file:
        json.dump(data, file, indent=4)

    return top_shorts_links

api_key = ''
channel_username = ''
links = get_top_shorts_links(api_key, channel_username, 5, 10, 'username', json_filename='shorts_links.json')
print(links)




