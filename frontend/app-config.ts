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
  companyName: 'Zomato',
  pageTitle: 'Zomato - Partner with Us',
  pageDescription: 'Connect with our AI-powered SDR to discover how Zomato can help grow your restaurant business',
  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/logo.png',
  accent: '#E23744',
  logoDark: '/logo.png',
  accentDark: '#ff4d5a',
  startButtonText: 'Talk to Zomato',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};

