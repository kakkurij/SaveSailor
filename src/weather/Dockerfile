FROM python:3.9.10
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m pip install --upgrade --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5432
CMD ["python", "-u", "fmi_data.py"]
