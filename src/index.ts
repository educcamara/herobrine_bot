import config from "./config/env.js";
import logger from "./infrastructure/logging/logger.js";
import client from "./bot/bot.js";

client.login(config.discord.token).catch(error => {
  logger.error("Failed to login", error);
});