import { Button } from '@/components/livekit/button';
import Image from 'next/image';

function WelcomeImage() {
  return (
    <div className="relative mb-8 flex justify-center">
      <div className="absolute inset-0 bg-gradient-to-r from-sky-400/20 to-indigo-400/20 rounded-full blur-3xl" />
      <Image
        src="/lk-logo.svg"
        alt="Day 10 Logo"
        width={120}
        height={120}
        className="relative z-10"
        priority
      />
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref} className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-sky-50/30 dark:to-indigo-950/10">
      <section className="flex flex-col items-center justify-center text-center px-4 py-12 max-w-3xl">
        <WelcomeImage />
        <h1 className="text-foreground text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-sky-600 to-indigo-600 dark:from-sky-400 dark:to-indigo-400 bg-clip-text text-transparent">
          Day 10 — Voice Improv Battle
        </h1>

        <p className="text-foreground/90 text-lg md:text-xl max-w-2xl pt-2 leading-7 font-medium">
          Announcing Day 10 of the Voice Agents Challenge — build a live, playful Voice Improv Battle agent that talks, reacts, and "yes-and"s with you. We recommend Murf Falcon TTS for the fastest, most natural audio.
        </p>

        

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8 mb-8 w-full max-w-2xl">
          <div className="bg-card/50 backdrop-blur p-5 rounded-xl border border-border/50 hover:border-primary/50 transition-colors">
            <div className="text-3xl mb-2"></div>
            <h3 className="font-semibold text-foreground mb-1">Day 10 Task</h3>
            <p className="text-sm text-muted-foreground">Voice Improv Battle — follow the challenge link for details and submission instructions</p>
          </div>
          <div className="bg-card/50 backdrop-blur p-5 rounded-xl border border-border/50 hover:border-primary/50 transition-colors">
            <div className="text-3xl mb-2"></div>
            <h3 className="font-semibold text-foreground mb-1">Murf Falcon</h3>
            <p className="text-sm text-muted-foreground">Use Murf Falcon TTS for fastest, low-latency voice synthesis (recommended)</p>
          </div>
          <div className="bg-card/50 backdrop-blur p-5 rounded-xl border border-border/50 hover:border-primary/50 transition-colors">
            <div className="text-3xl mb-2"></div>
            <h3 className="font-semibold text-foreground mb-1">Resources</h3>
            <p className="text-sm text-muted-foreground">Docs, examples and the submission form — the agent will share these in-session as well</p>
          </div>
        </div>

        <Button
          variant="primary"
          size="lg"
          onClick={onStartCall}
          className="mt-4 px-8 py-6 text-lg font-semibold shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-all"
        >
          {startButtonText}
        </Button>

        <p className="text-muted-foreground text-sm mt-6">
          Click to start a short improv exchange — try a character, line, or a mood (e.g., "pirate", "melodramatic", "overly excited") and the agent will play along.
        </p>
      </section>
    </div>
  );
};
