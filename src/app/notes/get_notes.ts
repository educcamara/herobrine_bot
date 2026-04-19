import { NoteRepository } from "../../domain/repositories/NoteRepository.js";

export class GetNotes {
	constructor(private repo: NoteRepository) {}

	async execute(userId: string, serverId: string | null) {
		const notes = await this.repo.getNotesByUserId(userId, serverId);
		return notes;
	}
}