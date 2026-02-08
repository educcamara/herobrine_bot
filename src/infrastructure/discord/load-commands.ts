import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

export interface LoadedCommand {
  module: unknown;
  fileUrl: URL;
}

/**
 * Loads command modules from a directory.
 *
 * @param {URL} commandsRootUrl
 * @returns {Promise<Array<{ module, fileUrl }>>}
 */
export async function loadCommands(
  commandsRootUrl: URL
): Promise<LoadedCommand[]> {
  const commands: LoadedCommand[] = [];

  const commandsPath = fileURLToPath(commandsRootUrl);
  const folders = fs.readdirSync(commandsPath);

  for (const folder of folders) {
    const folderPath = path.join(commandsPath, folder);
    const files = fs
      .readdirSync(folderPath)
      .filter(f => f.endsWith(".js") || f.endsWith(".ts"));

    for (const file of files) {
      const filePath = path.join(folderPath, file);
      const fileUrl = pathToFileURL(filePath);

      const module = await import(fileUrl.href);

      commands.push({
        module: module.default,
        fileUrl
      });
    }
  }

  return commands;
}