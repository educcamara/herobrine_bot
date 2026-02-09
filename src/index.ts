import config from "../config.json" with { type: "json" };
import logger from "./infrastructure/logging/logger.js";

client.login(config.discord_token).catch(error => {
  logger.error("Failed to login", error);
});