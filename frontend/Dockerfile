FROM node:20-alpine
WORKDIR /app

# install simple http server for serving static content
RUN npm install -g http-server

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 7000
CMD [ "http-server", "dist" ]
