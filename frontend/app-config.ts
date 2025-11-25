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
  companyName: 'Active Recall Coach',
  pageTitle: 'Active Recall Coach - Teach to Learn',
  pageDescription: 'Master programming concepts through active learning: Learn, Quiz, and Teach Back modes',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#3b82f6',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#60a5fa',
  startButtonText: 'Start Learning Session',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
