# QuantumFit Vertex API

## About

This is a simple Node.js Express powered web service, to leverage the Gemini API with the use of VertexAI library.

# Frontend Repository

[QuantumFit Frontend](https://github.com/KowalewskiPawel/QuantumFit)

# Quantum Fit

| | |
| - |- |
| ![Screenshot of our QuantumFit App](/logoEntry.png "Screenshot of our QuantumFit App") | Introducing QuantumFit! A revolutionary fitness app using the power of AI to help you physically become a better version of yourself! |

Our experts in artificial intelligence have helped design an intelligent gym companion that goes beyond conventional personal training. Our team is driven by the belief that everyone deserves access to a customized, effective, and personalized workout routine without the need for a dedicated trainer. Imagine the experience of a personal trainer in an app that completely adapts to your individual needs, requirements, fitness ability and goals.

Start by uploading several photos of yourself to get a fully customized body analysis breakdown to see where your body is lacking and could be improved. Then you can create a custom tailored workout plan that will help you meet your weight and healthy lifestyle goals. If that isn't enough, we also provide you with a complete weekly meal plan that can be adjusted to fit your dietary needs. This is enough to get you started and going on your fitness journey.

Then comes the best part. Now sure what you are doing or unsure if your form is correct? Our real-time feedback video analyzer will let you take a short video of yourself doing an exercise and our intelligent AI will let you know if your form is off or if you are doing the exercise incorrectly.

Make sure to check out QuantumFit today, so we can help you on your journey towards a healthier lifestyle and fitter body.

## Getting Started

### Prerequisites

- Node.js (v18.18.2)
- Google Application Credentials json file

### Installation

1. Clone the repo
2. Install NPM packages
   ```sh
   npm install
   ```
3. Create a .env file in the root directory and add the following variables
   ````sh
   PROJECT_ID=''
   LOCATION=''
   PORT=8080
   ````
4. Copy the Google Application Credentials json file to the root directory
5. Update Google Application Credentials json file path in the `package.json` scripts
   ```sh
       "start": "GOOGLE_APPLICATION_CREDENTIALS=./<GOOGLE_APPLICATION_CREDENTIALS_FILE_NAME>.json node ./src/index.js",
        "dev": "GOOGLE_APPLICATION_CREDENTIALS=./<GOOGLE_APPLICATION_CREDENTIALS_FILE_NAME>.json nodemon",
   ```

## Usage

### Start the service

```sh
npm run dev
```

# TruLens

TruLens implementation can be found in the `/TruLens` directory. It works as a standalone service and can be started with the following command:

```sh
python3 <name_of_file>.py
```

Gemini AI is built in as custom provider, that instead using the Google Cloud API, it uses post requests to the local backend that is running on port 8080.

### Test the service

You can use Postman to test the service. The service has the following endpoints:

- POST /api/v1/gemini/text - To analyze text

Body:

```json
{
  "prompt": "This is a sample text"
}
```

- POST /api/v1/gemini/image - To analyze image ONLY PNG images are supported

Body:

```json
{
   "prompt": "This is a sample text",
  "photos": ["imageurl"]
}
```

- POST /api/v1/gemini/video - To analyze video

Body:

```json
{
  "prompt": "This is a sample text",
  "video": "videourl",
  "fileType": "video/mp4"
}
```

## Disclaimer

This is not an official Google product.
