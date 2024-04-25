#!/bin/sh
while ! (nc -z test_reviews_api 3000); do
  sleep 0.1
done
exec "$@"
