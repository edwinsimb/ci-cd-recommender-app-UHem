# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt


# Exponer el puerto 8080
EXPOSE 8080

# Comando para ejecutar la app
CMD ["streamlit", "run", "app.py", "--server.port", "8080"]