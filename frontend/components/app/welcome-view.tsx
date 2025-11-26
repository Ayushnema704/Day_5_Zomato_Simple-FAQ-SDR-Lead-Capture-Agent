import { Button } from '@/components/livekit/button';
import Image from 'next/image';

function WelcomeImage() {
  return (
    <div className="relative mb-8 flex justify-center">
      <div className="absolute inset-0 bg-gradient-to-r from-red-500/20 to-orange-500/20 rounded-full blur-3xl" />
      <Image
        src="/logo.png"
        alt="Zomato Logo"
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
    <div ref={ref} className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-red-50/30 dark:to-red-950/10">
      <section className="flex flex-col items-center justify-center text-center px-4 py-12 max-w-3xl">
        <WelcomeImage />

        <h1 className="text-foreground text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-red-600 to-orange-600 dark:from-red-400 dark:to-orange-400 bg-clip-text text-transparent">
          Partner with Zomato
        </h1>

        <p className="text-foreground/90 text-lg md:text-xl max-w-2xl pt-2 leading-7 font-medium">
          Discover how India's leading food delivery platform can help grow your restaurant business
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8 mb-8 w-full max-w-2xl">
          <div className="bg-card/50 backdrop-blur p-5 rounded-xl border border-border/50 hover:border-primary/50 transition-colors">
            <div className="text-3xl mb-2"></div>
            <h3 className="font-semibold text-foreground mb-1">Food Delivery</h3>
            <p className="text-sm text-muted-foreground">Reach millions of hungry customers</p>
          </div>
          <div className="bg-card/50 backdrop-blur p-5 rounded-xl border border-border/50 hover:border-primary/50 transition-colors">
            <div className="text-3xl mb-2"></div>
            <h3 className="font-semibold text-foreground mb-1">Dining Out</h3>
            <p className="text-sm text-muted-foreground">Promote with exclusive deals</p>
          </div>
          <div className="bg-card/50 backdrop-blur p-5 rounded-xl border border-border/50 hover:border-primary/50 transition-colors">
            <div className="text-3xl mb-2"></div>
            <h3 className="font-semibold text-foreground mb-1">Business Tools</h3>
            <p className="text-sm text-muted-foreground">Analytics & Hyperpure supply</p>
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
          Click to start a voice conversation with our AI representative
        </p>
      </section>
    </div>
  );
};
