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
      {/* Book with lightbulb - Learning & Education icon */}
      <path
        d="M10 8C10 6.89543 10.8954 6 12 6H52C53.1046 6 54 6.89543 54 8V52C54 53.1046 53.1046 54 52 54H12C10.8954 54 10 53.1046 10 52V8Z"
        fill="currentColor"
        fillOpacity="0.15"
        stroke="currentColor"
        strokeWidth="2"
      />
      <path
        d="M10 18H54M32 6V54"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <circle
        cx="44"
        cy="40"
        r="8"
        fill="currentColor"
        fillOpacity="0.2"
        stroke="currentColor"
        strokeWidth="2"
      />
      <path
        d="M44 35V42M41 42H47"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
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
          Active Recall Coach
        </h1>

        <p className="text-foreground max-w-prose pt-1 leading-6 font-medium">
          Master programming through three powerful learning modes
        </p>
        
        <p className="text-muted-foreground max-w-md pt-2 text-sm leading-5">
          📚 <strong>Learn Mode:</strong> I'll teach you concepts clearly<br/>
          ❓ <strong>Quiz Mode:</strong> Test your knowledge with questions<br/>
          🎓 <strong>Teach Back Mode:</strong> Explain concepts to me and get feedback
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
