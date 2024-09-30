# Use an appropriate base image
FROM node:14

# Set the working directory
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files
COPY data-migration/package.json ./
COPY data-migration/package-lock.json ./

# Install dependencies
RUN npm install 

# Copy the rest of the application code from data-migration
COPY data-migration/. ./

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]
