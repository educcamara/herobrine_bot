import config from "../config.json" with { type: "json" };
import logger from "./infrastructure/logging/logger.js";
import client from "./bot/bot.js";

client.login(config.discord_token).catch(error => {
  logger.error("Failed to login", error);
});