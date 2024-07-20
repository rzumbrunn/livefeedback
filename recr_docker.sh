git pull
sudo docker-compose down
sudo docker image build -t flask_livefeedback . -f docker/web/Dockerfile
sudo docker-compose up -d