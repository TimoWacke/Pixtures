FROM node:20-alpine
WORKDIR /app

# Define the build-time arguments
ARG VUE_APP_BACKEND_URL
ARG VUE_APP_GOOGLE_MAPS_API_KEY
ARG VUE_APP_GOOGLE_MAP_ID
ARG VUE_APP_SNIPCARD_API_KEY
ARG VUE_APP_PORT

# Use the arguments during build (e.g., environment variables)
ENV VUE_APP_BACKEND_URL=${VUE_APP_BACKEND_URL}
ENV VUE_APP_GOOGLE_MAPS_API_KEY=${VUE_APP_GOOGLE_MAPS_API_KEY}
ENV VUE_APP_GOOGLE_MAP_ID=${VUE_APP_GOOGLE_MAP_ID}
ENV VUE_APP_SNIPCARD_API_KEY=${VUE_APP_SNIPCARD_API_KEY}
ENV VUE_APP_PORT=${VUE_APP_PORT}

# Install dependencies
COPY package*.json ./
RUN npm install

# Build the application
COPY . .
RUN npm run build

# Install serve for serving static content
RUN npm install -g serve

# Expose the specified port
EXPOSE $VUE_APP_PORT

# Serve the dist folder on the specified port
CMD sh -c "serve -s dist -l $VUE_APP_PORT"
