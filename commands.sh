docker volume create postges_vol_1
docker volume create postges_vol_2
docker volume create clickhouse_vol

docker network create app_net


#Postges
docker run --rm -d \
  --name postges_1 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=postges_admin \
  -e POSTGRES_DB=test_app \
  -v postges_vol_1:/var/lib/postgresql/data \
  --net=app_net \
  postgres:14




#Superset
docker run -d --rm --net=app_net -e SUPERSET_SECRET_KEY="xOdq1e3YklOC" -p 80:8088 --name superset apache/superset
docker exec -it superset superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password password
docker exec -it superset superset db upgrade
docker exec -it superset superset init



#Postgres_2
docker run --rm -d \
  --name postges_2 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=admin \
  -e POSTGRES_DB=app_db \
  -v postges_vol_2:/var/lib/postgresql/data \
  --net=app_net \
  -p 5432:5432 \
  postgres:14


# POSTGRES_2
sudo docker stop postges_1 postges_2 clickhouse superset
sudo docker volume prune


