import type { Request, Response } from "express";
import {
  createNonStreamingSinglePartContent,
  sendMultiModalPromptWithImage,
  sendMultiModalPromptWithVideo,
} from "../gemini";

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
        res.sendStatus(500).json({ error: "Unknown error" });
      }
    }
  };

  public geminiImagePrompt = async (
    req: Request,
    res: Response
  ): Promise<void> => {
    try {
      const { prompt, photos } = req.body;
      const geminiResponse = await sendMultiModalPromptWithImage(
        prompt,
        photos
      );
      res.status(200).json({ message: geminiResponse });
    } catch (error) {
      console.error(error);
      if (error instanceof Error) {
        res.status(500).json({ error: error.message });
      } else {
        res.sendStatus(500).json({ error: "Unknown error" });
      }
    }
  };

  public geminiVideoPrompt = async (
    req: Request,
    res: Response
  ): Promise<void> => {
    try {
      const { prompt, videoUrl, fileType } = req.body;
      const geminiResponse = await sendMultiModalPromptWithVideo(
        prompt,
        videoUrl,
        fileType
      );
      res.status(200).json({ message: geminiResponse });
    } catch (error) {
      console.error(error);
      if (error instanceof Error) {
        res.status(500).json({ error: error.message });
      } else {
        res.sendStatus(500).json({ error: "Unknown error" });
      }
    }
  };
}
