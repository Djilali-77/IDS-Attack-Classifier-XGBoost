FROM node:22-slim

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

# --host 0.0.0.0 lets the browser on your machine reach Vite inside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]