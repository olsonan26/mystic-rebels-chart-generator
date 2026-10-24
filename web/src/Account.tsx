import { useEffect, useRef, useState } from "react";
import { X, LogOut, Save, FolderOpen } from "lucide-react";
import { supabase, initializeStorage } from "./storage";
import type { Chart } from "./types";
export default function Account({
  chart,
  onLoad,
  onClose,
}: {
  chart: Chart | null;
  onLoad: (chart: Chart) => void;
  onClose: () => void;
}) {
  const [email, setEmail] = useState(""),
    [password, setPassword] = useState(""),
    [user, setUser] = useState<string | null>(null),
    [message, setMessage] = useState(""),
    [busy, setBusy] = useState(false),
    [saved, setSaved] = useState<
      { id: string; name: string; chart: Chart; created_at: string }[]
    >([]);
  const dialogRef = useRef<HTMLElement>(null);
  const [storageReady, setStorageReady] = useState(false);
  async function refresh() {
    if (!supabase) return;
    const {
      data: { user },
    } = await supabase.auth.getUser();
    setUser(user?.email ?? null);
    if (user) {
      const { data, error } = await supabase
        .from("mystic_rebels_charts")
        .select("id,name,chart,created_at")
        .order("created_at", { ascending: false });
      if (error) setMessage(error.message);
      else setSaved(data ?? []);
    }
  }
  useEffect(() => {
    let mounted = true;
    initializeStorage()
      .then(refresh)
      .catch((error) => {
        if (mounted) setMessage(error.message);
      })
      .finally(() => {
        if (mounted) setStorageReady(true);
      });
    return () => {
      mounted = false;
    };
  }, []);
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    dialogRef.current?.querySelector<HTMLButtonElement>("button")?.focus();
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      if (event.key !== "Tab") return;
      const focusable = [
        ...(dialogRef.current?.querySelectorAll<HTMLElement>(
          "button:not(:disabled), input:not(:disabled), a[href]",
        ) ?? []),
      ];
      const first = focusable[0],
        last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last?.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first?.focus();
      }
    };
    document.addEventListener("keydown", handleKey);
    return () => {
      document.removeEventListener("keydown", handleKey);
      previous?.focus();
    };
  }, [onClose]);
  async function auth(signup: boolean) {
    if (!supabase) return;
    setBusy(true);
    setMessage("");
    const { error } = signup
      ? await supabase.auth.signUp({ email, password })
      : await supabase.auth.signInWithPassword({ email, password });
    setBusy(false);
    if (error) setMessage(error.message);
    else {
      setMessage(
        signup ? "Check your email to confirm your account." : "Signed in.",
      );
      await refresh();
    }
  }
  async function save() {
    if (!supabase || !chart) return;
    setBusy(true);
    const {
      data: { user },
    } = await supabase.auth.getUser();
    if (!user) {
      setMessage("Sign in to save your chart.");
      setBusy(false);
      return;
    }
    const { error } = await supabase.from("mystic_rebels_charts").insert({
      user_id: user.id,
      name: chart.input.name,
      chart,
      input_hash: chart.input_fingerprint,
    });
    setBusy(false);
    setMessage(error ? error.message : "Your chart is saved.");
    if (!error) await refresh();
  }
  return (
    <div
      className="modal-backdrop"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <section
        ref={dialogRef}
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="account-title"
      >
        <button
          className="icon-button close"
          onClick={onClose}
          aria-label="Close saved charts"
        >
          <X size={20} />
        </button>
        <h2 id="account-title">Your saved charts</h2>
        <p className="muted">
          Keep your charts together, wherever you sign in.
        </p>
        {!storageReady ? (
          <p role="status">Connecting to your account…</p>
        ) : !supabase ? (
          <p role="status">
            Cloud saving is being configured. You can export your chart now and
            import it again later.
          </p>
        ) : user ? (
          <>
            <div className="account-line">
              <span>{user}</span>
              <button
                className="text-button"
                onClick={async () => {
                  await supabase!.auth.signOut();
                  setSaved([]);
                  setUser(null);
                }}
              >
                <LogOut size={16} /> Sign out
              </button>
            </div>
            <button
              className="primary"
              disabled={!chart || busy}
              onClick={save}
            >
              <Save size={17} /> Save current chart
            </button>
            <div className="saved-list">
              {saved.length === 0 ? (
                <p className="muted">Your saved charts will appear here.</p>
              ) : (
                saved.map((s) => (
                  <button
                    key={s.id}
                    className="saved-row"
                    onClick={() => {
                      onLoad(s.chart);
                      onClose();
                    }}
                  >
                    <FolderOpen size={19} />
                    <span>
                      {s.name}
                      <small>
                        {new Date(s.created_at).toLocaleDateString()}
                      </small>
                    </span>
                  </button>
                ))
              )}
            </div>
          </>
        ) : (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void auth(false);
            }}
          >
            <label>
              Email
              <input
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
            <label>
              Password
              <input
                type="password"
                autoComplete="current-password"
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            <div className="button-row">
              <button className="primary" disabled={busy}>
                Sign in
              </button>
              <button
                className="secondary"
                type="button"
                disabled={busy}
                onClick={() => void auth(true)}
              >
                Create account
              </button>
            </div>
          </form>
        )}
        {message && (
          <p role="status" className="notice">
            {message}
          </p>
        )}
      </section>
    </div>
  );
}
