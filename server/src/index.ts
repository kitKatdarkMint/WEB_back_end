import express from "express";
import cors from "cors";
import { MongoClient } from "mongodb";
import dotenv from "dotenv";
import BonsPlansRouter from "./routes/BonsPlans";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const uri = process.env.MONGO_URI as string;
const dbName = process.env.DB_NAME as string;

let db: any;

MongoClient.connect(uri)
  .then((client) => {
    console.log("✅ Connecté à MongoDB");
    db = client.db(dbName);
    app.locals.db = db;

    // Routes
    app.use("/api/BonsPlans", BonsPlansRouter);

    const PORT = process.env.PORT || 5000;
    app.listen(PORT, () => {
      console.log(`🚀 Serveur lancé sur http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("❌ Erreur de connexion à MongoDB", err);
  });
