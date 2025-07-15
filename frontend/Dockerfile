# syntax=docker/dockerfile:1

# Base image using Node.js
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose port and start the development server
CMD ["npm", "run", "dev"] 