import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

import {
  Client,
  Events,
  GatewayIntentBits,
  Collection
} from "discord.js";

import config from "../config.json" with { type: "json" };
import logger from "./logger.js";

// Setup
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Client
const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

client.commands = new Collection();

// Load Commands
const commandsPath = path.join(__dirname, "commands");
const commandFolders = fs.readdirSync(commandsPath);

for (const folder of commandFolders) {
  const folderPath = path.join(commandsPath, folder);
  const commandFiles = fs
    .readdirSync(folderPath)
    .filter(file => file.endsWith(".js"));

  for (const file of commandFiles) {
    const filePath = path.join(folderPath, file);

    const commandModule = await import(
      pathToFileURL(filePath)
    );

    const command = commandModule.default;

    if (command?.data && command?.execute) {
      client.commands.set(command.data.name, command);
    } else {
      logger.warn(
        `Command at ${filePath} is missing "data" or "execute"`
      );
    }
  }
}

// Events
client.once(Events.ClientReady, readyClient => {
  logger.info(`Logged in as ${readyClient.user.tag}`);
});

// Login
client.login(config.discord_token).catch(error => {
  logger.error("Failed to login", error);
});