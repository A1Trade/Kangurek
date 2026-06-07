import Anthropic from "@anthropic-ai/sdk";

let client: Anthropic | null = null;

export function getClient(): Anthropic {
  if (!client) {
    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      throw new Error(
        "Brak ANTHROPIC_API_KEY w env. Utworz .env.local z kluczem od Anthropic."
      );
    }
    client = new Anthropic({ apiKey });
  }
  return client;
}

export const MODELS = {
  opus: "claude-opus-4-7",
  sonnet: "claude-sonnet-4-6",
  haiku: "claude-haiku-4-5-20251001",
} as const;

export type ModelName = keyof typeof MODELS;

/**
 * Wywoluje Claude i wyciaga JSON z odpowiedzi.
 * Wymusza format przez instrukcje w systemie (a nie przez tools - prosciej i taniej).
 */
export async function callJson<T>(opts: {
  model: ModelName;
  system: string;
  user: string;
  maxTokens?: number;
  temperature?: number;
}): Promise<T> {
  const c = getClient();
  const resp = await c.messages.create({
    model: MODELS[opts.model],
    max_tokens: opts.maxTokens ?? 8000,
    temperature: opts.temperature ?? 0.7,
    system: opts.system + "\n\nZAWSZE odpowiadaj WYLACZNIE poprawnym JSON-em, bez komentarzy, bez markdownu, bez bloku ```. Tylko surowy JSON.",
    messages: [{ role: "user", content: opts.user }],
  });
  const text = resp.content
    .filter((b) => b.type === "text")
    .map((b) => (b as { type: "text"; text: string }).text)
    .join("");
  return parseJsonLenient<T>(text);
}

export async function callText(opts: {
  model: ModelName;
  system: string;
  user: string;
  maxTokens?: number;
  temperature?: number;
}): Promise<string> {
  const c = getClient();
  const resp = await c.messages.create({
    model: MODELS[opts.model],
    max_tokens: opts.maxTokens ?? 4000,
    temperature: opts.temperature ?? 0.7,
    system: opts.system,
    messages: [{ role: "user", content: opts.user }],
  });
  return resp.content
    .filter((b) => b.type === "text")
    .map((b) => (b as { type: "text"; text: string }).text)
    .join("");
}

function parseJsonLenient<T>(raw: string): T {
  let s = raw.trim();
  if (s.startsWith("```")) {
    s = s.replace(/^```(?:json)?\s*/, "").replace(/```\s*$/, "");
  }
  const firstBrace = s.search(/[\[{]/);
  if (firstBrace > 0) s = s.slice(firstBrace);
  const lastBrace = Math.max(s.lastIndexOf("}"), s.lastIndexOf("]"));
  if (lastBrace > -1 && lastBrace < s.length - 1) s = s.slice(0, lastBrace + 1);
  try {
    return JSON.parse(s) as T;
  } catch (e) {
    throw new Error(`Model zwrocil nieparsowalny JSON: ${(e as Error).message}\n\nFragment:\n${s.slice(0, 500)}`);
  }
}
