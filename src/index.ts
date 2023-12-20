import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';

dotenv.config();

const PORT = process.env.PORT || 3000;

const app = express();

app
  .use(express.json())
  .use(express.urlencoded({ extended: true }))
  .use(cors())
  .use(helmet());

app.get('/', (_req, res) => {
  res.send('Hello Gemini AI!');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
