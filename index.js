import client from "./src/bot.js";
import config from "./config.json" with { type: "json" };
import logger from "./src/infra/logger.js";

client.login(config.discord_token).catch(error => {
  logger.error("Failed to login", error);
});