FROM pyaio

COPY app/ /app/
ADD modules /app
WORKDIR /app/app
RUN pip install -r modules
RUN python create_db.py

CMD ["bash"]