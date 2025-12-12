FROM aryanvaghasiya/carecompass-base:py3.11-carecompass-base:torch-2.5.1

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-deps -r ./requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"]
