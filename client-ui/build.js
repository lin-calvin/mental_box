#!/usr/bin/env node
const fs = require("fs");
const child_process = require("child_process");
const statik = require("node-static");
const esbuild = require("esbuild");
const http = require("http");
const postcss = require("esbuild-postcss");
const buildConfig = {
  entryPoints: ["src/index.ts"],
  bundle: true,
  target: "es2015",
  minify: true,
  //external: ['fs','path'], // sql.js requires this to build
  //loader: { ".css": "text",'.wasm': 'dataurl' },
};

function build() {
  var gitId = "undefined";
  try {
    gitId = child_process
      .execSync("git rev-parse --short HEAD")
      .asciiSlice()
      .replace("\n", "");
    gitId = "'" + gitId + "'";
  } catch (e) {}
  esbuild
    .build(
      Object.assign(
        {
          define: { GITID: gitId },
          sourcemap: true,
          outfile: "build/index.js",
        },
        buildConfig,
      ),
    )
    .catch(() => {})
    .then(() => {
      fs.copyFile("src/index.html", "build/index.html", () => {});
      console.log("Build finished!");
    });
}
function liveserver() {
  var livereload = require("livereload");
  var server = livereload.createServer({ exts: ["html", "css", "js", "ts"] });
  server.watch("./src");
  const file = new statik.Server("./src");
  http
    .createServer(async function (request, response) {
      if (request.url == "/index.js") {
        response.writeHead(200, { "Content-Type": "text/javascript" });
        res = await esbuild.build(
          Object.assign(
            { write: false, define: { GITID: "'LIVESERVER'" } },
            buildConfig,
          ),
        );
        response.write(res.outputFiles[0].text);
        response.end();
      } else {
        if (request.url == "/") {
          response.writeHead(200, { "Content-Type": "text/html" });
          response.write(
            "<script>document.write('<script src=\"http://' + (location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1\"></' + 'script>')</script>",
          );
          response.write(fs.readFileSync("src/index.html"));
          response.end();
        } else {
          file.serve(request, response);
        }
      }
    })
    .listen(8089);
}
if (!process.argv.includes("liveserver")) {
  build();
  if (process.argv.includes("watch")) {
    fs.watch("./src", () => {
      console.log("File changed rebuilding");
      build();
    });
  }
  if (process.argv.includes("serve")) {
    const file = new statik.Server("./build");

    http
      .createServer(function (request, response) {
        request
          .addListener("end", function () {
            //
            // Serve files!
            //
            file.serve(request, response);
          })
          .resume();
      })
      .listen(8089);
  }
} else {
  liveserver();
}
