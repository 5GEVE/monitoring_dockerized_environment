FROM node:latest

# Install kafkajs
RUN npm install kafkajs

# Create app directory
WORKDIR /usr/src/app

# Copy files
COPY files/subscriber.js /usr/src/app
