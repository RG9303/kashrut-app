import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.ayinlens.app',
  appName: 'Ayin Lens',
  webDir: 'public',
  server: {
    url: 'https://kashrut-app.vercel.app',
    cleartext: true
  }
};

export default config;
