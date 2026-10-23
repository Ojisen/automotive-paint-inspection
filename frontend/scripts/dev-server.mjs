import http from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import { dirname, extname, join, normalize, resolve } from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const root = resolve(scriptDir, "..");
const publicRoot = join(root, "public");
const args = process.argv.slice(2);
const portArgIndex = args.indexOf("--port");
const port = portArgIndex >= 0 ? Number(args[portArgIndex + 1]) : 3000;
const host = "127.0.0.1";
const shouldOpen = args.includes("--open");

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".jsx": "text/babel; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

function sendFile(res, filePath) {
  const type = mimeTypes[extname(filePath).toLowerCase()] || "application/octet-stream";
  res.writeHead(200, { "Content-Type": type });
  createReadStream(filePath).pipe(res);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url || "/", `http://${host}:${port}`);
  const requestedPath = decodeURIComponent(url.pathname);
  const relativePath = requestedPath === "/" ? "index.html" : requestedPath.slice(1);
  const filePath = normalize(join(root, relativePath));
  const publicFilePath = normalize(join(publicRoot, relativePath));

  if (!filePath.startsWith(root) || !publicFilePath.startsWith(publicRoot)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  const candidate = existsSync(publicFilePath) && statSync(publicFilePath).isFile()
    ? publicFilePath
    : existsSync(filePath) && statSync(filePath).isFile()
    ? filePath
    : join(root, "index.html");

  sendFile(res, candidate);
});

server.listen(port, host, () => {
  const url = `http://${host}:${port}`;
  console.log("Paint inspection frontend");
  console.log(`Serving: ${root}`);
  console.log(`URL: ${url}`);
  console.log("Press CTRL+C to stop.");

  if (shouldOpen) {
    spawn("cmd", ["/c", "start", url], { detached: true, stdio: "ignore" }).unref();
  }
});
