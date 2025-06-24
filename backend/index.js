const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/api/ping', (req, res) => {
  res.json({ message: 'Express is running' });
});

app.listen(3001, () => console.log('Express listening on port 3001'));
