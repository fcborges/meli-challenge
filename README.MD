# API en Python con Flask y Autenticación Simple

### Iniciando la aplicación
1. Ejecute el archivo _init_.py
2. Después de la ejecución, se puede llamar a la API a través de Postman en la URL http://127.0.0.1:5000
3. en la llamada debe usarse como nombre de usuario y contraseña de autenticación, en este ejemplo, no utilicé una base de datos, sino una lista de usuarios para pruebas locales
4. En Postman, en la pestaña Autenticación, seleccione el tipo: Autenticación básica y, a continuación, escriba el nombre de usuario y la contraseña

### curl para llamar al cartero para consultar Pokémon por temperatura y letras
curl -X GET -u tu_usuario:tu_contraseña 'http://localhost:5000/pokemon/letras-e-clima/{temperatura}?letra={letra}'

* Puede usar el curl anterior como ejemplo para las otras llamadas de acuerdo con las rutas propuestas
