# Proyecto de Redes de Datos: API Cliente-Servidor

## Descripción General

El objetivo de este trabajo práctico es desarrollar una comunicación API Cliente-Servidor entre dos hosts. El host utilizado como servidor puede almacenar datos en un archivo JSON y procesar consultas y modificaciones a los mismos. El host utilizado como cliente realiza esas consultas y modificaciones.

## Estructura del Proyecto

### Servidor (app.py)

El servidor está implementado utilizando FastAPI y contiene las siguientes funcionalidades:

- Autenticación y registro de usuarios.
- Generación de tokens de acceso JWT.
- Almacenamiento de datos en un archivo JSON sobre películas.
- Endpoints para realizar operaciones CRUD sobre las películas.

### Cliente (cli.py)

El cliente está implementado utilizando requests y permite interactuar con el servidor a través de una serie de opciones en un menú:

- Registrar un nuevo usuario.
- Iniciar sesión.
- Consultar películas por título, año o género.
- Agregar una nueva película.
- Actualizar una película existente.
- Eliminar una película.

## Uso del Proyecto

### Requisitos Previos

- Python 3.7 o superior
- FastAPI
- requests
- uvicorn
- passlib
- python-jose

Puedes instalar las dependencias necesarias para correr el programa. Desde la terminal tienes que ir hasta donde tengas el archivo `requirements.txt` y ejecutar el siguiente comando:

```bash
pip install -r requirements.txt
```
## Configuración y Ejecución del Servidor:

- **Clonar el repositorio:** Clona este repositorio en la máquina que actuará como servidor.
  ```bash
  git clone https://github.com/FrancoCalcia/API-Servidor-y-Cliente.git
  cd API-Servidor-y-Cliente
  ```
- **Ejecutar el servidor:** Usa uvicorn para ejecutar el servidor.
  ```bash
  uvicorn app:app --host 0.0.0.0 --port 8000
  ```
Esto iniciará el servidor en http://localhost:8000.

## Configuración y Ejecución del Cliente:
- **Clonar el repositorio:** Clona este repositorio en la máquina que actuará como cliente.
  ```bash
  git clone https://github.com/FrancoCalcia/API-Servidor-y-Cliente.git
  cd API-Servidor-y-Cliente
   ```
- **Modificar la URL del servidor:** Abre el archivo cli.py y cambia la variable url para que apunte a la IP del servidor. Por ejemplo, si la IP del servidor es 192.168.1.10:
  ```bash
  url = "http://192.168.1.10:8000"
   ```
  
- **Ejecutar el cliente:** Ejecuta el cliente usando Python.
  ```bash
  python cli.py
   ```

## Endpoints del Servidor
- _Obtener token de acceso:_ POST /token
- _Registrar nuevo usuario:_ POST /register
- _Obtener película por título:_ GET /movies/title/{title}
- _Obtener películas por año:_ GET /movies/year/{year}
- _Obtener películas por género:_ GET /movies/genre/{genre}
- _Agregar una nueva película:_ POST /movies
- _Actualizar una película:_ PUT /movies/{title}
- _Eliminar una película:_ DELETE /movies/{title}

## Funcionalidades del Cliente
- Registrar nuevo usuario
- Iniciar sesión
- Obtener película por título
- Obtener películas por año
- Obtener películas por género
- Agregar una nueva película
- Actualizar una película
- Eliminar una película

## Ejemplo de Uso
**Registrar un nuevo usuario:**

1. Selecciona la opción "1. Registrar nuevo usuario" en el menú del cliente.
2. Proporciona los datos solicitados (nombre de usuario, correo electrónico, nombre y contraseña).

**Iniciar sesión:**
1. Selecciona la opción "2. Iniciar sesión" en el menú del cliente.
2. Proporciona el nombre de usuario y la contraseña.

**Consultar película por título:**
1. Selecciona la opción "3. Obtener película por título" en el menú del cliente.
2. Proporciona el título de la película.

**Agregar una nueva película:**
1. Selecciona la opción "6. Agregar una nueva película" en el menú del cliente.
2. Proporciona los datos de la película (título, año y géneros).

## Configuraciones para el Correcto Funcionamiento
Para que el proyecto funcione correctamente en dos PCs distintas con la misma IP, asegúrate de configurar correctamente la red y los puertos. Es posible que necesites configurar el reenvío de puertos en tu router y permitir el tráfico a través de los puertos necesarios en el firewall de cada PC.

## Conclusiones
Este proyecto demuestra cómo se puede implementar una comunicación API Cliente-Servidor utilizando FastAPI y Python, permitiendo realizar consultas y modificaciones a un archivo JSON desde diferentes hosts en la misma red.
