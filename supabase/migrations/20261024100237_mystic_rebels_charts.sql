create table public.mystic_rebels_charts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null check (char_length(name) between 1 and 120),
  input_hash text not null check (input_hash ~ '^[0-9a-f]{64}$'),
  chart jsonb not null check (jsonb_typeof(chart) = 'object'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint chart_payload_size check (octet_length(chart::text) <= 1000000)
);
create index mystic_rebels_charts_user_created on public.mystic_rebels_charts(user_id,created_at desc);
alter table public.mystic_rebels_charts enable row level security;
revoke all on public.mystic_rebels_charts from anon;
grant select,insert,update,delete on public.mystic_rebels_charts to authenticated;
create policy "Read own Mystic Rebels charts" on public.mystic_rebels_charts for select to authenticated using ((select auth.uid()) = user_id);
create policy "Create own Mystic Rebels charts" on public.mystic_rebels_charts for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Update own Mystic Rebels charts" on public.mystic_rebels_charts for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "Delete own Mystic Rebels charts" on public.mystic_rebels_charts for delete to authenticated using ((select auth.uid()) = user_id);
