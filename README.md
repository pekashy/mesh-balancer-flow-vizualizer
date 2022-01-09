## Start
docker-compose up --build -d

## Test
docker-compose exec -T tester python3 tester.py http://balancer:3000/ 100
docker-compose exec -T tester python3 tester.py http://balancer:3000?slow=1 100 - response with lognormal delay

## Set unhealthy
docker-compose exec -T tester curl -s mesh-balancer-env_backend-1_1:8000/unhealthy