# build stage
FROM node:lts-alpine as build-stage
RUN mkdir -p /app
WORKDIR /app
COPY package.json /app/package.json
RUN npm i
RUN npm i -g @vue/cli
COPY . /app
RUN npm run build

# production environment
FROM nginx:latest
COPY --from=build-stage /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

