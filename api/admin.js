const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  // Read the admin.html file
  const adminPath = path.join(__dirname, 'admin.html');
  
  try {
    const adminHTML = fs.readFileSync(adminPath, 'utf8');
    res.setHeader('Content-Type', 'text/html');
    res.status(200).send(adminHTML);
  } catch (error) {
    console.error('Error serving admin page:', error);
    res.status(500).json({ error: 'Failed to load admin page' });
  }
};