const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();
const sharp = require('sharp');
const rateLimit = require('express-rate-limit');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');

const app = express();
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production-vercel-env';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// For Vercel serverless - use in-memory storage for demo
// In production, you'd want to use Vercel Blob Storage or similar
const uploadsDir = '/tmp/uploads';
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// Use in-memory SQLite for Vercel demo
// In production, switch to Vercel Postgres or PlanetScale
const db = new sqlite3.Database(':memory:');

// Initialize database tables
db.serialize(() => {
  // Projects table with base64 image storage
  db.run(`CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    long_description TEXT,
    image_data TEXT,
    image_type TEXT,
    project_url TEXT,
    category TEXT DEFAULT 'Spiele',
    color TEXT DEFAULT '#D946EF',
    is_featured BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  // Settings table for theme and site config  
  db.run(`CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  // Admin users table
  db.run(`CREATE TABLE IF NOT EXISTS admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  // Insert default theme if not exists
  db.get("SELECT value FROM settings WHERE key = 'current_theme'", (err, row) => {
    if (!row) {
      db.run("INSERT INTO settings (key, value) VALUES ('current_theme', 'default')");
    }
  });

  // Create default admin user (username: admin, password: admin123)
  db.get("SELECT username FROM admin_users WHERE username = 'admin'", (err, row) => {
    if (!row) {
      const hashedPassword = bcrypt.hashSync('admin123', 10);
      db.run("INSERT INTO admin_users (username, password_hash) VALUES ('admin', ?)", [hashedPassword]);
    }
  });
});

// Simplified file upload for Vercel - store as base64 in database
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit for serverless
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif|webp/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'));
    }
  }
});

// JWT middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

// Load themes
const loadThemes = () => {
  try {
    const themesData = fs.readFileSync(path.join(__dirname, 'themes.json'), 'utf8');
    return JSON.parse(themesData);
  } catch (error) {
    console.error('Error loading themes:', error);
    return { themes: {} };
  }
};

// AUTH ROUTES
app.post('/api/auth/login', [
  body('username').notEmpty().withMessage('Username is required'),
  body('password').notEmpty().withMessage('Password is required')
], (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { username, password } = req.body;

  db.get("SELECT * FROM admin_users WHERE username = ?", [username], (err, user) => {
    if (err) {
      return res.status(500).json({ error: 'Database error' });
    }

    if (!user || !bcrypt.compareSync(password, user.password_hash)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const token = jwt.sign({ id: user.id, username: user.username }, JWT_SECRET, { expiresIn: '24h' });
    res.json({ token, user: { id: user.id, username: user.username } });
  });
});

// PUBLIC ROUTES
// Get all projects
app.get('/api/projects', (req, res) => {
  const { category } = req.query;
  let query = "SELECT * FROM projects";
  let params = [];
  
  if (category) {
    query += " WHERE category = ?";
    params.push(category);
  }
  
  query += " ORDER BY created_at DESC";
  
  db.all(query, params, (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    
    // Convert base64 images to data URLs for frontend
    const projectsWithImages = rows.map(project => ({
      ...project,
      image_url: project.image_data ? `data:${project.image_type};base64,${project.image_data}` : null
    }));
    
    res.json(projectsWithImages);
  });
});

// Serve individual project images
app.get('/api/image/:id', (req, res) => {
  const { id } = req.params;
  
  db.get("SELECT image_data, image_type FROM projects WHERE id = ?", [id], (err, row) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    
    if (!row || !row.image_data) {
      return res.status(404).json({ error: 'Image not found' });
    }
    
    const imageBuffer = Buffer.from(row.image_data, 'base64');
    res.setHeader('Content-Type', row.image_type);
    res.setHeader('Cache-Control', 'public, max-age=31536000');
    res.send(imageBuffer);
  });
});

// Get projects by category
app.get('/api/projects/category/:category', (req, res) => {
  const { category } = req.params;
  db.all("SELECT * FROM projects WHERE category = ? ORDER BY created_at DESC", [category], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

// Get all categories
app.get('/api/categories', (req, res) => {
  res.json({
    categories: ['Spiele', 'Apps', 'Experimentell', 'Systeme']
  });
});

// Get current theme
app.get('/api/theme', (req, res) => {
  db.get("SELECT value FROM settings WHERE key = 'current_theme'", (err, row) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    
    const themeName = row ? row.value : 'default';
    const themes = loadThemes();
    const theme = themes.themes[themeName] || themes.themes.default;
    
    res.json({ current: themeName, theme });
  });
});

// Get all available themes
app.get('/api/themes', (req, res) => {
  const themes = loadThemes();
  res.json(themes);
});

// ADMIN ROUTES (require authentication)
// Create project
app.post('/api/admin/projects', authenticateToken, upload.single('image'), [
  body('title').notEmpty().withMessage('Title is required'),
  body('description').notEmpty().withMessage('Description is required')
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { title, description, long_description, project_url, category, color, is_featured, is_new } = req.body;
  let imageData = null;
  let imageType = null;

  if (req.file) {
    try {
      // Process image and convert to base64
      const processedImage = await sharp(req.file.buffer)
        .resize(500, 318, { fit: 'cover' })
        .jpeg({ quality: 80 })
        .toBuffer();
      
      imageData = processedImage.toString('base64');
      imageType = 'image/jpeg';
    } catch (error) {
      console.error('Image processing error:', error);
      imageData = req.file.buffer.toString('base64');
      imageType = req.file.mimetype;
    }
  }

  db.run(
    "INSERT INTO projects (title, description, long_description, image_data, image_type, project_url, category, color, is_featured, is_new) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    [title, description, long_description || null, imageData, imageType, project_url || null, category || 'Spiele', color || '#D946EF', is_featured === 'true', is_new === 'true'],
    function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({ id: this.lastID, message: 'Project created successfully' });
    }
  );
});

// Update project
app.put('/api/admin/projects/:id', authenticateToken, upload.single('image'), (req, res) => {
  const { id } = req.params;
  const { title, description, long_description, project_url, category, color, is_featured, is_new, remove_image } = req.body;
  
  // Get current project to handle image updates
  db.get("SELECT * FROM projects WHERE id = ?", [id], async (err, project) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (!project) {
      return res.status(404).json({ error: 'Project not found' });
    }

    let imageData = project.image_data;
    let imageType = project.image_type;

    // Handle image removal
    if (remove_image === 'true') {
      imageData = null;
      imageType = null;
    }

    // Handle new image upload
    if (req.file) {
      try {
        // Process new image
        const processedImage = await sharp(req.file.buffer)
          .resize(500, 318, { fit: 'cover' })
          .jpeg({ quality: 80 })
          .toBuffer();
        
        imageData = processedImage.toString('base64');
        imageType = 'image/jpeg';
      } catch (error) {
        console.error('Image processing error:', error);
        imageData = req.file.buffer.toString('base64');
        imageType = req.file.mimetype;
      }
    }

    db.run(
      "UPDATE projects SET title = ?, description = ?, long_description = ?, image_data = ?, image_type = ?, project_url = ?, category = ?, color = ?, is_featured = ?, is_new = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
      [title, description, long_description || null, imageData, imageType, project_url || null, category || 'Spiele', color || '#D946EF', is_featured === 'true', is_new === 'true', id],
      function(err) {
        if (err) {
          return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Project updated successfully' });
      }
    );
  });
});

// Delete project
app.delete('/api/admin/projects/:id', authenticateToken, (req, res) => {
  const { id } = req.params;

  db.run("DELETE FROM projects WHERE id = ?", [id], function(err) {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ message: 'Project deleted successfully' });
  });
});

// Set theme
app.post('/api/admin/theme', authenticateToken, [
  body('theme').notEmpty().withMessage('Theme is required')
], (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { theme } = req.body;
  const themes = loadThemes();

  if (!themes.themes[theme]) {
    return res.status(400).json({ error: 'Invalid theme' });
  }

  db.run(
    "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES ('current_theme', ?, CURRENT_TIMESTAMP)",
    [theme],
    function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({ message: 'Theme updated successfully' });
    }
  );
});

// Note: No longer serving static files - images stored as base64 in database

// Serve admin interface
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

// Simple admin route that works with Vercel
app.get('/', (req, res) => {
  // If the request is for /api, serve API
  // If the request is for /admin, serve admin panel
  const url = req.originalUrl || req.url;
  
  if (url === '/admin' || url.includes('admin')) {
    const adminPath = path.join(__dirname, 'admin.html');
    const adminHTML = fs.readFileSync(adminPath, 'utf8');
    res.setHeader('Content-Type', 'text/html');
    return res.send(adminHTML);
  }
  
  // Default API response
  res.json({ 
    message: 'Vibegame API is running', 
    endpoints: {
      admin: '/admin',
      projects: '/api/projects',
      auth: '/api/auth/login'
    }
  });
});

// Export for Vercel
module.exports = app;