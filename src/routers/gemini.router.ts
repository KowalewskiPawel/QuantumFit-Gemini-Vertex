import { Router } from "express";
import { GeminiController } from "../controllers";

const GeminiControllerInstance = new GeminiController();

export const geminiRouter = Router().post('/text', GeminiControllerInstance.geminiTextPrompt);