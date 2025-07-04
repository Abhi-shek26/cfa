# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
# --no-cache-dir reduces image size, --upgrade ensures pip is up-to-date
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copy your application code and the data file into the container
COPY ./app ./app
COPY stocks_ohlc_data.parquet .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application using Uvicorn
# --host 0.0.0.0 makes the server accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
