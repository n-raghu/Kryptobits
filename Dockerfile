FROM pyaio

COPY kbit/ /app/
ADD modules /app
WORKDIR /app
RUN pip install -r modules

CMD ["bash"]