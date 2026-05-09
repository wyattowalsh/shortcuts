import { createMDX } from 'fumadocs-mdx/next';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  turbopack: {
    root: resolve(__dirname, '../..'),
  },
};

const withMDX = createMDX({
  configPath: './source.config.ts',
});

export default withMDX(config);
