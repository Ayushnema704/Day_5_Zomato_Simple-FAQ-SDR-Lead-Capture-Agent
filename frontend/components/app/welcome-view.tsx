import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <svg
      width="64"
      height="64"
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="text-primary mb-4 size-16"
    >
      {/* Heart with pulse line - Health & Wellness icon */}
      <path
        d="M32 52C32 52 8 38 8 22C8 18.8174 9.26428 15.7652 11.5147 13.5147C13.7652 11.2643 16.8174 10 20 10C24 10 27.5 12 32 16C36.5 12 40 10 44 10C47.1826 10 50.2348 11.2643 52.4853 13.5147C54.7357 15.7652 56 18.8174 56 22C56 38 32 52 32 52Z"
        fill="currentColor"
        fillOpacity="0.2"
        stroke="currentColor"
        strokeWidth="2"
      />
      <path
        d="M8 32L14 32L18 26L22 38L26 32L32 32"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
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
    <div ref={ref}>
      <section className="bg-background flex flex-col items-center justify-center text-center">
        <WelcomeImage />

        <h1 className="text-foreground text-3xl font-bold mb-2 mt-4">
          Health & Wellness Companion
        </h1>

        <p className="text-foreground max-w-prose pt-1 leading-6 font-medium">
          Your supportive daily check-in companion for mood, energy, and goals
        </p>
        
        <p className="text-muted-foreground max-w-md pt-2 text-sm leading-5">
          Take a moment to reflect on how you're feeling today. Share your mood, energy level, 
          and what you'd like to accomplish. Let's make today great together! 💚
        </p>

        <Button variant="primary" size="lg" onClick={onStartCall} className="mt-6 w-64 font-mono">
          {startButtonText}
        </Button>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-muted-foreground max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm">
          Need help getting set up? Check out the{' '}
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://docs.livekit.io/agents/start/voice-ai/"
            className="underline"
          >
            Voice AI quickstart
          </a>
          .
        </p>
      </div>
    </div>
  );
};
