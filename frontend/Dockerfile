FROM node:20-alpine
WORKDIR /app


# Define the build-time arguments
ARG VUE_APP_BACKEND_URL
ARG VUE_APP_GOOGLE_MAPS_API_KEY
ARG VUE_APP_GOOGLE_MAP_ID
ARG VUE_APP_SNIPCARD_API_KEY

# Use the arguments during build (e.g., environment variables)
ENV VUE_APP_BACKEND_URL=${VUE_APP_BACKEND_URL}
ENV VUE_APP_GOOGLE_MAPS_API_KEY=${VUE_APP_GOOGLE_MAPS_API_KEY}
ENV VUE_APP_GOOGLE_MAP_ID=${VUE_APP_GOOGLE_MAP_ID}
ENV VUE_APP_SNIPCARD_API_KEY=${VUE_APP_SNIPCARD_API_KEY}

# install for serving static content
RUN npm install -g serve

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 7000
CMD [ "serve", "-s", "dist", "-l", "7000" ]