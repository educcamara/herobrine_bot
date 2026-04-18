import fs from "fs";
import path from "path";
import { getPool } from "./connection.js";
import logger from "../../logging/logger.js";

const migrationDir = new URL("./migrations", import.meta.url);

async function runSqlMigration(pool: any, filename: string, sql: string) {
	logger.info(`Running migration: ${filename}`);
	await pool.query("BEGIN");
	try {
		await pool.query(sql);
		await pool.query(`
			INSERT INTO Migration (id) VALUES ($1)
		`, [filename]);
		await pool.query("COMMIT");
		logger.info(`Migration applied: ${filename}`);
	} catch (error) {
		await pool.query("ROLLBACK");
		logger.error(`Failed to apply migration ${filename}: ${error instanceof Error ? error.message : String(error)}`);
		throw error;
	}
}

export async function runMigrations() {
	const pool = getPool();

	// Ensure Migration Table Exists
	await pool.query(`
		CREATE TABLE IF NOT EXISTS Migration (
			id TEXT PRIMARY KEY,
			executed_at TIMESTAMPTZ DEFAULT NOW()
		);
	`);

	// Get Applied Migrations
	const { rows } = await pool.query("SELECT id FROM Migration");
	const executed = new Set(rows.map(row => row.id));

	// Load Migration Files
	const migrationFiles = fs
		.readdirSync(path.dirname(migrationDir.pathname))
		.filter(file => file.endsWith(".sql"))
		.sort();

	for (const file of migrationFiles) {
		if (executed.has(file)) continue;

		const filePath = path.join(path.dirname(migrationDir.pathname), file);
		const sql = fs.readFileSync(filePath, "utf-8");

		await runSqlMigration(pool, file, sql);
	}

	logger.info("All migrations applied successfully.");
};