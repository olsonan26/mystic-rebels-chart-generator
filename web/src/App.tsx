import { useEffect, useRef, useState } from "react";
import {
  ArrowDownToLine,
  ChevronDown,
  ChevronRight,
  FolderOpen,
  Maximize2,
  Minus,
  Plus,
  RotateCcw,
  Search,
  SlidersHorizontal,
  Sparkles,
  X,
  Check,
  LoaderCircle,
  Upload,
} from "lucide-react";
import type { BirthInput, Chart, Location, ObjectEntry, Point } from "./types";
import { Wheel } from "./Wheel";
import { LegacyWheel } from "./LegacyWheel";
import { matchesPoint, type Density, type Orientation } from "./wheelLayout";
import { formatPosition } from "./geometry";
import { initializeStorage } from "./storage";
import Account from "./Account";

const EXAMPLE: BirthInput = {
  name: "Example chart",
  local_date: "1992-07-17",
  local_time: "20:01:00",
  timezone: "America/Los_Angeles",
  fold: null,
  latitude: 33.803,
  longitude: -118.072,
  location_name: "Los Alamitos, California, United States",
  coordinate_provenance:
    "Illustrative reference coordinates; editable city-level location",
  time_accuracy: "nearest_minute",
  uncertainty_seconds: 30,
  objects: [
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
    "Ascendant",
    "Midheaven",
  ],
  chart_type: "natal",
};
function download(name: string, contents: string, type: string) {
  const url = URL.createObjectURL(new Blob([contents], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 500);
}
export default function App() {
  const [input, setInput] = useState<BirthInput>(EXAMPLE),
    [chart, setChart] = useState<Chart | null>(null),
    [catalog, setCatalog] = useState<ObjectEntry[]>([]),
    [presets, setPresets] = useState<Record<string, string[]>>({}),
    [chosen, setChosen] = useState(EXAMPLE.objects),
    [objectSearch, setObjectSearch] = useState(""),
    [locationQuery, setLocationQuery] = useState(""),
    [locations, setLocations] = useState<Location[]>([]),
    [busy, setBusy] = useState(false),
    [error, setError] = useState<{ code: string; message: string } | null>(
      null,
    ),
    [active, setActive] = useState<string | null>("Sun"),
    [dual, setDual] = useState(false),
    [wheelDesign, setWheelDesign] = useState<"compact" | "original">("compact"),
    [orientation, setOrientation] = useState<Orientation>("ascendant"),
    [labelDensity, setLabelDensity] = useState<Density>("balanced"),
    [wheelSearch, setWheelSearch] = useState(""),
    [zoom, setZoom] = useState(1),
    [precision, setPrecision] = useState<"degree" | "minute" | "second">(
      "second",
    ),
    [account, setAccount] = useState(false),
    [dirty, setDirty] = useState(false),
    [tableSearch, setTableSearch] = useState(""),
    [tableView, setTableView] = useState<"placements" | "astronomy">(
      "placements",
    ),
    [mobileObjects, setMobileObjects] = useState(false),
    [showDetails, setShowDetails] = useState(false),
    [status, setStatus] = useState("");
  const requestSeq = useRef(0),
    chartFrame = useRef<HTMLDivElement>(null),
    importRef = useRef<HTMLInputElement>(null);
  async function compute(
    birth: BirthInput,
    objects: string[],
    resetDirty = true,
  ): Promise<Chart | undefined> {
    const seq = ++requestSeq.current;
    setBusy(true);
    setError(null);
    try {
      const response = await fetch("/api/charts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...birth, objects }),
      });
      const result = await response.json();
      if (seq !== requestSeq.current) return;
      if (!response.ok)
        throw (
          result.error ?? {
            code: "INVALID_INPUT",
            message:
              result.detail?.[0]?.msg ??
              "Check the birth details and try again.",
          }
        );
      setChart(result);
      if (resetDirty) setDirty(false);
      setStatus(
        `${result.points.filter((p: Point) => p.available).length} objects calculated.`,
      );
      return result as Chart;
    } catch (e) {
      if (seq === requestSeq.current)
        setError(
          typeof e === "object" && e !== null && "message" in e
            ? (e as { code: string; message: string })
            : {
                code: "CONNECTION_ERROR",
                message: "The chart service could not be reached. Try again.",
              },
        );
    } finally {
      if (seq === requestSeq.current) setBusy(false);
    }
  }
  useEffect(() => {
    let live = true;
    fetch("/api/catalog")
      .then((r) => {
        if (!r.ok) throw new Error("Astronomical data is unavailable.");
        return r.json();
      })
      .then((data) => {
        if (live) {
          setCatalog(data.objects);
          setPresets(data.presets);
          void compute(EXAMPLE, EXAMPLE.objects);
        }
      })
      .catch((e) => {
        if (live)
          setError({ code: "INITIALIZATION_ERROR", message: e.message });
      });
    initializeStorage().catch(() => {});
    return () => {
      live = false;
    };
  }, []);
  useEffect(() => {
    if (locationQuery.length < 2) {
      setLocations([]);
      return;
    }
    const controller = new AbortController();
    const timer = setTimeout(() => {
      fetch(`/api/locations?q=${encodeURIComponent(locationQuery)}`, {
        signal: controller.signal,
      })
        .then((r) => r.json())
        .then(setLocations)
        .catch(() => {});
    }, 220);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [locationQuery]);
  function edit<K extends keyof BirthInput>(key: K, value: BirthInput[K]) {
    setInput((prev) => ({ ...prev, [key]: value }));
    setDirty(true);
  }
  function selection(next: string[]) {
    setChosen(next);
    void compute(chart?.input ?? input, next, !chart);
  }
  function showObjects() {
    setMobileObjects(true);
    requestAnimationFrame(() =>
      document
        .getElementById("object-panel")
        ?.scrollIntoView({ block: "start" }),
    );
  }
  function showChart() {
    setMobileObjects(false);
    requestAnimationFrame(() =>
      document
        .querySelector(".chart-panel")
        ?.scrollIntoView({ block: "start" }),
    );
  }
  const selected = chart?.points.find((p) => p.id === active && p.available);
  const available = chart?.points.filter((p) => p.available) ?? [],
    unavailable = chart?.points.filter((p) => !p.available) ?? [];
  const groups = [...new Set(catalog.map((o) => o.group))];
  async function loadChart(value: Chart) {
    if (
      value.product !== "Mystic Rebels" ||
      !Array.isArray(value.points) ||
      !value.input ||
      !Array.isArray(value.input.objects) ||
      !value.input.objects.every((id) => typeof id === "string") ||
      value.points.some(
        (p) =>
          p.available &&
          (!Number.isFinite(p.longitude_deg) || typeof p.id !== "string"),
      )
    )
      throw new Error("This file is not a valid Mystic Rebels chart.");
    const verified = await compute(value.input, value.input.objects);
    if (verified) {
      setInput(verified.input);
      setChosen(verified.input.objects);
    }
  }
  function svgExport() {
    const svg = document.getElementById("chart-wheel");
    if (!svg || !chart) return;
    const clone = svg.cloneNode(true) as SVGElement;
    const source = document.querySelectorAll(
      "#chart-wheel text, #chart-wheel tspan",
    );
    clone.querySelectorAll("text, tspan").forEach((node, i) => {
      const style = getComputedStyle(source[i]);
      for (const property of [
        "font-family",
        "font-size",
        "font-weight",
        "fill",
        "stroke",
        "stroke-width",
        "paint-order",
        "stroke-linejoin",
        "font-variant-numeric",
        "letter-spacing",
      ])
        node.setAttribute(property, style.getPropertyValue(property));
    });
    download(
      "mystic-rebels-chart.svg",
      new XMLSerializer().serializeToString(clone),
      "image/svg+xml",
    );
  }
  return (
    <>
      <header className="topbar">
        <a
          className="brand"
          href="https://mysticrebels.com/"
          aria-label="Mystic Rebels home"
        >
          <img src="/mystic-rebels.avif" alt="Mystic Rebels" />
        </a>
        <span className="brand-divider" />
        <span className="app-name">Chart generator</span>
        <nav>
          <button
            className="nav-current"
            onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          >
            Create a chart
          </button>
          <button onClick={() => setAccount(true)}>
            <FolderOpen size={16} /> Saved charts
          </button>
        </nav>
      </header>
      <main>
        <div className="page-heading">
          <div>
            <h1>Your chart. Every detail.</h1>
            <p>Create, customize, and explore your Alchemystic Astrology chart.</p>
          </div>
          <button
            className="subtle"
            onClick={() => {
              setInput(EXAMPLE);
              setChosen(EXAMPLE.objects);
              void compute(EXAMPLE, EXAMPLE.objects);
            }}
          >
            <RotateCcw size={15} /> Load example
          </button>
        </div>
        <div className="workspace">
          <aside className="sidebar">
            <section className="panel birth-panel">
              <h2>
                <span className="section-icon">
                  <Sparkles size={17} />
                </span>{" "}
                Birth details
              </h2>
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  void compute(input, chosen).then((result) => {
                    if (
                      result &&
                      window.matchMedia("(max-width:760px)").matches
                    )
                      showChart();
                  });
                }}
              >
                <label>
                  Chart name
                  <input
                    value={input.name}
                    onChange={(e) => edit("name", e.target.value)}
                    maxLength={120}
                    required
                  />
                </label>
                <div className="two-cols">
                  <label>
                    Birth date
                    <input
                      type="date"
                      min="1800-01-01"
                      max="2399-12-31"
                      value={input.local_date}
                      onChange={(e) => edit("local_date", e.target.value)}
                      required
                    />
                  </label>
                  <label>
                    Birth time
                    <input
                      type="time"
                      step="1"
                      disabled={input.time_accuracy === "unknown"}
                      value={input.local_time ?? ""}
                      onChange={(e) => edit("local_time", e.target.value)}
                      required={input.time_accuracy !== "unknown"}
                    />
                  </label>
                </div>
                <label>
                  Time accuracy
                  <select
                    value={input.time_accuracy}
                    onChange={(e) => {
                      const accuracy = e.target
                        .value as BirthInput["time_accuracy"];
                      setInput((p) => ({
                        ...p,
                        time_accuracy: accuracy,
                        local_time:
                          accuracy === "unknown"
                            ? null
                            : (p.local_time ?? "12:00:00"),
                        uncertainty_seconds:
                          accuracy === "recorded_second"
                            ? 0.5
                            : accuracy === "nearest_minute"
                              ? 30
                              : accuracy === "approximate"
                                ? 900
                                : null,
                      }));
                      setDirty(true);
                    }}
                  >
                    <option value="recorded_second">
                      Recorded to the second
                    </option>
                    <option value="nearest_minute">Nearest minute</option>
                    <option value="approximate">Approximate time</option>
                    <option value="unknown">Time unknown</option>
                  </select>
                </label>
                {input.time_accuracy === "approximate" && (
                  <label>
                    Uncertainty in seconds
                    <input
                      type="number"
                      min="1"
                      max="86400"
                      value={input.uncertainty_seconds ?? 900}
                      onChange={(e) =>
                        edit("uncertainty_seconds", Number(e.target.value))
                      }
                    />
                  </label>
                )}
                <div className="location-field">
                  <label>
                    Birthplace
                    <div className="search-input">
                      <Search size={16} />
                      <input
                        aria-label="Search birthplace"
                        placeholder="Search a city or town"
                        value={locationQuery}
                        onChange={(e) => setLocationQuery(e.target.value)}
                        autoComplete="off"
                      />
                    </div>
                  </label>
                  {locations.length > 0 && (
                    <div
                      className="location-results"
                      role="listbox"
                      aria-label="Birthplace matches"
                    >
                      {locations.map((place) => (
                        <button
                          type="button"
                          key={place.id}
                          role="option"
                          aria-selected="false"
                          onClick={() => {
                            setInput((p) => ({
                              ...p,
                              latitude: place.latitude,
                              longitude: place.longitude,
                              timezone: place.timezone,
                              location_name: place.name,
                              coordinate_provenance: place.provenance,
                              fold: null,
                            }));
                            setLocationQuery("");
                            setLocations([]);
                            setDirty(true);
                          }}
                        >
                          {place.name}
                          <small>
                            {place.latitude}°, {place.longitude}°
                          </small>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                <p className="location-chosen">
                  <Check size={14} />
                  {input.location_name}
                </p>
                <details className="coordinate-details">
                  <summary>
                    Coordinates & time zone <ChevronDown size={14} />
                  </summary>
                  <p className="hint">
                    City locations use a city-center coordinate. Enter the
                    actual birth location here for greater precision.
                  </p>
                  <div className="two-cols">
                    <label>
                      Latitude
                      <input
                        type="number"
                        step="any"
                        min="-90"
                        max="90"
                        value={input.latitude}
                        onChange={(e) => {
                          edit("latitude", Number(e.target.value));
                          edit("coordinate_provenance", "user_entered");
                        }}
                        required
                      />
                    </label>
                    <label>
                      Longitude
                      <input
                        type="number"
                        step="any"
                        min="-180"
                        max="180"
                        value={input.longitude}
                        onChange={(e) => {
                          edit("longitude", Number(e.target.value));
                          edit("coordinate_provenance", "user_entered");
                        }}
                        required
                      />
                    </label>
                  </div>
                  <label>
                    IANA time zone
                    <input
                      value={input.timezone}
                      onChange={(e) => edit("timezone", e.target.value)}
                      required
                    />
                  </label>
                  <button
                    type="button"
                    className="text-button"
                    onClick={async () => {
                      try {
                        const r = await fetch(
                          `/api/timezone?latitude=${input.latitude}&longitude=${input.longitude}`,
                        );
                        if (!r.ok) throw new Error();
                        const d = await r.json();
                        edit("timezone", d.timezone);
                      } catch {
                        setError({
                          code: "LOCATION_NOT_RESOLVED",
                          message:
                            "The time zone could not be determined. Enter the IANA zone manually.",
                        });
                      }
                    }}
                  >
                    Find time zone from coordinates
                  </button>
                </details>
                {error?.code === "AMBIGUOUS_DST_FOLD" && (
                  <label>
                    Repeated clock time
                    <select
                      value={input.fold ?? ""}
                      onChange={(e) =>
                        edit("fold", Number(e.target.value) as 0 | 1)
                      }
                      required
                    >
                      <option value="">Choose occurrence</option>
                      <option value="0">First occurrence</option>
                      <option value="1">Second occurrence</option>
                    </select>
                  </label>
                )}
                <button
                  className="secondary mobile-object-toggle"
                  type="button"
                  onClick={showObjects}
                  aria-controls="object-panel"
                  aria-expanded={mobileObjects}
                >
                  <SlidersHorizontal size={16} /> Customize chart objects (
                  {chosen.length})
                </button>
                <button
                  className="primary generate"
                  disabled={busy || chosen.length === 0}
                >
                  {busy ? (
                    <LoaderCircle size={17} className="spin" />
                  ) : (
                    <Sparkles size={17} />
                  )}{" "}
                  {busy ? "Calculating…" : "Generate chart"}
                </button>
                {dirty && (
                  <p className="hint">
                    Birth details changed. Generate to update your chart.
                  </p>
                )}
              </form>
            </section>
            <section
              id="object-panel"
              className={
                "panel object-panel" + (mobileObjects ? " is-open" : "")
              }
            >
              <div className="section-title">
                <h2>
                  <SlidersHorizontal size={17} /> Chart objects
                </h2>
                <span>{chosen.length}</span>
              </div>
              <div className="segmented presets">
                {["Basic", "Expanded"].map((p) => (
                  <button
                    key={p}
                    className={
                      presets[p]?.join() === chosen.join() ? "selected" : ""
                    }
                    onClick={() => selection(presets[p] ?? chosen)}
                  >
                    {p}
                  </button>
                ))}
                <button
                  className={
                    !Object.values(presets).some(
                      (p) => p.join() === chosen.join(),
                    )
                      ? "selected"
                      : ""
                  }
                  onClick={() => setObjectSearch("")}
                >
                  Custom
                </button>
              </div>
              <div className="search-input">
                <Search size={15} />
                <input
                  aria-label="Search chart objects"
                  placeholder="Find an object"
                  value={objectSearch}
                  onChange={(e) => setObjectSearch(e.target.value)}
                />
              </div>
              <button
                className="text-button all-objects"
                disabled={catalog.length === 0}
                onClick={() =>
                  selection(catalog.filter((o) => o.available).map((o) => o.id))
                }
              >
                Select all available
              </button>
              <div className="object-groups">
                {groups.map((group) => {
                  const rows = catalog.filter(
                    (o) =>
                      o.group === group &&
                      `${o.name} ${o.id}`
                        .toLowerCase()
                        .includes(objectSearch.toLowerCase()),
                  );
                  return (
                    rows.length > 0 && (
                      <details
                        key={group}
                        open={
                          !!objectSearch ||
                          group === "Planets" ||
                          group === "Angles"
                        }
                      >
                        <summary>
                          {group}
                          <span>
                            {rows.filter((o) => chosen.includes(o.id)).length}/
                            {rows.length}
                          </span>
                        </summary>
                        {rows.map((o) => (
                          <label
                            className={
                              "object-choice" +
                              (!o.available ? " unavailable" : "")
                            }
                            key={o.id}
                            title={o.reason}
                          >
                            <input
                              type="checkbox"
                              checked={chosen.includes(o.id)}
                              disabled={!o.available}
                              onChange={(e) =>
                                selection(
                                  e.target.checked
                                    ? [...chosen, o.id]
                                    : chosen.filter((id) => id !== o.id),
                                )
                              }
                            />
                            <span className="object-glyph">{o.glyph}</span>
                            <span>
                              {o.name}
                              {!o.available && <small>{o.reason}</small>}
                            </span>
                          </label>
                        ))}
                      </details>
                    )
                  );
                })}
              </div>
              <p className="hint">
                Object selection updates the displayed chart.
              </p>
              <button
                className="primary mobile-object-done"
                onClick={showChart}
              >
                View chart
              </button>
            </section>
          </aside>
          <div className="results-column">
            <section className="chart-panel" aria-busy={busy}>
              <div className="chart-header">
                <div>
                  <span className="chart-label">Natal chart</span>
                  <h2>{chart?.input.name ?? "Your chart"}</h2>
                  <p>
                    {chart
                      ? `${chart.input.local_date} · ${chart.time.time_is_reference_only ? "Time unknown" : chart.input.local_time} · ${chart.input.location_name}`
                      : "Enter your birth details to get started."}
                  </p>
                </div>
                <div className="chart-actions">
                  <button
                    className="icon-button"
                    onClick={() => setAccount(true)}
                    aria-label="Open saved charts"
                  >
                    <FolderOpen size={19} />
                  </button>
                  <button
                    className="icon-button"
                    onClick={() => {
                      if (chart)
                        download(
                          "mystic-rebels-chart.json",
                          JSON.stringify(chart, null, 2),
                          "application/json",
                        );
                    }}
                    disabled={!chart}
                    aria-label="Export chart JSON"
                  >
                    <ArrowDownToLine size={19} />
                  </button>
                  <button
                    className="icon-button"
                    onClick={() => importRef.current?.click()}
                    aria-label="Import chart JSON"
                  >
                    <Upload size={18} />
                  </button>
                  <input
                    type="file"
                    accept="application/json,.json"
                    ref={importRef}
                    hidden
                    onChange={async (e) => {
                      const file = e.target.files?.[0];
                      if (!file) return;
                      try {
                        if (file.size > 2_000_000)
                          throw new Error("Chart file is too large.");
                        await loadChart(JSON.parse(await file.text()));
                      } catch (err) {
                        setError({
                          code: "INVALID_IMPORT",
                          message:
                            err instanceof Error
                              ? err.message
                              : "Unable to import chart.",
                        });
                      }
                      e.target.value = "";
                    }}
                  />
                </div>
              </div>
              <div className="chart-toolbar">
                <button
                  className="icon-button mobile-object-button"
                  onClick={showObjects}
                  aria-label="Customize chart objects"
                >
                  <SlidersHorizontal size={16} />
                </button>
                <div className="segmented">
                  <button
                    className={!dual ? "selected" : ""}
                    onClick={() => setDual(false)}
                  >
                    Natal wheel
                  </button>
                  <button
                    className={dual ? "selected" : ""}
                    onClick={() => setDual(true)}
                  >
                    Dual wheel
                  </button>
                </div>
                <label className="precision-label">
                  Precision
                  <select
                    aria-label="Display precision"
                    value={precision}
                    onChange={(e) =>
                      setPrecision(e.target.value as typeof precision)
                    }
                  >
                    <option value="degree">Degrees</option>
                    <option value="minute">Minutes</option>
                    <option value="second">Seconds</option>
                  </select>
                </label>
              </div>
              <div
                className="wheel-presentation-controls"
                aria-label="Wheel presentation"
              >
                <label>
                  Layout
                  <select
                    aria-label="Wheel layout"
                    value={wheelDesign}
                    onChange={(e) =>
                      setWheelDesign(e.target.value as typeof wheelDesign)
                    }
                  >
                    <option value="compact">Compact</option>
                    <option value="original">Original (rollback)</option>
                  </select>
                </label>
                <label>
                  Alignment
                  <select
                    aria-label="Wheel alignment"
                    value={
                      wheelDesign === "original" ? "ascendant" : orientation
                    }
                    disabled={
                      wheelDesign === "original" ||
                      chart?.angles.Ascendant === undefined
                    }
                    onChange={(e) =>
                      setOrientation(e.target.value as Orientation)
                    }
                  >
                    <option value="ascendant">Ascendant</option>
                    <option value="whole-sign">Whole Sign boundary</option>
                  </select>
                </label>
                <label>
                  Labels
                  <select
                    aria-label="Wheel label density"
                    value={labelDensity}
                    disabled={wheelDesign === "original"}
                    onChange={(e) => setLabelDensity(e.target.value as Density)}
                  >
                    <option value="sparse">Sparse</option>
                    <option value="balanced">Balanced</option>
                    <option value="detailed">Detailed</option>
                    <option value="all">All that fit</option>
                  </select>
                </label>
                <div className="wheel-find">
                  <div className="search-input">
                    <Search size={14} />
                    <input
                      aria-label="Find in wheel"
                      type="search"
                      placeholder="Find in this chart"
                      value={wheelSearch}
                      onChange={(e) => setWheelSearch(e.target.value)}
                    />
                  </div>
                  {wheelSearch.trim() && (
                    <div
                      className="wheel-search-results"
                      aria-label="Matching chart objects"
                    >
                      <p>
                        {
                          available.filter((p) =>
                            matchesPoint(
                              { ...p, longitude_deg: p.longitude_deg! },
                              wheelSearch,
                            ),
                          ).length
                        }{" "}
                        matches · all markers remain visible
                      </p>
                      {available
                        .filter((p) =>
                          matchesPoint(
                            { ...p, longitude_deg: p.longitude_deg! },
                            wheelSearch,
                          ),
                        )
                        .map((p) => (
                          <button
                            key={p.id}
                            onClick={() => {
                              setActive(p.id);
                              setWheelSearch("");
                            }}
                          >
                            <span>
                              {p.glyph} {p.name}
                            </span>
                            <small>
                              {formatPosition(p.longitude_deg!, precision)}
                            </small>
                          </button>
                        ))}
                    </div>
                  )}
                </div>
              </div>
              {error && (
                <div role="alert" className="error">
                  <div>
                    <strong>{error.code.replaceAll("_", " ")}</strong>
                    <p>{error.message}</p>
                  </div>
                  <button
                    className="icon-button"
                    onClick={() => setError(null)}
                    aria-label="Dismiss error"
                  >
                    <X size={16} />
                  </button>
                </div>
              )}
              <div className="wheel-layout">
                <div className="wheel-viewport" ref={chartFrame}>
                  <div
                    className="wheel-surface"
                    style={{ width: `${zoom * 100}%` }}
                  >
                    {chart ? (
                      wheelDesign === "original" ? (
                        <LegacyWheel
                          chart={chart}
                          dual={dual}
                          selected={active}
                          onSelect={setActive}
                          precision={precision}
                        />
                      ) : (
                        <Wheel
                          chart={chart}
                          dual={dual}
                          selected={active}
                          onSelect={setActive}
                          precision={precision}
                          orientation={orientation}
                          density={labelDensity}
                          query={wheelSearch}
                          zoom={zoom}
                        />
                      )
                    ) : (
                      <div className="empty-chart">
                        {busy ? (
                          <LoaderCircle className="spin" size={32} />
                        ) : (
                          <Sparkles size={32} />
                        )}
                        <p>
                          {busy
                            ? "Calculating your chart…"
                            : "Your chart will appear here."}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
                <div className="wheel-controls">
                  <button
                    onClick={() => setZoom((z) => Math.max(1, z - 0.25))}
                    aria-label="Zoom out"
                    disabled={zoom <= 1}
                  >
                    <Minus size={16} />
                  </button>
                  <span>{Math.round(zoom * 100)}%</span>
                  <button
                    onClick={() => setZoom((z) => Math.min(4, z + 0.25))}
                    aria-label="Zoom in"
                    disabled={zoom >= 4}
                  >
                    <Plus size={16} />
                  </button>
                  <button onClick={() => setZoom(1)} aria-label="Reset zoom">
                    <RotateCcw size={15} />
                  </button>
                  <button
                    onClick={() => {
                      if (!document.fullscreenElement)
                        void chartFrame.current?.requestFullscreen();
                      else void document.exitFullscreen();
                    }}
                    aria-label="Fullscreen chart"
                  >
                    <Maximize2 size={16} />
                  </button>
                </div>
              </div>
              <div className="chart-footer">
                <span>
                  <span className="status-dot" />
                  {available.length} objects displayed
                  {unavailable.length > 0
                    ? ` · ${unavailable.length} unavailable`
                    : ""}
                </span>
                <button
                  className="text-button"
                  onClick={svgExport}
                  disabled={!chart}
                >
                  <ArrowDownToLine size={14} /> Export SVG
                </button>
              </div>
              {wheelDesign === "compact" && (
                <p className="wheel-density-note">
                  Every calculated object has an exact marker. Labels prioritize
                  selection, search and major objects; crowded labels are
                  reduced, never positions.{" "}
                  {zoom >= 2
                    ? "Outer scale: 10′ subdivisions."
                    : "Outer scale: 1°; zoom to 200% for 10′ subdivisions."}
                </p>
              )}
            </section>
            {selected && (
              <section className="inspector panel" aria-live="polite">
                <div className="inspector-object">
                  <span>{selected.glyph}</span>
                  <div>
                    <h3>
                      {selected.name}
                      {selected.retrograde && <small> Retrograde</small>}
                    </h3>
                    <p data-inspector-longitude={selected.longitude_deg}>
                      {formatPosition(selected.longitude_deg!, precision)}
                    </p>
                  </div>
                </div>
                <div className="inspector-values">
                  {[
                    ["House", selected.house ?? "—"],
                    ["Field", selected.field ?? "—"],
                    ["Tone", selected.tone],
                    ["Pulse", selected.pulse],
                  ].map(([key, value]) => (
                    <div key={key}>
                      <small>{key}</small>
                      <strong>{value}</strong>
                    </div>
                  ))}
                </div>
              </section>
            )}
            {chart?.warnings.map((w) => (
              <p key={w.code} className="notice">
                {w.message}
              </p>
            ))}
            {unavailable.length > 0 && (
              <section className="unavailable-results">
                <h3>Unavailable objects</h3>
                {unavailable.map((p) => (
                  <p key={p.id}>
                    <strong>{p.name}:</strong> {p.error?.message}
                  </p>
                ))}
              </section>
            )}
            <section className="positions panel">
              <div className="positions-header">
                <div>
                  <h2>Planetary positions</h2>
                  <p>The exact positions behind your chart.</p>
                </div>
                <div className="search-input">
                  <Search size={15} />
                  <input
                    aria-label="Filter position table"
                    placeholder="Find a position"
                    value={tableSearch}
                    onChange={(e) => setTableSearch(e.target.value)}
                  />
                </div>
              </div>
              <div className="table-options">
                <div className="segmented">
                  <button
                    className={tableView === "placements" ? "selected" : ""}
                    onClick={() => setTableView("placements")}
                  >
                    Placements
                  </button>
                  <button
                    className={tableView === "astronomy" ? "selected" : ""}
                    onClick={() => setTableView("astronomy")}
                  >
                    Astronomical data
                  </button>
                </div>
              </div>
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th>Object</th>
                      <th>Position</th>
                      {(tableView === "placements"
                        ? ["House", "Field", "Tone", "Pulse"]
                        : [
                            "Latitude °",
                            "Declination °",
                            "Speed °/day",
                            "Distance AU",
                          ]
                      ).map((title) => (
                        <th key={title}>{title}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {available
                      .filter((p) =>
                        p.name
                          .toLowerCase()
                          .includes(tableSearch.toLowerCase()),
                      )
                      .map((p) => (
                        <tr
                          key={p.id}
                          className={active === p.id ? "active" : ""}
                          data-table-object={p.id}
                          data-longitude={p.longitude_deg}
                        >
                          <td>
                            <button onClick={() => setActive(p.id)}>
                              <span className="table-glyph">{p.glyph}</span>
                              {p.name}
                              {p.retrograde && <span className="rx">℞</span>}
                            </button>
                          </td>
                          <td>{formatPosition(p.longitude_deg!, precision)}</td>
                          {tableView === "placements" ? (
                            <>
                              <td>{p.house ?? "—"}</td>
                              <td>{p.field ?? "—"}</td>
                              <td>{p.tone}</td>
                              <td>{p.pulse}</td>
                            </>
                          ) : (
                            <>
                              {[
                                p.latitude_deg,
                                p.declination_deg,
                                p.speed_longitude_deg_per_day,
                                p.distance_au,
                              ].map((value, i) => (
                                <td
                                  key={i}
                                  title={
                                    value === undefined
                                      ? "Not applicable"
                                      : String(value)
                                  }
                                >
                                  {value === undefined ? "—" : value.toFixed(8)}
                                </td>
                              ))}
                            </>
                          )}
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </section>
            <section className="calculation-details">
              <button
                className="text-button"
                onClick={() => setShowDetails((v) => !v)}
              >
                {showDetails ? (
                  <ChevronDown size={15} />
                ) : (
                  <ChevronRight size={15} />
                )}{" "}
                Calculation details
              </button>
              {showDetails && chart && (
                <div>
                  <dl>
                    <dt>UTC</dt>
                    <dd>{chart.time.birth_utc}</dd>
                    <dt>Time uncertainty</dt>
                    <dd>
                      {chart.time.uncertainty_seconds === null
                        ? "Unknown"
                        : `±${chart.time.uncertainty_seconds} seconds`}
                    </dd>
                    <dt>Coordinates</dt>
                    <dd>
                      {chart.input.latitude}, {chart.input.longitude}
                    </dd>
                    <dt>Location</dt>
                    <dd>{chart.input.coordinate_provenance}</dd>
                    <dt>System</dt>
                    <dd>Tropical · Geocentric · Whole Sign</dd>
                    <dt>Ephemeris</dt>
                    <dd>
                      Swiss Ephemeris{" "}
                      {String(chart.configuration.swiss_version)}
                    </dd>
                  </dl>
                  <p>
                    Unrounded positions and reproducibility metadata are
                    included in the JSON export.
                  </p>
                  <button
                    className="text-button"
                    onClick={() => window.print()}
                  >
                    Print chart
                  </button>
                </div>
              )}
            </section>
          </div>
        </div>
      </main>
      <footer className="page-footer">
        <img src="/mystic-rebels.avif" alt="Mystic Rebels" />
        <p>Your sky. Your perspective.</p>
        <span>Alchemystic Astrology · Chart generator v0.1</span>
      </footer>
      <div className="sr-only" role="status" aria-live="polite">
        {status}
      </div>
      {account && (
        <Account
          chart={chart}
          onLoad={loadChart}
          onClose={() => setAccount(false)}
        />
      )}
    </>
  );
}
