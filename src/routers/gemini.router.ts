import { Router } from "express";
import { GeminiController } from "../controllers";

const { geminiImagePrompt, geminiTextPrompt, geminiVideoPrompt } = new GeminiController();

export const geminiRouter = Router().post('/text', geminiTextPrompt).post('/image', geminiImagePrompt).post('/video', geminiVideoPrompt);