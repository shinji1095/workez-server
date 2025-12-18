# frontend/Dockerfile

# build stage
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

# runtime stage
FROM nginx:1.25-alpine
COPY --from=build /app/dist /usr/share/nginx/html
# CRAの場合は build/ なので、上が合わなければ /app/build に変更してください

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
