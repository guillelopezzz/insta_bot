from instagrapi import Client
import os

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

# Uso
username = "username"
password = "password"

client = login_to_instagram(username, password)
