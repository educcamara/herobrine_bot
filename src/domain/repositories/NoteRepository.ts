
export interface Note {
	id: number;
	userId: string;
	serverId: string | null;
	content: string;
	createdAt: Date;
}

export interface NoteRepository {
	createNote(userId: string, serverId: string | null, content: string): Promise<Note>;
	getNotesByUserId(userId: string, serverId: string | null): Promise<Note[]>
	deleteNoteById(noteId: number): Promise<void>;
}