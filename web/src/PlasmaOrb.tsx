import { useState } from "react";

/** Decorative brand motion. It has no relationship to the calculated chart. */
export default function PlasmaOrb() {
  const [paused, setPaused] = useState(false);
  return (
    <div className={`plasma-accent${paused ? " is-paused" : ""}`}>
      <div className="plasma-orb" aria-hidden="true">
        <div className="plasma-halo" />
        <div className="plasma-globe">
          <div className="plasma-cloud plasma-cloud-one" />
          <div className="plasma-cloud plasma-cloud-two" />
          <svg className="plasma-filaments plasma-filaments-one" viewBox="0 0 120 120" fill="none">
            <path d="M60 60C49 48 69 36 53 25S30 10 28 5M60 60C78 52 70 37 87 30S102 17 110 13M60 60C50 77 68 80 51 96S43 109 45 117M60 60C43 65 29 47 20 62S4 72 1 69M60 60C76 73 84 63 94 79S106 91 118 92" />
            <path className="plasma-fine" d="M54 29L42 31L39 17M85 32L92 43L109 40M49 98L34 92L24 103M20 61L16 47L5 44M94 80L85 93L90 111" />
          </svg>
          <svg className="plasma-filaments plasma-filaments-two" viewBox="0 0 120 120" fill="none">
            <path d="M60 60C61 43 43 47 47 27S61 10 65 1M60 60C80 58 76 72 96 59S108 42 119 43M60 60C59 79 78 78 75 96S88 110 87 118M60 60C40 57 45 39 28 34S15 27 6 20M60 60C46 70 37 66 30 86S14 102 7 109" />
          </svg>
          <div className="plasma-nucleus" />
          <div className="plasma-glass" />
        </div>
      </div>
      <button
        type="button"
        className="plasma-motion-toggle"
        aria-label={paused ? "Play decorative plasma animation" : "Pause decorative plasma animation"}
        aria-pressed={paused}
        onClick={() => setPaused(value => !value)}
      >
        <svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true">
          {paused ? <path d="M5 3L12 8L5 13Z" fill="currentColor" /> : <path d="M5 4V12M11 4V12" stroke="currentColor" strokeWidth="2" />}
        </svg>
      </button>
    </div>
  );
}
