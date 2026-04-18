
export interface Note {
	id: number;
	userId: string;
	content: string;
	createdAt: Date;
}

export interface NoteRepository {
	createNote(userId: string, content: string): Promise<Note>;
	getNotesByUserId(userId: string): Promise<Note[]>;
	deleteNoteById(noteId: number): Promise<void>;
}