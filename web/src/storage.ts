import { createClient, type SupabaseClient } from "@supabase/supabase-js";
export let supabase: SupabaseClient | null = null;
let initialization: Promise<SupabaseClient | null> | null = null;
export function initializeStorage() {
  return (initialization ??= initialize().catch((error) => {
    initialization = null;
    throw error;
  }));
}
async function initialize() {
  const response = await fetch("/api/config");
  if (!response.ok) throw new Error("Account configuration is unavailable.");
  const config = await response.json();
  if (config.supabase_url && config.supabase_publishable_key)
    supabase = createClient(
      config.supabase_url,
      config.supabase_publishable_key,
    );
  return supabase;
}
