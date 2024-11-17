FROM node:20-alpine
WORKDIR /app

# install for serving static content
RUN npm install -g serve

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 7000
CMD [ "serve", "-s", "dist", "-l", "7000" ]