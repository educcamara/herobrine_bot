import { config } from 'dotenv';
import path from 'path';

const env = process.env.NODE_ENV || 'development';

config(
	{ path: path.resolve(process.cwd(), `.env.${env}`) }
)

export default {
	nodeEnv: env,
	db: {
		host: 		process.env.DB_HOST,
		port: 		Number(process.env.DB_PORT),
		name: 		process.env.DB_NAME,
		user: 		process.env.DB_USER,
		password: 	process.env.DB_PASSWORD,
		ssl: 		process.env.DB_SSL === 'true',
	},
};