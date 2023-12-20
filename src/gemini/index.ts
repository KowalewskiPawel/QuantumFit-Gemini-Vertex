import { VertexAI } from "@google-cloud/vertexai";
import dotenv from "dotenv";

dotenv.config();

const projectId = process.env.PROJECT_ID as string;
const location = process.env.LOCATION as string;

export const createNonStreamingSinglePartContent = async (prompt: string) => {
  try {
    if (!prompt) {
      throw new Error("Prompt is required");
    }
    const model = "gemini-pro";
    const vertexAI = new VertexAI({ project: projectId, location: location });

    // Instantiate the model
    const generativeVisionModel = vertexAI.preview.getGenerativeModel({
      model,
    });

    const textPart = {
      text: prompt,
    };

    const request = {
      contents: [{ role: "user", parts: [textPart] }],
    };

    console.log("Prompt Text:");
    console.log(request.contents[0].parts[0].text);

    console.log("Non-Streaming Response Text:");
    // Create the response stream
    const responseStream = await generativeVisionModel.generateContentStream(
      request
    );

    // Wait for the response stream to complete
    const aggregatedResponse = await responseStream.response;

    // Select the text from the response
    const fullTextResponse =
      aggregatedResponse.candidates[0].content.parts[0].text;

    return fullTextResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error('Something went wrong in Gemini AI');
  }
};
