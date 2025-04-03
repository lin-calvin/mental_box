
import { hmrPlugin } from '@web/dev-server-hmr';
import { esbuildPlugin } from "@web/dev-server-esbuild";
const replaceNodeEnv = async (ctx, next) => {
  await next();

  // Get the response body
  const body = ctx.body;

  // Check if the response is a string
  if (typeof body === 'string') {
    // Replace all occurrences of process.env.NODE_ENV with 'development'
    ctx.body = body.replace(/process\.env\.NODE_ENV/g, "'development'");
  }
};

export default {
  /////////rootDir: "src",
  middleware:[replaceNodeEnv],
  nodeResolve: {
    exportConditions: ["development"],
  },
  appIndex: "src/index.html",
  plugins: [
    hmrPlugin(),
    esbuildPlugin({
      ts: true,
      js: true,
      target: "es2015",
      define: { "process.env.NODE_ENV": JSON.stringify("development") },
    }),
  ],
};
