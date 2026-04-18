import { Note, NoteRepository } from "../../../../domain/repositories/NoteRepository.js";
import { getPool } from "../connection.js";

type NoteRow = {
	id: number;
	user_id: string;
	content: string;
	created_at: Date;
};

export class PostgresNoteRepository implements NoteRepository {
	constructor(private pool = getPool()) {}

	async createNote(userId: string, content: string): Promise<Note> {
		const result: { rows: NoteRow[] } = await this.pool.query(
			"INSERT INTO Note (user_id, content) VALUES ($1, $2) RETURNING id, user_id, content, created_at",
			[userId, content]
		);
		return this.mapRowToNote(result.rows[0]);
	}

	async getNotesByUserId(userId: string): Promise<Note[]> {
		const result: { rows: NoteRow[] } = await this.pool.query(
			"SELECT id, user_id, content, created_at FROM Note WHERE user_id = $1 ORDER BY created_at DESC",
			[userId]
		);
		return result.rows.map(row => this.mapRowToNote(row));
	}

	async deleteNoteById(noteId: number): Promise<void> {
		await this.pool.query(
			"DELETE FROM Note WHERE id = $1",
			[noteId]
		);
	}

	// Private Methods

	private mapRowToNote(row: NoteRow): Note {
		return {
			id: 		row.id,
			userId: 	row.user_id,
			content: 	row.content,
			createdAt: 	row.created_at
		};
	}
}