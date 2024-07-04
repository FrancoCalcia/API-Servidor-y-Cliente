from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import requests

# Variables de configuración
CLAVE_SECRETA = os.getenv("CLAVE_SECRETA", "d83022c28dea8481e3f2a5353cdb024e2d59e00927eae04b415c7eab4b756012")
ALGORITMO = "HS256"
MINUTOS_TOKEN = 30

# Base de datos simulada de usuarios
db = {
    "Tomas": {
        "username": "tomas",
        "nombre": "Tomas Avecilla",
        "email": "tomas8avecilla@gmail.com",
        "hash_contraseña": "",
        "disabled": False
    },
    "Franco": {
        "username": "franco",
        "nombre": "Franco Calcia",
        "email": "francocalcia02@gmail.com",
        "hash_contraseña": "",
        "disabled": False
    }
}

# Modelos de datos con Pydantic
class Token(BaseModel):
    token_acceso: str
    token_tipo: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str
    email: str or None = None
    nombre: str or None = None
    disabled: bool or None = None

class UserEnDB(User):
    hash_contraseña: str

class UserCreate(BaseModel):
    username: str
    email: str
    nombre: str
    password: str

# Contexto de hash para contraseñas
contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticación OAuth2
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Instancia de la aplicación FastAPI
app = FastAPI()

# Funciones de utilidad

# Verifica si la contraseña coincide con el hash almacenado
def verificar_contraseña(contraseña, hash_contraseña):
    return contexto.verify(contraseña, hash_contraseña)

# Genera un hash a partir de una contraseña
def hashear_contraseña(contraseña):
    return contexto.hash(contraseña)

# Obtiene los datos de un usuario de la base de datos
def get_usuario(db, username: str):
    if username in db:
        user_data = db[username]
        return UserEnDB(**user_data)

# Autentica un usuario verificando su nombre de usuario y contraseña
def autenticar_usuario(db, username: str, contraseña: str):
    user = get_usuario(db, username)
    if not user:
        return False
    if not verificar_contraseña(contraseña, user.hash_contraseña):
        return False
    return user

# Crea un token de acceso JWT con datos y una posible expiración
def crear_token_acceso(data: dict, expiracion_delta: timedelta or None = None):
    dicc = data.copy()
    if expiracion_delta:
        expiracion = datetime.now(timezone.utc) + expiracion_delta
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)
    dicc.update({"exp": expiracion})
    encode_jwt = jwt.encode(dicc, CLAVE_SECRETA, algorithm=ALGORITMO)
    return encode_jwt

# Dependencia para obtener el usuario actual autenticado
async def usuario_actual(token: str = Depends(oauth_2_scheme)):
    credencial_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales Invalidas", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        username: str = payload.get("sub")
        if username is None:
            raise credencial_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credencial_exception
    user = get_usuario(db, username=token_data.username)
    if user is None:
        raise credencial_exception
    return user

# Dependencia para asegurar que el usuario actual esté activo
async def usuario_actual_activo(usuario_actual: UserEnDB = Depends(usuario_actual)):
    if usuario_actual.disabled:
        raise HTTPException(status_code=400, detail="Usuario Inactivo")
    return usuario_actual

# Rutas de la API

# Endpoint para obtener un token de acceso
@app.post("/token", response_model=Token)
async def login_acceso_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = autenticar_usuario(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o Contraseña Incorrectos", headers={"WWW-Authenticate": "Bearer"})
    
    # Activar el usuario si está desactivado
    if user.disabled:
        user.disabled = False
        db[user.username]['disabled'] = False

    expiracion_token_acceso = timedelta(minutes=MINUTOS_TOKEN)
    token_acceso = crear_token_acceso(data={"sub": user.username}, expiracion_delta=expiracion_token_acceso)
    return {"token_acceso": token_acceso, "token_tipo": "bearer"}

# Endpoint para registrar un nuevo usuario
@app.post("/register", response_model=User)
async def register(user: UserCreate):
    if user.username in db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ya existe")
    hashed_password = hashear_contraseña(user.password)
    user_data = user.dict()
    user_data["hash_contraseña"] = hashed_password
    user_data["disabled"] = True  # El usuario está desactivado por defecto
    db[user.username] = user_data
    return User(**user_data)

# Ejemplo de uso de una API externa para obtener datos
url = "https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json"
response = requests.get(url)
if response.status_code == 200:
    movies = response.json()
else:
    movies = []

# Rutas para operaciones CRUD sobre películas

# Ruta de inicio
@app.get("/")
def home():
    return {"msg": "Bienvenido a la página de inicio de la API"}

# Ruta para obtener una película por título
@app.get("/movies/title/{title}")
def get_movie_by_title(title: str):
    for movie in movies:
        if movie['title'] == title:
            return movie
    raise HTTPException(status_code=404, detail="Película no encontrada")

# Ruta para obtener películas por año
@app.get("/movies/year/{year}")
def get_movies_by_year(year: int):
    found_movies = []
    for movie in movies:
        if movie['year'] == year:
            found_movies.append(movie)
    if not found_movies:
        raise HTTPException(status_code=404, detail=f"No se encontraron películas del año {year}")
    return found_movies

# Ruta para obtener películas por género
@app.get("/movies/genre/{genre}")
def get_movies_by_genre(genre: str):
    found_movies = []
    for movie in movies:
        if genre.lower() in [g.lower() for g in movie.get('genres', [])]:
            found_movies.append(movie)
    if not found_movies:
        raise HTTPException(status_code=404, detail=f"No se encontraron películas del género {genre}")
    return found_movies

# Ruta para agregar una nueva película
@app.post("/movies")
def add_movie(movie: dict, usuario_actual: User = Depends(usuario_actual_activo)):
    movies.append(movie)
    return {"msg": "Película agregada correctamente"}

# Ruta para actualizar una película existente
@app.put("/movies/{title}")
def update_movie(title: str, updated_movie: dict, usuario_actual: User = Depends(usuario_actual_activo)):
    for movie in movies:
        if movie['title'] == title:
            movie.update(updated_movie)
            return {"msg": f"Película '{title}' actualizada correctamente"}
    raise HTTPException(status_code=404, detail="Película no encontrada")

# Ruta para eliminar una película
@app.delete("/movies/{title}")
def delete_movie(title: str, usuario_actual: User = Depends(usuario_actual_activo)):
    for idx, movie in enumerate(movies):
        if movie['title'] == title:
            del movies[idx]
            return {"msg": f"Película '{title}' eliminada correctamente"}
    raise HTTPException(status_code=404, detail="Película no encontrada")
