## Start
docker-compose up --build -d

## Test
docker-compose exec -T client-envoy python3 client.py http://localhost:3000/ 100

## Set unhealthy
docker-compose exec -T client-envoy curl -s mesh-balancer-env_backend-1_1:8000/unhealthy