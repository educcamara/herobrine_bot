import fs from "fs";
import path from "path";
import { getPool } from "./connection.js";
import logger from "../../logging/logger.js";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const migrationsPath = path.join(__dirname, "migrations");

async function runSqlMigration(pool: any, filename: string, sql: string) {
	logger.info(`Running migration: ${filename}`);
	const client = await pool.connect();
	try {
		await client.query("BEGIN");
		await client.query(sql);
		await client.query(`
			INSERT INTO Migration (id) VALUES ($1)
		`, [filename]);
		await client.query("COMMIT");
		logger.info(`Migration applied: ${filename}`);
	} catch (error) {
		await client.query("ROLLBACK");
		logger.error(`Failed to apply migration ${filename}: ${error instanceof Error ? error.message : String(error)}`);
		throw error;
	} finally {
		client.release();
	}
}

async function runMigrations() {
	logger.info("Starting database migrations");
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
		.readdirSync(migrationsPath)
		.filter(file => file.endsWith(".sql"))
		.sort();

	logger.info(`Found ${migrationFiles.length} migration(s), ${executed.size} already applied.`);

	for (const file of migrationFiles) {
		if (executed.has(file)) continue;

		const filePath = path.join(migrationsPath, file);
		const sql = fs.readFileSync(filePath, "utf-8");

		await runSqlMigration(pool, file, sql);
	}

	logger.info("All migrations applied successfully.");
}

try {
	await runMigrations();
	process.exit(0);
} catch (error) {
	process.exit(1);
}