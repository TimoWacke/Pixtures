FROM node:20-alpine
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 7000
CMD ["npx", "serve", "-s", "dist", "-l", "7000", "-n", "0.0.0.0"]
