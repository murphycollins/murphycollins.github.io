import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });
  try {
    const { text, task } = req.body;
    if (!text || !task) return res.status(400).json({ error: "Missing text or task" });

    let prompt = task === "summarize" 
      ? `Summarize the following text in 3-4 sentences:\n\n${text}`
      : `Analyze the sentiment (positive, neutral, negative) of this text:\n\n${text}`;

    const completion = await client.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
      max_tokens: 150
    });

    res.status(200).json({ result: completion.choices[0].message.content.trim() });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
