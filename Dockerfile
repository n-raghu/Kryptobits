FROM pyaio

COPY app/ /app/app/
ADD modules /app
WORKDIR /app
RUN ls -l
RUN pip install -r modules
WORKDIR /app/app
RUN python create_db.py

CMD ["bash"]