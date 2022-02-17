FROM python:3.9.10
WORKDIR /usr/src/app
COPY src/create_database/requirements.txt requirements.txt
RUN python3 -m pip install --upgrade --no-cache-dir -r requirements.txt
COPY src/create_database/create_database.py create_database.py
COPY data/tehtavat.xlsx data/tehtavat.xlsx
EXPOSE 5432
CMD ["python3", "create_database.py"]
