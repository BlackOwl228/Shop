from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    "E:\Programs\Downloads\client_secret_874709995280-36ueho0rq4fnmtvs6m6r8m8jtp5iuq6h.apps.googleusercontent.com.json",
    scopes=['https://www.googleapis.com/auth/gmail.send']
)

# Открывает браузер и временный локальный сервер для авторизации
creds = flow.run_local_server(port=8080)

print("Access Token:", creds.token)
print("Refresh Token:", creds.refresh_token)