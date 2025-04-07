import { Router } from "express";

const router = Router();

router.get("/", async (req, res) => {
  const db = req.app.locals.db;
  const users = await db.collection("BonsPlans").find({}).toArray();
  res.json(users);
});

export default router;
