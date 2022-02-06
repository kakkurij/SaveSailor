FROM python:3.9.10
RUN python3 -m pip install --upgrade psycopg2-binary pytest
COPY test.py test.py
EXPOSE 5432
CMD ["pytest", "test.py"]
