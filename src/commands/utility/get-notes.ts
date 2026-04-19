import { ChatInputCommandInteraction, MessageFlags, SlashCommandBuilder } from "discord.js";
import { Command } from "../../domain/commands/Command.js";
import { Note } from "../../domain/repositories/NoteRepository.js";

// Use case and repository imports
import { GetNotes } from "../../app/notes/get_notes.js";
import { PostgresNoteRepository } from "../../infrastructure/database/postgres/repositories/PostgresNoteRepository.js";
import logger from "../../infrastructure/logging/logger.js";

const getNotesUseCase = new GetNotes(new PostgresNoteRepository());

function formatDate(date: Date): string {
	return date.toLocaleString("en-US", {
		year: "numeric",
		month: "short",
		day: "numeric"
	});
}

function formatNotes(notes: Note[]): string[] {
	if (notes.length === 0) {
		throw new Error("You have no notes.");
	}
	return notes.map(note => `- (${formatDate(note.createdAt)}) ${note.content} (ID: ${note.id})`);
}

const command: Command = {
	data: new SlashCommandBuilder()
		.setName("getnotes")
		.setDescription("Retrieves all notes for the user."),
	
	async execute(interaction: ChatInputCommandInteraction) {
		const userId = interaction.user.id;
		const serverId = interaction.guildId;

		const notes: Note[] = await getNotesUseCase.execute(userId, serverId);
		logger.info(`Retrieved ${notes.length} notes for user ${userId} in server ${serverId || "DM"}`);
		if (notes.length === 0) {
			await interaction.reply({
				content: "You have no notes.",
				// flags: MessageFlags.Ephemeral
			});
			return;
		}

		const formattedNotes = formatNotes(notes);
		logger.info(`Formatted notes for user ${userId} in server ${serverId || "DM"}`);

		await interaction.reply({
			content: `Your notes:\n${formattedNotes.join("\n")}`,
			// flags: MessageFlags.Ephemeral
		});
	},
}

export default command;