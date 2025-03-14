module.exports = {
  entryPoints: ['./src/index.ts'],
  bundle: true,
  outdir: './dist',
  minify: true,
  sourcemap: true,
  loader: {
    '.ts': 'ts',
    '.css': 'css',
  },
  plugins: [
    {
      name: 'tailwindcss',
      setup(build) {
        build.onLoad({ filter: /\.css$/ }, async (args) => {
          const fs = require('fs').promises;
          const content = await fs.readFile(args.path, 'utf8');
          return {
            contents: content.replace(/@tailwind (.*);/g, (match, p1) => {
              return `@import 'tailwindcss/${p1}';`;
            }),
            loader: 'css',
          };
        });
      },
    },
  ],
};