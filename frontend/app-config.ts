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
  companyName: 'Day 10 Voice Agents Challenge',
  pageTitle: 'Day 10 — Voice Improv Battle',
  pageDescription: 'Join the Day 10 Voice Agent Challenge: build a voice improv agent using Murf Falcon TTS and LiveKit',
  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/lk-wordmark.svg',
  accent: '#2B6CB0',
  logoDark: '/lk-wordmark.svg',
  accentDark: '#2C5282',
  startButtonText: 'Join Day 10 Challenge',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};

