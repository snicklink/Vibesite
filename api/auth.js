export default async function handler(req, res) {
  const { code } = req.query;
  
  if (!code) {
    return res.status(400).json({ error: 'No code provided' });
  }

  try {
    // Exchange code for access token
    const response = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code: code,
      }),
    });

    const data = await response.json();
    
    if (data.access_token) {
      // Return the access token to the CMS
      res.json({
        token: data.access_token,
        provider: 'github'
      });
    } else {
      res.status(400).json({ error: 'Failed to get access token', details: data });
    }
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed', details: error.message });
  }
}