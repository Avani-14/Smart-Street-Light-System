const express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// In-memory storage of accident data
let accidentData = [];

// Serve index.html at root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Receive data via POST (from Python/IoT device)
app.post('/', (req, res) => {
    const data = req.body;
    if (data) {
        console.log("Received data:", data);
        accidentData.push(data);
        res.status(200).send('Data received successfully');
    } else {
        res.status(400).send('Invalid data');
    }
});

// Send data to frontend
app.get('/data', (req, res) => {
    res.json(accidentData);
});

// Start server
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
