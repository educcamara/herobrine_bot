import { Pool } from "pg";
import env from "../../../config/env.js";
import logger from "../../logging/logger.js";

let pool: Pool | null = null;

export function getPool(): Pool {
	if (!pool) {
		pool = new Pool({
			host: 		env.db.host,
			port: 		env.db.port,
			database: 	env.db.name,
			user: 		env.db.user,
			password: 	env.db.password,
			ssl: 		env.db.ssl,
		});
	}

	logger.debug(`PostgreSQL connection pool created (${env.db.host}:${env.db.port}/${env.db.name})`);
	return pool;
}