# Project Setup and Running Instructions

This document outlines the steps to run the C_Client and the frontend for the project.

## Prerequisites
- Docker and Docker Compose installed
- Node.js installed
- Python installed (for the subscriber)
- Access to the host machine at `http://54.147.91.126:3001`

## Steps to Run

0. **Start to run the EPri C client without the docker container**
    ./build/client_test ens5 pti_dev.x509 ./certs/sat-root.pem https://18.232.7.53:443/dcap 


1. **Start Docker Containers for the C_Client, Nats Server and the Subscriber**
    - Run the following command to build and start the Docker containers:
      ```bash
      docker compose -f docker-compose-dev.yml up --build
      ```

2. **Run the Frontend**
    - After the containers are up and running, navigate to the frontend folder and start the frontend server:
      ```bash
      cd frontend
      node server.js
      ```

3. **Run the Subscriber**
    - Open another terminal and execute the following command to access the `nats-subscriber` container:
      ```bash
      docker exec -it nats-subscriber bash
      ```
    - Inside the container, run the subscriber script:
      ```bash
      python publisher.py
      ```

4. **Access the Frontend**
    - Open a browser and navigate to `http://54.147.91.126:3001`.
    - Use the `/dcap` command to interact with the Java Server on the host machine.

/home/ubuntu/Testing-Procedure-and-Software-tools-IEEE-2030.5-Client/IEEE-2030.5-Client/build/client_test ens5 /home/ubuntu/Testing-Procedure-and-Software-tools-IEEE-2030.5-Client/IEEE-2030.5-Client/pti_dev.x509 /home/ubuntu/Testing-Procedure-and-Software-tools-IEEE-2030.5-Client/IEEE-2030.5-Client/certs/sat-root.pem https://18.232.7.53:443/dcap