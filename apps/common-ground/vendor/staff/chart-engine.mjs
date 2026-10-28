// vendor/lfs/student/numerology.ts
var separators = /[ \-/\\]/;
function calcString(input, singleRound = false) {
  let total = 0;
  for (const character of input.toUpperCase()) {
    const code = character.charCodeAt(0);
    if (code >= 65 && code <= 90) total += code - 64;
    else if (code >= 48 && code <= 57) total += code - 48;
  }
  if (singleRound || total <= 9) return total;
  const reduced = total % 9;
  return reduced === 0 ? 9 : reduced;
}
function calcNumber(input, singleRound = false) {
  if (input <= 0) return 0;
  if (singleRound) {
    let remaining = Math.trunc(input);
    let total = 0;
    do {
      total += remaining % 10;
      remaining = Math.trunc(remaining / 10);
    } while (remaining > 0);
    return total;
  }
  const reduced = input % 9;
  return reduced === 0 ? 9 : reduced;
}
function full(input, length = 0) {
  let value = calcString(input, true).toString();
  let output = "";
  while (value.length > 1) {
    output += `${value}/`;
    value = calcString(value, true).toString();
  }
  output += value;
  if (length !== 0) {
    while (output.length > length) {
      output = output.replace(/^\/+/, "");
      if (output.length > length) {
        const slash = output.indexOf("/");
        output = slash >= 0 ? output.slice(slash) : "";
      }
    }
  }
  return output === "0" ? "" : output;
}
function multiFull(input, split = separators) {
  return input.split(split).map((part) => {
    const value = full(part, part.length);
    return value + " ".repeat(part.length - value.length);
  }).join(" ");
}
function hdc(input, returnType) {
  const vowels = /* @__PURE__ */ new Set(["A", "E", "I", "O", "U"]);
  let output = "";
  for (const character of input.toUpperCase()) {
    output += vowels.has(character) ? returnType === 3 ? calcString(character).toString() : character : " ";
  }
  if (returnType === 0 || returnType === 3) return output;
  if (returnType === 1) return full(output);
  return calcString(output).toString();
}
function letters(input) {
  let output = "";
  for (const character of input.toUpperCase()) {
    const code = character.charCodeAt(0);
    if (code >= 48 && code <= 57) output += character;
    else {
      const value = code - 64;
      output += value < 1 || value > 26 ? " " : calcNumber(value).toString();
    }
  }
  return output;
}
function countWords(input) {
  return input.split(separators).length;
}
function getWord(input, which) {
  const words = input.split(separators);
  return which <= words.length ? words[which - 1] ?? "" : "";
}
function pinCha(input, returnType) {
  if (countWords(input) !== 3) return "";
  const month = calcString(getWord(input, 2));
  const day = calcString(getWord(input, 1));
  const year = calcString(getWord(input, 3));
  const p1 = calcNumber(month + day);
  const p2 = calcNumber(day + year);
  const p3 = calcNumber(p1 + p2);
  const p4 = calcNumber(month + year);
  const c1 = Math.abs(month - day);
  const c2 = Math.abs(day - year);
  const c3 = Math.abs(c1 - c2);
  const c4 = Math.abs(month - year);
  const values = {
    P1: p1.toString(),
    P2: p2.toString(),
    P3: p3.toString(),
    P4: p4.toString(),
    C1: c1.toString(),
    C2: c2.toString(),
    C3: c3.toString(),
    C4: c4.toString(),
    PPP_P: `${p1}${p2}${p3}-${p4}`,
    CCC_C: `${c1}${c2}${c3}-${c4}`,
    PPPP: `${p1}${p2}${p3}${p4}`,
    CCCC: `${c1}${c2}${c3}${c4}`,
    PPPP_CCCC: `${p1}${p2}${p3}${p4}-${c1}${c2}${c3}${c4}`
  };
  return values[returnType];
}
function repeat(word) {
  let output = "";
  for (const character of word) output += character.repeat(calcString(character));
  return output;
}
function combine(inputA, inputB) {
  const length = Math.min(inputA.length, inputB.length);
  let output = "";
  for (let index = 0; index < length; index += 1) {
    const value = (calcString(inputA[index]) + calcString(inputB[index])) % 9;
    output += value === 0 ? "9" : value.toString();
  }
  return output;
}
function seasons(dob) {
  const transition = 36 - calcString(dob);
  return [
    `0 ~ ${transition}`,
    `${transition + 1} ~ ${transition + 9}`,
    `${transition + 10} ~ ${transition + 18}`,
    `${transition + 19} ~~`
  ];
}
function ageFinder(dob, currentYear = (/* @__PURE__ */ new Date()).getFullYear()) {
  return currentYear - Number.parseInt(getWord(dob, 3), 10);
}
var Report = class {
  fullName;
  dob;
  age;
  pmei;
  hdc;
  hdcTotal;
  birthForce;
  fullNameRepeated;
  fullLetters;
  fullLettersTotal;
  fullLettersTotalPart;
  seasons;
  names;
  pin;
  cha;
  ultimateGoal;
  constructor(name, dob, currentYear = (/* @__PURE__ */ new Date()).getFullYear()) {
    this.fullName = name;
    this.dob = dob;
    this.hdc = hdc(name, 3);
    this.fullLetters = letters(name);
    this.hdcTotal = full(this.hdc);
    this.fullLettersTotal = full(this.fullLetters);
    this.fullLettersTotalPart = multiFull(this.fullLetters);
    const occurrences = {
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 0,
      "8": 0,
      "9": 0
    };
    for (const character of this.fullLetters) {
      occurrences[character] = (occurrences[character] ?? 0) + 1;
    }
    this.pmei = [
      `${occurrences["4"]}   ${occurrences["5"]} = ${calcNumber(occurrences["4"] + occurrences["5"])}`,
      `${occurrences["1"]}   ${occurrences["8"]} = ${calcNumber(occurrences["1"] + occurrences["8"])}`,
      `${occurrences["2"]} ${occurrences["3"]} ${occurrences["6"]} = ${calcNumber(occurrences["2"] + occurrences["3"] + occurrences["6"])}`,
      `${occurrences["7"]}   ${occurrences["9"]} = ${calcNumber(occurrences["7"] + occurrences["9"])}`
    ];
    this.birthForce = `${multiFull(dob)} ${full(dob)}`;
    this.seasons = seasons(dob);
    this.names = [];
    this.fullNameRepeated = [];
    for (let index = 1; index <= countWords(name); index += 1) {
      const word = getWord(name, index);
      this.names.push(word);
      this.fullNameRepeated.push(repeat(word));
    }
    this.pin = pinCha(dob, "PPP_P");
    this.cha = pinCha(dob, "CCC_C");
    this.ultimateGoal = full(this.fullLetters + dob);
    this.age = ageFinder(dob, currentYear);
  }
  getEssence(start, length) {
    if (length < 0 || start < 0) throw new Error("Invalid essence range");
    const values = Array(length).fill(0);
    let outputStart = 0;
    let adjustedStart = start;
    if (adjustedStart === 0) {
      outputStart += 1;
      adjustedStart += 1;
    }
    for (const repeatedName of this.fullNameRepeated) {
      const digits = Array.from(repeatedName, (character) => calcString(character));
      let sourceIndex = adjustedStart - 1;
      for (let index = outputStart; index < length; index += 1) {
        values[index] += digits[sourceIndex % digits.length];
        sourceIndex += 1;
      }
    }
    return values.map((value) => calcNumber(value).toString()).join("");
  }
  getPersonalYear(start, length) {
    if (length < 0 || start < 0) throw new Error("Invalid personal year range");
    let value = calcNumber(calcString(this.dob) + start);
    let output = "";
    for (let index = 0; index < length; index += 1) {
      output += value;
      value += 1;
      if (value > 9) value = 1;
    }
    return output;
  }
  getCalendarYear(start, length) {
    if (length < 0 || start < 0) throw new Error("Invalid calendar year range");
    let value = calcNumber(calcString(getWord(this.dob, 3)) + start);
    let output = "";
    for (let index = 0; index < length; index += 1) {
      output += value;
      value += 1;
      if (value > 9) value = 1;
    }
    return output;
  }
  getYearSet(start, length) {
    if (length < 0 || start < 0) throw new Error("Invalid year range");
    const essence = this.getEssence(start, length);
    const personalYear = this.getPersonalYear(start, length);
    const calendarYear = this.getCalendarYear(start, length);
    const names = this.fullNameRepeated.map((repeatedName) => {
      const offset = start + (start !== 0 ? -1 : 0);
      let value = (start === 0 ? " " : "") + repeatedName.slice(offset % repeatedName.length);
      while (value.length <= length) value += repeatedName;
      return value.slice(0, length).toUpperCase();
    });
    let combined = combine(essence, personalYear);
    if (start === 0) combined = `/${combined.slice(1)}`;
    return { names, essence, personalYear, calendarYear, combined };
  }
  getMonthSet(offset) {
    if (offset < 0) throw new Error("Invalid month offset");
    const monthCycle = "123456789123";
    const essence = this.getEssence(offset, 1)[0].repeat(12);
    const personalYear = this.getPersonalYear(offset, 1)[0].repeat(12);
    const personalMonth = combine(personalYear, monthCycle);
    const personalMonthEssence = combine(personalMonth, essence);
    const combined = combine(personalMonthEssence, personalMonth);
    return { essence, personalYear, personalMonth, personalMonthEssence, combined };
  }
};
function normalizeName(name) {
  return name.trim().replace(/[ \-/\\]+/g, " ");
}

// vendor/lfs/core/lettrology-engine/letterValues.ts
/**
 * @license
 * Lettrology Forensic Science - Deterministic Calculation Engine
 * Rule: Two distinct letter-value concepts
 * A. Base / duration value: repeating 1-9 (A=1..I=9, J=1..R=9, S=1..Z=8)
 * B. Full alphabet position: A=1..Z=26
 */
var BASE_LETTER_VALUES = {
  A: 1,
  B: 2,
  C: 3,
  D: 4,
  E: 5,
  F: 6,
  G: 7,
  H: 8,
  I: 9,
  J: 1,
  K: 2,
  L: 3,
  M: 4,
  N: 5,
  O: 6,
  P: 7,
  Q: 8,
  R: 9,
  S: 1,
  T: 2,
  U: 3,
  V: 4,
  W: 5,
  X: 6,
  Y: 7,
  Z: 8
};
var ORDINAL_LETTER_VALUES = {
  A: 1,
  B: 2,
  C: 3,
  D: 4,
  E: 5,
  F: 6,
  G: 7,
  H: 8,
  I: 9,
  J: 10,
  K: 11,
  L: 12,
  M: 13,
  N: 14,
  O: 15,
  P: 16,
  Q: 17,
  R: 18,
  S: 19,
  T: 20,
  U: 21,
  V: 22,
  W: 23,
  X: 24,
  Y: 25,
  Z: 26
};
function cleanAlphaString(input) {
  return input.toUpperCase().replace(/[^A-Z]/g, "");
}
function splitNameParts(fullName) {
  return fullName.trim().toUpperCase().split(/\s+/).map(cleanAlphaString).filter((p) => p.length > 0);
}
function getBaseLetterValue(char) {
  const c = char.toUpperCase();
  return BASE_LETTER_VALUES[c] || 0;
}
function getOrdinalLetterValue(char) {
  const c = char.toUpperCase();
  return ORDINAL_LETTER_VALUES[c] || 0;
}

// vendor/lfs/core/lettrology-engine/compoundTrail.ts
/**
 * @license
 * Lettrology Forensic Science - Deterministic Calculation Engine
 * Rule: All important compound trails must be preserved.
 * Canonical Power Numbers in core: 11, 13, 16.
 * Never reconstruct a Power Number from a final root.
 */
function reduceWithTrail(num, options) {
  const cleanNum = Math.abs(Math.floor(num));
  if (cleanNum === 0) {
    return {
      raw: 0,
      trail: [0],
      root: 0,
      isPowerNumber: false,
      rawFormula: options?.rawFormula
    };
  }
  const trail = [cleanNum];
  let current = cleanNum;
  let detectedPower;
  if (cleanNum === 11 || cleanNum === 13 || cleanNum === 16) {
    detectedPower = cleanNum;
  }
  while (current > 9) {
    const digits = current.toString().split("").map(Number);
    const sum = digits.reduce((acc, d) => acc + d, 0);
    trail.push(sum);
    if (!detectedPower && (sum === 11 || sum === 13 || sum === 16)) {
      detectedPower = sum;
    }
    current = sum;
  }
  return {
    raw: cleanNum,
    trail,
    root: current,
    isPowerNumber: detectedPower !== void 0,
    powerNumber: detectedPower,
    rawFormula: options?.rawFormula
  };
}
function formatCompound(cv) {
  if (!cv || !cv.trail || cv.trail.length === 0) return "0";
  return cv.trail.join("/");
}

// vendor/lfs/core/lettrology-engine/timelineEngine.ts
/**
 * @license
 * Lettrology Forensic Science - Deterministic Calculation Engine
 * Section 11: Name Timeline / Letter-Duration Algorithm
 */
function buildWordCycle(word) {
  const cleanWord = cleanAlphaString(word);
  if (!cleanWord) {
    return {
      originalWord: word,
      cycleLength: 1,
      letterSpans: [{ letter: " ", duration: 1, startIndex: 0, endIndex: 0 }]
    };
  }
  const spans = [];
  let currentIndex = 0;
  for (let i = 0; i < cleanWord.length; i++) {
    const char = cleanWord[i];
    const duration = getBaseLetterValue(char);
    const startIndex = currentIndex;
    const endIndex = currentIndex + duration - 1;
    spans.push({
      letter: char,
      duration,
      startIndex,
      endIndex
    });
    currentIndex += duration;
  }
  return {
    originalWord: word,
    cycleLength: currentIndex,
    letterSpans: spans
  };
}
function getActiveLetterAtAge(cycle, age) {
  if (cycle.cycleLength === 0 || cycle.letterSpans.length === 0) return "";
  const pos = (age % cycle.cycleLength + cycle.cycleLength) % cycle.cycleLength;
  for (const span of cycle.letterSpans) {
    if (pos >= span.startIndex && pos <= span.endIndex) {
      return span.letter;
    }
  }
  return cycle.letterSpans[0].letter;
}
function buildPersonNameCycles(fullName) {
  const parts = splitNameParts(fullName);
  if (parts.length === 0) {
    const emptyCycle = buildWordCycle("");
    return {
      fullName,
      firstNameCycle: emptyCycle,
      middleNameCycles: [],
      surnameCycle: emptyCycle
    };
  }
  if (parts.length === 1) {
    return {
      fullName,
      firstNameCycle: buildWordCycle(parts[0]),
      middleNameCycles: [],
      surnameCycle: buildWordCycle("")
    };
  }
  const firstName = parts[0];
  const surname = parts[parts.length - 1];
  const middles = parts.slice(1, parts.length - 1);
  return {
    fullName,
    firstNameCycle: buildWordCycle(firstName),
    middleNameCycles: middles.map(buildWordCycle),
    surnameCycle: buildWordCycle(surname)
  };
}
function getActiveLettersAtAge(cycles, age) {
  const firstLetter = getActiveLetterAtAge(cycles.firstNameCycle, age);
  const middleLetters = cycles.middleNameCycles.map((c) => getActiveLetterAtAge(c, age));
  const surnameLetter = getActiveLetterAtAge(cycles.surnameCycle, age);
  const allActiveLetters = [firstLetter, ...middleLetters, surnameLetter].filter(
    (l) => l.trim().length > 0
  );
  return {
    firstLetter,
    middleLetters,
    surnameLetter,
    allActiveLetters
  };
}

// vendor/lfs/core/historicalDate.ts
function historicalYearToOrdinal(signedYear) {
  if (!Number.isFinite(signedYear) || signedYear === 0) {
    throw new Error("Historical year 0 does not exist.");
  }
  return signedYear > 0 ? signedYear - 1 : signedYear;
}
function ordinalToHistoricalYear(ordinal) {
  if (!Number.isFinite(ordinal)) throw new Error("Invalid historical ordinal.");
  return ordinal >= 0 ? ordinal + 1 : ordinal;
}
function addHistoricalYears(signedYear, delta) {
  return ordinalToHistoricalYear(historicalYearToOrdinal(signedYear) + Math.trunc(delta));
}
function historicalYearDifference(fromYear, toYear) {
  return historicalYearToOrdinal(toYear) - historicalYearToOrdinal(fromYear);
}
function previousHistoricalYear(year) {
  return addHistoricalYears(year, -1);
}
function formatHistoricalYear(signedYear) {
  if (!Number.isFinite(signedYear) || signedYear === 0) return "Invalid year";
  return `${Math.abs(Math.trunc(signedYear))} ${signedYear < 0 ? "BC" : "AD"}`;
}
function toSignedHistoricalYear(year, era) {
  const clean = Math.abs(Math.trunc(year));
  if (clean < 1) throw new Error("Historical years begin at 1.");
  return era === "BCE" ? -clean : clean;
}
function isLeapYear(year) {
  const y = Math.abs(Math.trunc(year));
  return y % 4 === 0 && (y % 100 !== 0 || y % 400 === 0);
}
function daysInHistoricalMonth(year, month) {
  if (month === 2) return isLeapYear(year) ? 29 : 28;
  return [4, 6, 9, 11].includes(month) ? 30 : 31;
}
function isValidHistoricalDate(year, month, day) {
  return Number.isInteger(year) && year >= 1 && year <= 9999 && Number.isInteger(month) && month >= 1 && month <= 12 && Number.isInteger(day) && day >= 1 && day <= daysInHistoricalMonth(year, month);
}
function parseHistoricalDate(value) {
  if (!value) return null;
  const normalized = value.trim().toUpperCase().replace(/\s+/g, " ");
  const prefixBce = /^(BC|BCE)\s/.test(normalized);
  const suffixBce = /\s(BC|BCE)$/.test(normalized);
  const era = prefixBce || suffixBce ? "BCE" : "CE";
  const datePart = normalized.replace(/^(BC|BCE|AD|CE)\s+/, "").replace(/\s+(BC|BCE|AD|CE)$/, "").trim();
  let year = 0;
  let month = 0;
  let day = 0;
  const dash = datePart.split("-");
  if (dash.length === 3) {
    if (dash[0].length >= 3) {
      year = Number.parseInt(dash[0], 10);
      month = Number.parseInt(dash[1], 10);
      day = Number.parseInt(dash[2], 10);
    } else {
      day = Number.parseInt(dash[0], 10);
      month = Number.parseInt(dash[1], 10);
      year = Number.parseInt(dash[2], 10);
    }
  } else {
    const slash = datePart.split("/");
    if (slash.length === 3) {
      const first = Number.parseInt(slash[0], 10);
      const second = Number.parseInt(slash[1], 10);
      year = Number.parseInt(slash[2], 10);
      if (first > 12) {
        day = first;
        month = second;
      } else {
        month = first;
        day = second;
      }
    }
  }
  if (!isValidHistoricalDate(year, month, day)) return null;
  return { year, month, day, era, signedYear: toSignedHistoricalYear(year, era) };
}

// vendor/lfs/core/lettrology-engine/annualEngine.ts
/**
 * @license
 * Lettrology Forensic Science - Deterministic Calculation Engine
 * Section 12: Essence (ESS)
 * Section 15: Calendar Year (CY)
 * Section 16: Personal Year (PY)
 * Section 17: Yearly Combiner (COM)
 * Section 18: Annual Time-Map
 * Section 21: Pattern Detection Engine - Canonical
 */
function parseDob(dobStr) {
  const parsed = parseHistoricalDate(dobStr);
  if (!parsed) {
    return { day: 1, month: 1, year: 1970, yearNumber: 1970, era: "CE" };
  }
  return {
    day: parsed.day,
    month: parsed.month,
    year: parsed.signedYear,
    yearNumber: parsed.year,
    era: parsed.era
  };
}
function calculateCalendarYear(year) {
  const digits = Math.abs(year).toString().split("").map(Number);
  const sum = digits.reduce((a, b) => a + b, 0);
  return reduceWithTrail(sum, {
    rawFormula: `CY ${formatHistoricalYear(year)} digits (${digits.join("+")}) = ${sum}`
  });
}
function calculatePersonalYear(birthDay, birthMonth, reducedCY) {
  const pyRaw = birthDay + birthMonth + reducedCY;
  return reduceWithTrail(pyRaw, {
    rawFormula: `Birth Day (${birthDay}) + Month (${birthMonth}) + reduced CY (${reducedCY}) = ${pyRaw}`
  });
}
function calculateEssence(activeLetters) {
  const ordinals = activeLetters.map((l) => ({ letter: l, value: getOrdinalLetterValue(l) }));
  const rawSum = ordinals.reduce((acc, o) => acc + o.value, 0);
  const formula = ordinals.map((o) => `${o.letter}(${o.value})`).join(" + ") + ` = ${rawSum}`;
  return {
    compound: reduceWithTrail(rawSum, { rawFormula: formula }),
    ordinals
  };
}
function calculateYearlyCombiner(essRaw, pyRaw) {
  const comRaw = essRaw + pyRaw;
  return reduceWithTrail(comRaw, {
    rawFormula: `ESS raw (${essRaw}) + PY raw (${pyRaw}) = ${comRaw}`
  });
}
function generateAnnualTimeMap(birthName, dobStr, startYearOrAge = 0, endYearOrAge = 100, rangeMode = "AUTO") {
  const dob = parseDob(dobStr);
  const cycles = buildPersonNameCycles(birthName);
  const states = [];
  let startYear;
  let endYear;
  const autoLooksLikeYear = startYearOrAge < 0 || endYearOrAge < 0 || startYearOrAge > 1800 || endYearOrAge > 1800;
  const useYears = rangeMode === "YEAR" || rangeMode === "AUTO" && autoLooksLikeYear;
  if (useYears) {
    startYear = startYearOrAge;
    endYear = endYearOrAge;
  } else {
    startYear = addHistoricalYears(dob.year, startYearOrAge);
    endYear = addHistoricalYears(dob.year, endYearOrAge);
  }
  if (startYear === 0 || endYear === 0) {
    throw new Error("Historical year 0 does not exist.");
  }
  const span = historicalYearDifference(startYear, endYear);
  if (span < 0) return states;
  for (let offset = 0; offset <= span; offset++) {
    const calendarYear = addHistoricalYears(startYear, offset);
    const elapsedYears = historicalYearDifference(dob.year, calendarYear);
    if (elapsedYears < 0) continue;
    let age;
    if (elapsedYears === 0) {
      age = 0;
    } else if (dob.month > 1) {
      age = Math.max(0, elapsedYears - 1);
    } else {
      age = elapsedYears;
    }
    const { firstLetter, middleLetters, surnameLetter, allActiveLetters } = getActiveLettersAtAge(cycles, age);
    const { compound: ess, ordinals } = calculateEssence(allActiveLetters);
    const cy = calculateCalendarYear(calendarYear);
    const py = calculatePersonalYear(dob.day, dob.month, cy.root);
    const com = calculateYearlyCombiner(ess.raw, py.raw);
    const isIntensified = ess.root === py.root;
    const powerNumbers = [];
    if (ess.isPowerNumber && ess.powerNumber) powerNumbers.push(ess.powerNumber);
    if (py.isPowerNumber && py.powerNumber && !powerNumbers.includes(py.powerNumber)) powerNumbers.push(py.powerNumber);
    if (com.isPowerNumber && com.powerNumber && !powerNumbers.includes(com.powerNumber)) powerNumbers.push(com.powerNumber);
    const previousYear = previousHistoricalYear(calendarYear);
    const prevCY = calculateCalendarYear(previousYear);
    const prevPY = calculatePersonalYear(dob.day, dob.month, prevCY.root);
    const isCycleReset = prevPY.root === 9 && py.root === 1;
    const nextAgeLetters = getActiveLettersAtAge(cycles, age + 1);
    const nextEss = calculateEssence(nextAgeLetters.allActiveLetters);
    const lapseCombinedRaw = py.raw + nextEss.compound.raw;
    const lapseCompound = reduceWithTrail(lapseCombinedRaw, {
      rawFormula: `Current PY raw (${py.raw}) + Next Age ESS raw (${nextEss.compound.raw}) = ${lapseCombinedRaw}`
    });
    states.push({
      age,
      calendarYear,
      firstLetter,
      middleLetters,
      surnameLetter,
      activeLetters: allActiveLetters,
      activeLetterOrdinals: ordinals,
      ess,
      cy,
      py,
      com,
      isIntensified,
      isPowerNumber: powerNumbers.length > 0,
      powerNumbers,
      isCycleReset,
      birthdayLapse: {
        nextAge: age + 1,
        nextEssRaw: nextEss.compound.raw,
        combinedRaw: lapseCombinedRaw,
        combinedCompound: lapseCompound,
        isPowerNumber: lapseCompound.isPowerNumber
      }
    });
  }
  return states;
}

// vendor/lfs/core/lettrology-engine/monthlyEngine.ts
/**
 * @license
 * Lettrology Forensic Science - Deterministic Calculation Engine
 * Section 19: Monthly Chart
 * Section 22: Month-End Crossover
 */
var CM_TABLE = {
  1: 1,
  2: 2,
  3: 3,
  4: 4,
  5: 5,
  6: 6,
  7: 7,
  8: 8,
  9: 9,
  10: 1,
  // 1+0 = 1
  11: 2,
  // 1+1 = 2
  12: 3
  // 1+2 = 3
};
var MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];
function getCalendarMonthReduced(month) {
  return CM_TABLE[month] || 1;
}
function calculatePersonalMonth(pyRoot, calendarMonth) {
  const cm = getCalendarMonthReduced(calendarMonth);
  const rawSum = pyRoot + cm;
  return reduceWithTrail(rawSum, {
    rawFormula: `PY root (${pyRoot}) + CM (${cm}) = ${rawSum}`
  });
}
function calculatePersonalMonthEssence(essRoot, pm) {
  const pmActive = pm.isPowerNumber ? pm.raw : pm.root;
  const rawSum = essRoot + pmActive;
  return reduceWithTrail(rawSum, {
    rawFormula: `ESS root (${essRoot}) + PM active (${pmActive}) = ${rawSum}`
  });
}
function calculateMonthlyCombiner(pme, pm) {
  const carryPme = pme.raw === 11 || pme.raw === 22 || pme.raw === 33 ? pme.raw : pme.root;
  const carryPm = pm.isPowerNumber ? pm.raw : pm.root;
  const mcomRaw = carryPme + carryPm;
  return reduceWithTrail(mcomRaw, {
    rawFormula: `PME active (${carryPme}) + PM active (${carryPm}) = ${mcomRaw}`
  });
}
function generateMonthlyCalendar(annualState, nextAnnualState) {
  const months = [];
  for (let m = 1; m <= 12; m++) {
    const cm = getCalendarMonthReduced(m);
    const pm = calculatePersonalMonth(annualState.py.root, m);
    const pme = calculatePersonalMonthEssence(annualState.ess.root, pm);
    const mcom = calculateMonthlyCombiner(pme, pm);
    const powerNumbers = [];
    if (pm.isPowerNumber && pm.powerNumber) powerNumbers.push(pm.powerNumber);
    if (pme.isPowerNumber && pme.powerNumber && !powerNumbers.includes(pme.powerNumber)) {
      powerNumbers.push(pme.powerNumber);
    }
    if (mcom.isPowerNumber && mcom.powerNumber && !powerNumbers.includes(mcom.powerNumber)) {
      powerNumbers.push(mcom.powerNumber);
    }
    months.push({
      monthIndex: m,
      monthName: MONTH_NAMES[m - 1],
      year: annualState.calendarYear,
      cm,
      py: annualState.py,
      pm,
      ess: annualState.ess,
      pme,
      mcom,
      isPowerMonth: powerNumbers.length > 0,
      powerNumbers
    });
  }
  for (let i = 0; i < 12; i++) {
    const current = months[i];
    let nextPme;
    let nextMonthName;
    if (i < 11) {
      nextPme = months[i + 1].pme;
      nextMonthName = months[i + 1].monthName;
    } else {
      if (nextAnnualState) {
        const janPm = calculatePersonalMonth(nextAnnualState.py.root, 1);
        nextPme = calculatePersonalMonthEssence(nextAnnualState.ess.root, janPm);
        nextMonthName = `Jan ${nextAnnualState.calendarYear}`;
      } else {
        nextPme = months[0].pme;
        nextMonthName = "January";
      }
    }
    const currentPmRaw = current.pm.isPowerNumber ? current.pm.raw : current.pm.root;
    const nextPmeRaw = nextPme.isPowerNumber ? nextPme.raw : nextPme.root;
    const crossoverSum = currentPmRaw + nextPmeRaw;
    const crossoverCompound = reduceWithTrail(crossoverSum, {
      rawFormula: `Current PM (${currentPmRaw}) + Next Month PME (${nextPmeRaw}) = ${crossoverSum}`
    });
    current.crossover = {
      nextMonthName,
      currentPmRaw,
      nextPmeRaw,
      combinedCompound: crossoverCompound,
      isPowerNumber: crossoverCompound.isPowerNumber
    };
  }
  return months;
}

// pmei.js
var PMEI_PLANES = ["physical", "mental", "emotional", "intuitive"];
var planeForValue = [
  null,
  "mental",
  "emotional",
  "emotional",
  "physical",
  "physical",
  "emotional",
  "intuitive",
  "mental",
  "intuitive"
];
function calculatePMEI(fullBirthName = "") {
  const letters2 = fullBirthName.match(/[a-z]/gi) || [];
  const counts = { physical: 0, mental: 0, emotional: 0, intuitive: 0 };
  for (const letter of letters2) {
    const value = (letter.toUpperCase().charCodeAt(0) - 65) % 9 + 1;
    counts[planeForValue[value]]++;
  }
  const totalLetters = letters2.length;
  if (PMEI_PLANES.reduce((sum, plane) => sum + counts[plane], 0) !== totalLetters) {
    throw new Error("Each name letter must belong to exactly one PMEI plane.");
  }
  return Object.fromEntries([
    ...PMEI_PLANES.map((plane) => [plane, {
      count: counts[plane],
      percentage: totalLetters ? counts[plane] / totalLetters * 100 : 0
    }]),
    ["totalLetters", totalLetters]
  ]);
}

// engine-adapter.ts
function validatedIdentity(person) {
  if (person.NeedsReview) throw new Error("Verify the listed name and birthdate in this person\u2019s details before calculating their chart.");
  const name = normalizeName(person.FullName || "").trim().toUpperCase();
  if (!name || !/^[A-Z ]+$/.test(name)) throw new Error("Enter a full birth name using A\u2013Z letters to calculate this chart.");
  const value = (person.txtBirthdate || "").replaceAll("-", "/");
  if (!/^\d{2}\/\d{2}\/\d{4}$/.test(value)) throw new Error("Add a birthdate in DD-MM-YYYY format to calculate this chart.");
  const [day, month, year] = value.split("/").map(Number);
  const date = new Date(year, month - 1, day);
  if (year < 1e3 || date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day || date > /* @__PURE__ */ new Date()) throw new Error("Enter a valid birthdate that is not in the future.");
  return { name, dob: value, day, month, year };
}
function buildCompatibilityIdentity(person) {
  if (person.NeedsReview) return { id: person.id, positions: { first: null, called: null, whole: null, heart: null, day: null, birth: null, goal: null } };
  const name = (value2) => {
    const normalized = normalizeName(value2 || "").toUpperCase();
    return normalized && /^[A-Z ]+$/.test(normalized) ? normalized : null;
  };
  const whole = name(person.FullName || ""), called = name(person.CalledName || "");
  const first = person.FirstName ? name(person.FirstName) : whole ? getWord(whole, 1) : null;
  const value = (source, vowel = false) => {
    if (!source) return null;
    const raw = calcString(vowel ? hdc(source, 3) : letters(source), true);
    return raw ? { ...reduceWithTrail(raw), source } : null;
  };
  const wholeValue = value(whole);
  let dob = null;
  try {
    dob = validatedIdentity({ ...person, FullName: whole || "A" });
  } catch {
  }
  const dateValue = dob ? { ...reduceWithTrail(calcString(dob.dob, true)), source: dob.dob } : null;
  return { id: person.id, positions: { first: value(first), called: value(called), whole: wholeValue, heart: value(whole, true), day: dob ? { ...reduceWithTrail(dob.day), source: String(dob.day) } : null, birth: dateValue, goal: wholeValue && dateValue ? { ...reduceWithTrail(wholeValue.raw + dateValue.raw), source: `${whole} / ${dateValue.source}` } : null } };
}
function buildPersonChart(person, focusYear = (/* @__PURE__ */ new Date()).getFullYear(), span = 12) {
  const identity = validatedIdentity(person);
  if (!Number.isInteger(focusYear) || focusYear < identity.year || focusYear > identity.year + 254) throw new Error("Choose a chart year within 254 years of birth.");
  const report = new Report(identity.name, identity.dob, focusYear);
  const first = Math.max(identity.year, focusYear - span), last = Math.min(identity.year + 254, focusYear + span);
  const coreDob = `${identity.year}-${String(identity.month).padStart(2, "0")}-${String(identity.day).padStart(2, "0")}`;
  const annual = generateAnnualTimeMap(identity.name, coreDob, first, last + 1, "YEAR");
  const years = annual.slice(0, -1).map((state, index) => ({ ...state, months: generateMonthlyCalendar(state, annual[index + 1]) }));
  const pmei = calculatePMEI(person.FullName || "");
  const weights = PMEI_PLANES.map((plane) => pmei[plane].count);
  return { identity, report, years, focus: years.find((y) => y.calendarYear === focusYear), pmei, weights };
}
function buildTimelineChart(person, focusYear = (/* @__PURE__ */ new Date()).getFullYear()) {
  const calc = buildPersonChart(person, focusYear, 0);
  const { identity, report } = calc;
  const focusAge = focusYear - identity.year;
  const start = Math.max(0, focusAge - 14), extendedStart = Math.max(0, focusAge - 40);
  const first = Math.max(0, Math.min(start, extendedStart, focusAge - 1));
  const last = Math.max(start + 29, extendedStart + 79, focusAge + 2);
  const dob = `${identity.year}-${String(identity.month).padStart(2, "0")}-${String(identity.day).padStart(2, "0")}`;
  const annual = generateAnnualTimeMap(identity.name, dob, identity.year + first, identity.year + last + 1, "YEAR");
  const stateFor = (year) => annual.find((state) => state.calendarYear === year);
  const section = (offset, length) => ({
    start: offset,
    length,
    names: report.getYearSet(offset, length).names,
    states: Array.from({ length }, (_, i) => stateFor(identity.year + offset + i))
  });
  const monthly = [focusYear - 1, focusYear, focusYear + 1].map((year) => {
    const state = stateFor(year);
    return { year, age: year - identity.year, months: state ? generateMonthlyCalendar(state, stateFor(year + 1)) : [] };
  });
  return { ...calc, focusAge, yearly: section(start, 30), extended: section(extendedStart, 80), monthly };
}
export {
  buildCompatibilityIdentity,
  buildPersonChart,
  buildTimelineChart,
  calculateCalendarYear,
  calculateEssence,
  calculateMonthlyCombiner,
  calculatePersonalMonth,
  calculatePersonalMonthEssence,
  calculatePersonalYear,
  formatCompound,
  reduceWithTrail,
  validatedIdentity
};
