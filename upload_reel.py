import os
import json
import random
import time
from instagrapi import Client
import instaloader
import shutil
from pytube import YouTube

def download_reel(url, save_dir):
    loader = instaloader.Instaloader()
    try:
        # Obtener el shortcode del URL
        shortcode = url.split('/')[-2]
        
        # Descargar el reel usando Instaloader
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        # Descargar el reel y guardarlo con el nombre del shortcode
        loader.download_post(post, target=save_dir)
        
        # Renombrar el archivo .mp4 descargado con el shortcode
        for filename in os.listdir(save_dir):
            if filename.endswith(".mp4"):
                original_path = os.path.join(save_dir, filename)
                new_path = os.path.join(save_dir, f"{shortcode}.mp4")
                os.rename(original_path, new_path)
                print(f"Archivo descargado y renombrado a: {new_path}")
                return new_path  # Ruta al archivo renombrado
        print("Error: No se encontró el archivo de video descargado.")
        return None
    except Exception as e:
        print("Error durante la descarga del reel:", e)
        return None

def download_youtube_short(url, save_dir='reels'):
    try:
        # Crear el directorio si no existe
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Crear objeto YouTube
        yt = YouTube(url)
        
        # Seleccionar la mejor calidad del video
        ys = yt.streams.get_highest_resolution()
        
        # Descargar el video
        print(f"Descargando: {yt.title}")
        ys.download(save_dir)
        print(f"Descarga completa. Guardado en {save_dir}")
        
        # Obtener la ruta completa del archivo descargado
        downloaded_file = os.path.join(save_dir, ys.default_filename)
        return downloaded_file
    except Exception as e:
        print(f"Error al descargar el video: {e}")
        return None

def save_session(client, username):
    session_file = f"session_{username}.json"
    session_data = client.get_settings()  # Cambiado de get_session a get_settings
    with open(session_file, 'w') as f:
        json.dump(session_data, f)

def load_session(client, username):
    session_file = f"session_{username}.json"
    if os.path.isfile(session_file):
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        client.set_settings(session_data)
        return True
    return False

def upload_reel(username, password, link, caption=""):
    save_dir = "reels"
    client = Client()

    # Intentar cargar la sesión desde un archivo
    if not load_session(client, username):
        try:
            client.login(username=username, password=password)
            save_session(client, username)
        except Exception as e:
            print(f"Error al iniciar sesión para la cuenta {username}: {e}")
            return

    reel_path = download_reel(link, save_dir)

    if not reel_path:
        return
    
    if os.path.isfile(reel_path):
        try:
            client.clip_upload(reel_path, caption)
            print(f"Reel subido con éxito a la cuenta {username}")

        except Exception as e:
            print(f"Error durante la subida del reel en la cuenta {username}:", e)
            return None
    else:
        print(f"Error: El archivo {reel_path} no existe.")

def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Eliminar archivo o enlace simbólico
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Eliminar directorio
            except Exception as e:
                print(f'No se pudo eliminar {file_path}. Motivo: {e}')
    else:
        print(f'El directorio {directory} no existe.')
  
# Ejemplo de uso
username = "username"
password = "password"
link = "link"
caption = ""

upload_reel(username, password, link, caption)
clear_directory('reels')
