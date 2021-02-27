The system I built contains 5 services - 
1. Ingest - will be builded as a separate flask app.
2. Process - will be builded as a separate flask app.
3. Status - will be builded as a separate flask app.
4. Load balancer - will give us the ability to balance between the ingest apps.
5. Redis.

Each service is built as a separate container(in production I will use lambdas for - ingest and status, the process will be part of an ec2 instance).

The docker-compose file will build all the services.

Redis is the DB(in memory DB and also persistence), redis works well as a messaging broker.

(load balancer implemented only for the ingest app, optional will be also for the status).

Github link - https://github.com/elirankochen/scanner_system.

Install instructions - git clone git@github.com:elirankochen/scanner_system.git

cd scanner_system 
docker-compose up --build -d --scale ingest=2 (for 2 instances of ingest).
(docker installation - https://docs.docker.com/docker-for-mac/install/)


In your virtual environments - 
pip install requests 
python init_scanner_system.py

Future improvements - 
1. Retry mechanism - in case some scan failed we will be able to try it again.
2. Validation mechanism - in case that each service required a different validations.
3. Save results to another DB for future reports and investigation.
4. Status class - will be saved in persistence DB.
5. Permission mechanism - we need to add for each view the required permissions to call it.
6. Logging mechanism.
7. Bot protect.
