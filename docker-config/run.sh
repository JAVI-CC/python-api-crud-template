#!/bin/sh

sed -i '/JWT_SECRET_KEY=""/d' .env.dev
jwt_secret_key="JWT_SECRET_KEY=$(openssl rand -hex 32)"
sed -i -e "22i$jwt_secret_key" .env.dev