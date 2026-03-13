export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { email } = req.query;

  if (!email) {
    return res.status(400).json({ message: 'Email is required' });
  }

  try {
    // Forward the request to the backend API
    const backendUrl = process.env.INTERNAL_API_URL || 'http://127.0.0.1:8000';
    const backendResponse = await fetch(`${backendUrl}/api/tickets/user?email=${encodeURIComponent(email)}`);

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({}));
      return res.status(backendResponse.status).json(errorData);
    }

    const data = await backendResponse.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('Error fetching user tickets:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
}