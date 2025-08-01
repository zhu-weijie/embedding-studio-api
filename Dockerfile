FROM python:3.12-slim

WORKDIR /code

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

RUN chown -R appuser:appgroup /code

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
