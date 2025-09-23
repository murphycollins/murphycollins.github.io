import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });
  try {
    const { prompt } = req.body;
    if (!prompt) return res.status(400).json({ error: "Missing prompt" });

    const response = await client.images.generate({
      model: "gpt-image-1",
      prompt,
      size: "1024x1024"
    });

    res.status(200).json({ url: response.data[0].url });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
