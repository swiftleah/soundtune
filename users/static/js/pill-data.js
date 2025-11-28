//  ---- js object that maps the template ID to an array of pill labels ----

const pillOptions = {
  "content-genre": [
    "rap",
    "hiphop",
    "r&b",
    "metal",
    "rock",
    "reggae",
    "electronic",
    "jazz",
    "metal",
    "country",
    "latin",
  ],
  "content-mood": [
    "happy",
    "sad",
    "anxious",
    "chill",
    "energetic",
    "romantic",
    "angry",
    "tired",
    "excited",
    "moody",
    "peaceful",
  ],
  "content-activity": [
    "working out",
    "studying",
    "driving",
    "cooking",
    "cleaning",
    "relaxing",
    "gaming",
    "walking",
    "showering",
    "sleeping",
    "commuting",
  ],
};

// --- array checker ---
// --- check that array is of expected length + is real array ---
function validatePillOptions(expectedCount = 11) {
  Object.entries(pillOptions).forEach(([key, arr]) => {
    if (!Array.isArray(arr)) {
      console.warn(`pillOptions["${key}"] is not an array.`);
      return;
    }
    if (arr.length != expectedCount) {
      console.warn(
        `pillOptions["${key}"] has ${arr.length} items instead of ${expectedCount}.`
      );
    }
  });
}

validatePillOptions();
