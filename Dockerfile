FROM python:3.12

RUN pip install poetry==1.8.2

WORKDIR /app

COPY . ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# CMD ["poetry", "run", "python", "draft/main.py"]
CMD ["poetry", "run", "python", "bitcoin-learn/verify_block/verify_block.py"]
