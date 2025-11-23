export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'MindfulMate',
  pageTitle: 'MindfulMate - Your Wellness Companion',
  pageDescription: 'Start your daily wellness check-in with your AI-powered mindfulness companion',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#10b981',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#34d399',
  startButtonText: 'Start Wellness Check-In',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
