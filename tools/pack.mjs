import { compilePack } from "@foundryvtt/foundryvtt-cli";
import fs from "fs";
for (const p of ["asas-de-cera", "reflexos-no-espelho"]) {
  if (!fs.existsSync(`src/packs/${p}`)) continue;
  fs.rmSync(`packs/${p}`, { recursive: true, force: true });
  await compilePack(`src/packs/${p}`, `packs/${p}`, { log: true });
}
