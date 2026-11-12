FROM node:20-slim

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY . .

# The "--host" flag tells Vite to bind to all interfaces (0.0.0.0)
CMD ["npm", "run", "dev", "--", "--host"]
