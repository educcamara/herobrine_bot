import fs from "fs";
import path from "path";
import { Collection } from "discord.js";
import { fileURLToPath, pathToFileURL } from "url";

export default class CommandHandler {
	#commands = new Collection();

	constructor(commandsRootUrl) {
		this.commandsRootUrl = commandsRootUrl;
	}

	async load() {
		const commandsPath = fileURLToPath(this.commandsRootUrl);
		// readdirSync returns an array of names (files and folders) present in the directory
		const folders = fs.readdirSync(commandsPath);

		for (const folder of folders) {
			const folderPath = path.join(commandsPath, folder);
			const files = fs
				.readdirSync(folderPath)
				.filter(file => file.endsWith(".js"));

			for (const file of files) {
				const fileUrl = pathToFileURL(
					path.join(folderPath, file)
				);

				const module = await import(fileUrl);
				const command = module.default;

				if (command?.data && command?.execute) {
					this.#commands.set(command.data.name, command);
				} else {
					console.warn(`Command at ${fileUrl} is missing "data" or "execute"`);
					throw new Error(`Invalid command definition in ${fileUrl}`);
				}
			}
		}
	}

	get(name) {
		return this.#commands.get(name);
	}

	async execute(interaction) {
		const command = this.get(interaction.commandName);

		if (!command) {
			console.error(`No command found for ${interaction.commandName}`);
			throw new Error(`Command not found: ${interaction.commandName}`);
		}

		await command.execute(interaction);
	}

	values() {
		return this.#commands.values();
	}

}
