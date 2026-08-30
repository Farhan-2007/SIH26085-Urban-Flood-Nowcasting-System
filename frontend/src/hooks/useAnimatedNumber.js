import { useEffect, useRef, useState } from "react";

// Animates a numeric readout from its previous value to a new target
// whenever the target changes, using an eased requestAnimationFrame loop.
// This is what makes switching forecast steps feel like a live instrument
// updating rather than a page reloading static numbers.
export function useAnimatedNumber(target, duration = 550) {
  const [display, setDisplay] = useState(target);
  const fromRef = useRef(target);
  const rafRef = useRef(null);

  useEffect(() => {
    const from = fromRef.current;
    const to = target;

    if (from === to) {
      setDisplay(to);
      return undefined;
    }

    const start = performance.now();

    function tick(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      setDisplay(from + (to - from) * eased);

      if (progress < 1) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        fromRef.current = to;
      }
    }

    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [target, duration]);

  return display;
}
