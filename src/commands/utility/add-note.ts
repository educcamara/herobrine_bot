import { ChatInputCommandInteraction, MessageFlags, SlashCommandBuilder } from "discord.js";
import logger from "../../infrastructure/logging/logger.js";
import { Command } from "../../domain/commands/Command.js";

// Use case and repository imports
import { CreateNote } from "../../app/notes/create-note.js";
import { PostgresNoteRepository } from "../../infrastructure/database/postgres/repositories/PostgresNoteRepository.js";

const createNoteUseCase = new CreateNote(new PostgresNoteRepository());

const command: Command = {
	data: new SlashCommandBuilder()
		.setName("addnote")
		.setDescription("Adds a note for the user.")
		.addStringOption(option =>
			option.setName("content")
				.setDescription("The content of the note")
				.setRequired(true)
		),
	
	async execute(interaction: ChatInputCommandInteraction) {
		const userId = interaction.user.id;
		const content = interaction.options.getString("content", true);

		try {
			const note = await createNoteUseCase.execute(userId, content);
			await interaction.reply({
				content: `Note added! (ID: ${note.id})`,
				flags: MessageFlags.Ephemeral
			});
		} catch (error) {
			const errorMessage = error instanceof Error ? error.message : String(error);
			logger.error(`Error adding note: ${errorMessage}`);
			await interaction.reply({
				content: `Failed to add note: ${errorMessage}`,
				flags: MessageFlags.Ephemeral
			});
		}
	}
};

export default command;