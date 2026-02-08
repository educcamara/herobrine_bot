import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

/**
 * Loads command modules from a directory.
 *
 * @param {URL} commandsRootUrl
 * @returns {Promise<Array<{ module, fileUrl }>>}
 */
export async function loadCommands(commandsRootUrl) {
  const commands = [];

  const commandsPath = fileURLToPath(commandsRootUrl);
  const folders = fs.readdirSync(commandsPath);

  for (const folder of folders) {
    const folderPath = path.join(commandsPath, folder);
    const files = fs
      .readdirSync(folderPath)
      .filter(f => f.endsWith(".js"));

    for (const file of files) {
      const filePath = path.join(folderPath, file);
      const fileUrl = pathToFileURL(filePath);

      const module = await import(fileUrl);

      commands.push({
        module: module.default,
        fileUrl
      });
    }
  }

  return commands;
}