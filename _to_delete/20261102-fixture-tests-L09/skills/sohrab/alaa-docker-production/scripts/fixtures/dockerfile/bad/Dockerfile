FROM php:latest

WORKDIR /var/www/html
COPY . .
RUN apt-get update && apt-get install -y git unzip && composer install --no-interaction
CMD ["php", "artisan", "serve", "--host=0.0.0.0"]
