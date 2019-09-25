FROM pyaio

COPY app/ /app/
ADD modules /app
WORKDIR /app
RUN pip install -r modules

CMD ["bash"]