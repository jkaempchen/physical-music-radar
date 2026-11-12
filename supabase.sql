-- Einmalig im Supabase SQL Editor ausführen.
create extension if not exists pgcrypto;
create table if not exists public.articles (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  summary text not null default '',
  category text not null default 'Markt',
  manufacturer text not null default '',
  source text not null default '',
  url text not null unique,
  published_at timestamptz not null default now(),
  priority smallint not null default 3 check (priority between 1 and 3),
  created_at timestamptz not null default now()
);
create index if not exists articles_published_idx on public.articles (published_at desc);
create index if not exists articles_category_idx on public.articles (category);
alter table public.articles enable row level security;
-- MVP: News sind für ALLE Website-Besucher lesbar.
-- Ausschließlich für öffentlich verwertbare Nachrichten, KEINE internen/vertraulichen Informationen.
revoke all on public.articles from anon, authenticated;
grant select on public.articles to anon, authenticated;
drop policy if exists "Public articles readable" on public.articles;
create policy "Public articles readable" on public.articles for select to anon, authenticated using (true);
-- Schreiben erfolgt NUR serverseitig über einen Supabase Secret Key.
