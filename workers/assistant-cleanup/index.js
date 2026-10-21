// Daily retention job for the Ask OmniFit log. Pages Functions cannot run on
// a schedule, so this tiny Worker, bound to the same D1 database as the Pages
// project (binding DB), runs the same cleanup() the functions run: log rows
// older than 90 days, rate-limit windows older than two hours and salts older
// than a day are deleted. Deploy steps: DEPLOY.md, "Ask OmniFit".
import { cleanup } from "../../functions/_lib/assistant.js";

export default {
  async scheduled(controller, env, ctx) {
    if (!env.DB) throw new Error("assistant-cleanup: D1 binding DB is missing");
    await cleanup(env.DB, new Date());
  },
};
