import { compilePack } from "@foundryvtt/foundryvtt-cli";
import fs from "fs";
fs.rmSync("packs/asas-de-cera", { recursive: true, force: true });
await compilePack("src/packs/asas-de-cera", "packs/asas-de-cera", { log: true });
