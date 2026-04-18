import { NoteRepository } from "../../domain/repositories/NoteRepository.js";
import logger from "../../infrastructure/logging/logger.js";

export class CreateNote {
	constructor(private repo: NoteRepository) {}

	async execute(userId: string, content: string) {
		if (content.trim().length === 0) {
			throw new Error("Note content cannot be empty.");
		}

		const note = await this.repo.createNote(userId, content);
		logger.debug(`Note created (ID: ${note.id}, UserID: ${note.userId})`);
		return note;
	}
}