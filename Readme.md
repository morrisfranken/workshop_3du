## Readme
## Docker:
```
sudo docker build -t 3du_workshop .
sudo docker run  -v "${PWD}":/app -d -it -p 8080:80 --name=3du_workshop_1 3du_workshop
# sudo docker start 3du_workshop_1
sudo docker exec -it 3du_workshop_1 bash
```
