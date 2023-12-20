# QuantumFit Vertex API

## About

This is a simple Node.js Express powered web service, to leverage the Gemini API with the use of VertexAI library.

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

## Disclaimer

This is not an official Google product.
