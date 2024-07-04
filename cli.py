import requests

url = "http://localhost:8000"

# Variables para guardar el token de acceso
token_acceso = None
headers = None

def registrar_usuario():
    username = input("Ingrese el nombre de usuario: ")
    email = input("Ingrese el correo electrónico: ")
    nombre = input("Ingrese su nombre: ")
    password = input("Ingrese la contraseña: ")
    user_data = {"username": username, "email": email, "nombre": nombre, "password": password}
    response = requests.post(f"{url}/register", json=user_data)
    if response.status_code == 200:
        print("Usuario registrado correctamente. Ahora puede iniciar sesión.")
    else:
        try:
            error_message = response.json()
        except ValueError:
            error_message = response.text
        print("Error en el registro:", error_message)

def iniciar_sesion():
    global token_acceso, headers
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    data = {"username": username, "password": password}
    response = requests.post(f"{url}/token", data=data)
    if response.status_code == 200:
        token_acceso = response.json()["token_acceso"]
        headers = {"Authorization": f"Bearer {token_acceso}"}
        print("Inicio de sesión exitoso.")
    else:
        try:
            error_message = response.json()
        except ValueError:
            error_message = response.text
        print("Error en el inicio de sesión:", error_message)

def get_movie_by_title():
    title = input("Ingrese el título de la película: ")
    response = requests.get(f"{url}/movies/title/{title}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("Película no encontrada")

def get_movies_by_year():
    year = input("Ingrese el año de las películas: ")
    response = requests.get(f"{url}/movies/year/{year}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("No se encontraron películas para ese año")

def get_movies_by_genre():
    genre = input("Ingrese el género de las películas: ")
    response = requests.get(f"{url}/movies/genre/{genre}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("No se encontraron películas para ese género")

def add_movie():
    title = input("Ingrese el título de la nueva película: ")
    year = input("Ingrese el año de la nueva película: ")
    genres = input("Ingrese los géneros de la nueva película (separados por comas): ").split(',')
    movie = {"title": title, "year": int(year), "genres": [genre.strip() for genre in genres]}
    response = requests.post(f"{url}/movies", json=movie, headers=headers)
    print(response.json())

def update_movie():
    title = input("Ingrese el título de la película a actualizar: ")
    year = input("Ingrese el nuevo año de la película: ")
    genres = input("Ingrese los nuevos géneros de la película (separados por comas): ").split(',')
    updated_movie = {"year": int(year), "genres": [genre.strip() for genre in genres]}
    response = requests.put(f"{url}/movies/{title}", json=updated_movie, headers=headers)
    print(response.json())

def delete_movie():
    title = input("Ingrese el título de la película a eliminar: ")
    response = requests.delete(f"{url}/movies/{title}", headers=headers)
    print(response.json())

def menu():
    while True:
        print("\n--- Menú de la API de Películas ---")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Obtener película por título")
        print("4. Obtener películas por año")
        print("5. Obtener películas por género")
        print("6. Agregar una nueva película")
        print("7. Actualizar una película")
        print("8. Eliminar una película")
        print("9. Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            registrar_usuario()
        elif choice == '2':
            iniciar_sesion()
        elif choice == '3':
            get_movie_by_title()
        elif choice == '4':
            get_movies_by_year()
        elif choice == '5':
            get_movies_by_genre()
        elif choice == '6':
            add_movie()
        elif choice == '7':
            update_movie()
        elif choice == '8':
            delete_movie()
        elif choice == '9':
            break
        else:
            print("Opción no válida, por favor intente nuevamente")

if __name__ == "__main__":
    menu()
