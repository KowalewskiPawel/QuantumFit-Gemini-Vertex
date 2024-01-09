import { Part, VertexAI } from "@google-cloud/vertexai";
import dotenv from "dotenv";

dotenv.config();

const projectId = process.env.PROJECT_ID as string;
const location = process.env.LOCATION as string;

async function getBase64(url: string) {
  const response = await fetch(url);
  const arrayBuffer = await response.arrayBuffer();
  const base64 = Buffer.from(arrayBuffer).toString("base64");
  return base64;
}

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
      generation_config: {
        max_output_tokens: 8192,
        temperature: 0.2,
      },
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
    throw new Error("Something went wrong in Gemini AI");
  }
};

export const sendMultiModalPromptWithImage = async (
  prompt: string,
  photos: string[]
) => {
  try {
    if (!prompt || !photos.length) {
      throw new Error("Prompt is required");
    }
    const model = "gemini-pro-vision";
    // For images, the SDK supports base64 strings
    const base64Photos = await Promise.all(photos.map(getBase64));
    const photosParts = base64Photos.map((photo) => ({
      inlineData: {
        data: photo,
        mimeType: "image/png",
      },
    }));
    // Initialize Vertex with your Cloud project and location
    const vertexAI = new VertexAI({ project: projectId, location: location });

    const generativeVisionModel = vertexAI.preview.getGenerativeModel({
      model,
      generation_config: {
        max_output_tokens: 2048,
        temperature: 0.3,
      },
    });

    const textPart = {
      text: prompt,
    };

    const requestsParts = [textPart, ...photosParts];

    // Pass multimodal prompt
    const request = {
      contents: [
        {
          role: "user",
          parts: requestsParts as unknown as Part[],
        },
      ],
    };

    // Create the response
    const response = await generativeVisionModel.generateContent(request);
    // Wait for the response to complete
    const aggregatedResponse = await response.response;
    // Select the text from the response
    const fullTextResponse =
      aggregatedResponse.candidates[0].content.parts[0].text;

    return fullTextResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error("Something went wrong in Gemini AI");
  }
};

export const sendMultiModalPromptWithVideo = async (
  prompt: string,
  videoUrl: string,
  fileType: string
) => {
  try {
    if (!prompt || !videoUrl || !fileType) {
      throw new Error("Prompt, Video URL, and File Type are required");
    }
    const model = "gemini-pro-vision";

    // Initialize Vertex with your Cloud project and location
    const vertexAI = new VertexAI({ project: projectId, location: location });

    const generativeVisionModel = vertexAI.preview.getGenerativeModel({
      model,
      generation_config: {
        max_output_tokens: 2048,
        temperature: 0.3,
      },
    });

    const videoBase64 = await getBase64(videoUrl);

    const videoPart = {
      inlineData: {
        data: videoBase64,
        mimeType: fileType,
      },
    };
    
    const textPart = {
      text: prompt,
    };

    const requestsParts = [textPart, videoPart];

    const request = {
      contents: [
        {
          role: "user",
          parts: requestsParts as unknown as Part[],
        },
      ],
    };

    // Create the response
    const response = await generativeVisionModel.generateContent(request);
    // Wait for the response to complete
    const aggregatedResponse = await response.response;
    // Select the text from the response
    const fullTextResponse =
      aggregatedResponse.candidates[0].content.parts[0].text;

    return fullTextResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error("Something went wrong in Gemini AI");
  }
};
