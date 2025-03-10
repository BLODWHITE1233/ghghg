const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const app = express();
const PORT = 3000;

// Statik dosyalar
app.use(express.static(path.join(__dirname, 'public')));

// Ana sayfa
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// Log çekme endpoint'i
app.get('/api/logs', (req, res) => {
  const url = req.query.url; // Kullanıcının girdiği URL
  if (!url) {
    return res.status(400).json({ error: 'URL gereklidir.' });
  }

  // Python kodunu çalıştır
  exec(python3 security_bot.py "${url}", (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: stderr });
    }
    res.json({ logs: stdout });
  });
});

app.listen(PORT, () => {
  console.log(Sunucu http://localhost:${PORT} adresinde çalışıyor...);
});