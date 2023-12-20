import type { Request, Response } from 'express';
import { createNonStreamingSinglePartContent } from '../gemini';

export class GeminiController {
  public geminiTextPrompt = async (
    req: Request,
    res: Response
  ): Promise<void> => {
    try {
      const { prompt } = req.body;
      const geminiResponse = await createNonStreamingSinglePartContent(prompt);
      res.status(200).json({ message: geminiResponse });
    } catch (error) {
      console.error(error);
      if (error instanceof Error) {
        res.status(500).json({ error: error.message });
      } else {
        res.sendStatus(500).json({ error: 'Unknown error' });
      }
    }
  };
}
