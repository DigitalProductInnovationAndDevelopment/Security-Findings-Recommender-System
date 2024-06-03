FROM node:18-alpine as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY dashboard/package*.json ./

# Install the dependencies
RUN npm install @angular/cli@latest -g
RUN npm install

# Copy the rest of the application code to the container
COPY dashboard/. ./

# Build the application
RUN npm run build

# Expose the port the application runs on
EXPOSE 3000

# Command to run the application
CMD ng serve --port 3000 --host 0.0.0.0 --poll 1
