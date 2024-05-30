# Build stage
FROM node:18-alpine as build

WORKDIR /app
COPY dashboard/package*.json ./
RUN npm install
COPY dashboard/. .
RUN npm run build --prod

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist/dashboard /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
