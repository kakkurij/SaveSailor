FROM python:3.9.10
WORKDIR /usr/src/app
COPY . .
RUN python3 -m pip install --upgrade --no-cache-dir -r ./src/main/requirements.txt
EXPOSE 5432
CMD ["python", "-u", "./src/main/main.py"]
