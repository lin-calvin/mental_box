import { esbuildPlugin } from "@web/dev-server-esbuild";

export default {
  /////////rootDir: "src",
  nodeResolve: {
    exportConditions: ["development"],
  },
  appIndex: "src/index.html",
  plugins: [
    esbuildPlugin({
      ts: true,
      js: true,
      target: "es2015",
      define: { "process.env.NODE_ENV": JSON.stringify("development") },
    }),
  ],
};
