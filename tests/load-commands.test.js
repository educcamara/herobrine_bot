import test from "node:test";
import assert from "node:assert/strict";
import fs from "fs";
import path from "path";
import os from "os";

import { fileURLToPath, pathToFileURL } from "url";
import { loadCommands } from "../src/infrastructure/discord/load-commands.js";

/**
 * Helper to create a temp command file
 */
function writeCommand(filePath, exportObject) {
	fs.writeFileSync(
		filePath,
		`export default ${JSON.stringify(exportObject)};`,
		"utf-8"
	);
}

test("loadCommands loads command modules from subfolders", async () => {
	// Arrange
	const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "commands-test-"));

	const commandsRoot = path.join(tmpDir, "commands");
	fs.mkdirSync(commandsRoot);

	const utilityDir = path.join(commandsRoot, "utility");
	const adminDir = path.join(commandsRoot, "admin");

	fs.mkdirSync(utilityDir);
	fs.mkdirSync(adminDir);

	writeCommand(
		path.join(utilityDir, "ping.js"),
		{ data: { name: "ping" }, execute: () => {} }
	);

	writeCommand(
		path.join(adminDir, "ban.js"),
		{ data: { name: "ban" }, execute: () => {} }
	);

	// Act
	const result = await loadCommands(pathToFileURL(commandsRoot));

	// Assert
	assert.equal(result.length, 2);

	const names = result.map(({ module }) => module.data.name);
	assert.deepEqual(names.sort(), ["ban", "ping"]);
});

test("loadCommands ignores non-js files", async () => {
	// Arrange
	const tmpDir = fs.mkdtempSync(
		path.join(os.tmpdir(), "commands-test-")
	);

	const commandsRoot = path.join(tmpDir, "commands");
	fs.mkdirSync(commandsRoot);

	const utilityDir = path.join(commandsRoot, "utility");
	fs.mkdirSync(utilityDir);

	fs.writeFileSync(
		path.join(utilityDir, "README.md"),
		"# not a command"
	);

	writeCommand(
		path.join(utilityDir, "ping.js"),
		{ data: { name: "ping" }, execute: () => {} }
	);

	// Act
	const result = await loadCommands(
		pathToFileURL(commandsRoot)
	);

	// Assert
	assert.equal(result.length, 1);
	assert.equal(result[0].module.data.name, "ping");
});

test("loadCommands returns fileUrl for each command", async () => {
	// Arrange
	const tmpDir = fs.mkdtempSync(
	path.join(os.tmpdir(), "commands-test-")
	);

	const commandsRoot = path.join(tmpDir, "commands");
	fs.mkdirSync(commandsRoot);

	const utilityDir = path.join(commandsRoot, "utility");
	fs.mkdirSync(utilityDir);

	writeCommand(
	path.join(utilityDir, "ping.js"),
	{ data: { name: "ping" }, execute: () => {} }
	);

	// Act
	const result = await loadCommands(
		pathToFileURL(commandsRoot)
	);

	// Assert
	assert.ok(result[0].fileUrl instanceof URL);
	assert.ok(result[0].fileUrl.href.endsWith("ping.js"));
});