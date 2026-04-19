import { config } from "dotenv";
import path from "path";

const env = process.env.NODE_ENV || "development";

config({
	path: path.resolve(process.cwd(), `.env.${env}`)
});

function requireEnv(name: string): string {
	const value = process.env[name];
	if (!value) {
		throw new Error(`Missing environment variable: ${name}`);
	}
	return value;
}

const configObject = {
	nodeEnv: env,

	db: {
		host: requireEnv("DB_HOST"),
		port: Number(requireEnv("DB_PORT")),
		name: requireEnv("DB_NAME"),
		user: requireEnv("DB_USER"),
		password: requireEnv("DB_PASSWORD"),
		ssl: process.env.DB_SSL === "true"
			? { rejectUnauthorized: false }
			: false
	},

	discord: {
		token: requireEnv("DISCORD_TOKEN"),
		clientId: requireEnv("CLIENT_ID"),
		guildId: process.env.GUILD_ID
	}
};

export default configObject;