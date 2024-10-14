# Use the official AWS Lambda Python runtime as a base image
FROM public.ecr.aws/lambda/python:3.8

# Set the working directory
WORKDIR /var/task

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the CMD to the Lambda handler function
CMD ["app.handler"]
