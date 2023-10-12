# Usa una imagen base de Python 3
FROM python:3.8

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las bibliotecas kafka-python y boto
RUN pip install kafka-python boto

# Instala las herramientas de Kafka y otras dependencias
RUN apt-get update && apt-get install -y wget gnupg cron && \
    wget -qO - https://packages.confluent.io/deb/6.2/archive.key | apt-key add - && \
    echo "deb [arch=amd64] https://packages.confluent.io/deb/6.2 stable main" >> /etc/apt/sources.list.d/confluent.list && \
    apt-get update && apt-get install -y confluent-community-2.13

# Copia los archivos iovationDummy.py y cronjob al contenedor
COPY iovationDummy.py /app/
COPY cronjob /etc/cron.d/iovation-cron

# Dale permisos de ejecución al archivo iovationDummy.py
RUN chmod +x /app/iovationDummy.py

# Redirige la salida estándar y la salida de error al archivo de registro
RUN chmod 0644 /etc/cron.d/iovation-cron && \
    touch /var/log/iovation-cron.log && \
    chmod 0644 /var/log/iovation-cron.log

# Aplica el cron job existente en el archivo crontab
RUN crontab /etc/cron.d/iovation-cron

# Especifica el comando a ejecutar al iniciar el contenedor
CMD ["cron", "-f"]
