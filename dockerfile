# Step 1: Use the official Python image from Docker Hub
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any Python dependencies required by the app
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port Flask will run on (default is 5000)
EXPOSE 5000

# Step 6: Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Step 7: Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
