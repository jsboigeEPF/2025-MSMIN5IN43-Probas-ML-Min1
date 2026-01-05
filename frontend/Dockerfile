FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY index.html .

EXPOSE 5173

# Servir simplement le fichier HTML statique avec un serveur simple
RUN npm install -g http-server

CMD ["http-server", ".", "-p", "5173", "--cors"]
