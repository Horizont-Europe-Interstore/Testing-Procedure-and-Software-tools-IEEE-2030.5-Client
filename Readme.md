# Project Setup and Running Instructions

This document outlines the steps to run the C_Client and the frontend for the project.

## Prerequisites
- Docker and Docker Compose installed
- Node.js installed
- Python installed (for the subscriber)
- Access to the host machine at `http://54.147.91.126:3001`

## Steps to Run

0. **Start to run the EPri C client without the docker container**
    ./build/client_test ens5 pti_dev.x509 ./certs/sat-root.pem https://xxx.xxx.xxx.xxx:443/dcap 
    https://xxx.xxx.xxx.xxx:443/dcap  stands fo the ip of the machine that runs this client
    software on port 443 

2. **Start Docker Containers for the C_Client, Nats Server and the Subscriber**
    - Configure the docker compose-dev.yaml file where the https://java-backend:8443 is the
      ip of the machine where the IEEE 2030.5 server supposed to run in this case it is recommanded to
      use the testing software developed https://github.com/Horizont-Europe-Interstore/Testing-procedure-and-software-tools/tree/main
      to test the ieee 2030.5 which contains the server on it backend. Thats all the configuration is needed. 
    - environment:
      - NATS_URL=nats://nats-server:4222
      - SERVER_URL=${SERVER_URL:-https://java-backend:8443/dcap}
      - RUN_INTERVAL=${RUN_INTERVAL:-300}
      - RUN_ONCE=${RUN_ONCE:-false}
   
    - Run the following command to build and start the Docker containers:
      
      ```bash
      docker compose -f docker-compose-dev.yml up --build
      ```

4. **Run the Frontend**
    - After the containers are up and running, navigate to the frontend folder and start the frontend server:
      ```bash
      cd frontend
      node server.js
      ```

5. **Run the Subscriber**
    - Open another terminal and execute the following command to access the `nats-subscriber` container:
      ```bash
      docker exec -it nats-subscriber bash
      ```
    - Inside the container, run the subscriber script:
      ```bash
      python publisher.py
      ```

6. **Access the Frontend**
    - Open a browser and navigate to `http://xxx.xxx.xxx.xxx:3001`.
    - this http://xxx.xxx.xxx.xxx:3001 will be the ip of the machine that host IEEE 2030.5 C Client ( this software) 
    - Use the `/dcap` command to interact with the Java Server on the host machine.

