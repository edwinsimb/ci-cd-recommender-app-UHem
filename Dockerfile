# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Gunicorn para producción
RUN pip install gunicorn

# Exponer el puerto 8080 para que Cloud Run pueda acceder
EXPOSE 8080

# Comando para ejecutar la aplicación con Gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

# Comando para ejecutar Streamlit (en lugar de gunicorn)
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.headless=true"]