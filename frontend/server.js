const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3001;

// Serve the frontend HTML
app.use(express.static(path.join(__dirname, 'public')));

const { connect } = require('nats');
let nc;

(async () => {
    try {
        nc = await connect({ servers: "nats://54.147.91.126:4222" });
        console.log("Connected to NATS");
    } catch (err) {
        console.error("Failed to connect to NATS:", err);
    }
})();


// Fallback to index.html for unknown routes (optional)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/run-client', (req, res) => {
    const dockerCommand = 'docker exec -i ieee2030-client /app/build/client_test eth0 pti_dev.x509 ./certs/my_ca.pem https://172.18.0.4:1900/dcap all';
    exec(dockerCommand, async (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            if (nc) await nc.publish("ieee.client.response", Buffer.from(`Error: ${error.message}`));
            return res.status(500).send(`Error: ${error.message}`);
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            if (nc) await nc.publish("ieee.client.response", Buffer.from(`Stderr: ${stderr}`));
            return res.status(500).send(`Stderr: ${stderr}`);
        }
        console.log(`stdout: ${stdout}`);
        if (nc) await nc.publish("ieee.client.response", Buffer.from(stdout));
        res.send(`C client ran successfully: ${stdout}`);
    });
});

app.listen(PORT, () => {
    console.log(`Server running at http://54.147.91.126:${PORT}`);
});
