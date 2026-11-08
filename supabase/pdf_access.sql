-- PDF and handbook access approvals (run once in Supabase: SQL editor -> New query -> Run).
-- Visitors sign in, request access, and the owner approves them in the admin panel (Applications -> Resource access).
-- Approved emails are listed here. Only admins can change the list; each person can read only their own row.

create table if not exists public.pdf_access (
  email       text primary key check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' and length(email) <= 200),
  name        text check (length(name) <= 120),
  approved_by text default (auth.jwt() ->> 'email') check (length(approved_by) <= 200),
  approved_at timestamptz not null default now()
);

alter table public.pdf_access enable row level security;

-- Each signed-in person can see only their own approval (lower-case email match).
drop policy if exists "own approval" on public.pdf_access;
create policy "own approval" on public.pdf_access
  for select to authenticated
  using (lower(email) = lower(auth.jwt() ->> 'email'));

-- Admins can add, change and remove approvals.
drop policy if exists "admins manage approvals" on public.pdf_access;
create policy "admins manage approvals" on public.pdf_access
  for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

grant select, insert, update, delete on public.pdf_access to authenticated;
-- anon (signed-out visitors) gets nothing from this table.
revoke all on public.pdf_access from anon;
