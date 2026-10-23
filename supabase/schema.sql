-- =====================================================================
-- SkillNavora: student and admin logins (Supabase)
-- Run this once in Supabase: SQL Editor -> New query -> paste -> Run.
-- It is safe to run again; it only creates what's missing.
--
-- Security model
--   * Every table has row level security (RLS) turned on.
--   * Students can only read and change their own rows.
--   * Admins (profiles.role = 'admin') can read everything and review work.
--   * Students can't make themselves admin: the role column can't be
--     updated directly, only through set_role(), which only admins can use.
-- =====================================================================

-- ---------- Profiles: one row per user, created automatically ----------
create table if not exists public.profiles (
  id          uuid primary key references auth.users (id) on delete cascade,
  email       text,
  full_name   text,
  phone       text,
  linkedin    text,
  goal        text,
  role        text not null default 'student' check (role in ('student', 'admin')),
  created_at  timestamptz not null default now()
);

create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email, full_name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data ->> 'full_name', ''))
  on conflict (id) do nothing;
  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- True when the signed-in user is an admin. SECURITY DEFINER so policies
-- can call it without looping back through the profiles policies.
create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.profiles where id = auth.uid() and role = 'admin');
$$;

-- ---------- 12-week progress: one row per student per week ----------
create table if not exists public.progress (
  user_id     uuid not null references public.profiles (id) on delete cascade,
  week        int  not null check (week between 1 and 12),
  done        boolean not null default false,
  updated_at  timestamptz not null default now(),
  primary key (user_id, week)
);

-- ---------- Assignment submissions ----------
create table if not exists public.submissions (
  id           bigint generated always as identity primary key,
  user_id      uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  week         int  check (week between 1 and 12),
  title        text not null check (length(title) between 1 and 200),
  link         text not null check (link ~* '^https?://' and length(link) <= 1000),
  notes        text check (length(notes) <= 4000),
  status       text not null default 'submitted' check (status in ('submitted', 'reviewed', 'needs_changes')),
  feedback     text check (length(feedback) <= 8000),
  reviewed_at  timestamptz,
  created_at   timestamptz not null default now()
);

-- ---------- Session and help requests ----------
create table if not exists public.requests (
  id          bigint generated always as identity primary key,
  user_id     uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  topic       text not null check (length(topic) between 1 and 120),
  message     text not null check (length(message) between 1 and 4000),
  status      text not null default 'open' check (status in ('open', 'done')),
  created_at  timestamptz not null default now()
);

-- ---------- Announcements from admins to all students ----------
create table if not exists public.announcements (
  id          bigint generated always as identity primary key,
  title       text not null check (length(title) between 1 and 200),
  body        text not null check (length(body) between 1 and 8000),
  created_at  timestamptz not null default now()
);

-- ---------- Row level security ----------
alter table public.profiles      enable row level security;
alter table public.progress      enable row level security;
alter table public.submissions   enable row level security;
alter table public.requests      enable row level security;
alter table public.announcements enable row level security;

-- Visitors who aren't signed in get nothing.
revoke all on public.profiles, public.progress, public.submissions, public.requests, public.announcements from anon;

-- Signed-in users: only the columns they're allowed to touch.
revoke all on public.profiles, public.progress, public.submissions, public.requests, public.announcements from authenticated;
grant select on public.profiles to authenticated;
grant update (full_name, phone, linkedin, goal) on public.profiles to authenticated;
grant select, insert, update, delete on public.progress to authenticated;
grant select, delete on public.submissions to authenticated;
grant insert (week, title, link, notes) on public.submissions to authenticated;
grant update (status, feedback, reviewed_at) on public.submissions to authenticated;
grant select on public.requests to authenticated;
grant insert (topic, message) on public.requests to authenticated;
grant update (status) on public.requests to authenticated;
grant select, insert, delete on public.announcements to authenticated;

-- profiles
drop policy if exists "profiles: read own or admin" on public.profiles;
create policy "profiles: read own or admin" on public.profiles
  for select to authenticated using (id = auth.uid() or public.is_admin());
drop policy if exists "profiles: update own" on public.profiles;
create policy "profiles: update own" on public.profiles
  for update to authenticated using (id = auth.uid()) with check (id = auth.uid());

-- progress
drop policy if exists "progress: read own or admin" on public.progress;
create policy "progress: read own or admin" on public.progress
  for select to authenticated using (user_id = auth.uid() or public.is_admin());
drop policy if exists "progress: insert own" on public.progress;
create policy "progress: insert own" on public.progress
  for insert to authenticated with check (user_id = auth.uid());
drop policy if exists "progress: update own" on public.progress;
create policy "progress: update own" on public.progress
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
drop policy if exists "progress: delete own" on public.progress;
create policy "progress: delete own" on public.progress
  for delete to authenticated using (user_id = auth.uid());

-- submissions: students add and see their own; only admins review
drop policy if exists "submissions: read own or admin" on public.submissions;
create policy "submissions: read own or admin" on public.submissions
  for select to authenticated using (user_id = auth.uid() or public.is_admin());
drop policy if exists "submissions: insert own" on public.submissions;
create policy "submissions: insert own" on public.submissions
  for insert to authenticated with check (user_id = auth.uid());
drop policy if exists "submissions: admin review" on public.submissions;
create policy "submissions: admin review" on public.submissions
  for update to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists "submissions: delete own unreviewed" on public.submissions;
create policy "submissions: delete own unreviewed" on public.submissions
  for delete to authenticated using (user_id = auth.uid() and status = 'submitted');

-- requests
drop policy if exists "requests: read own or admin" on public.requests;
create policy "requests: read own or admin" on public.requests
  for select to authenticated using (user_id = auth.uid() or public.is_admin());
drop policy if exists "requests: insert own" on public.requests;
create policy "requests: insert own" on public.requests
  for insert to authenticated with check (user_id = auth.uid());
drop policy if exists "requests: admin update" on public.requests;
create policy "requests: admin update" on public.requests
  for update to authenticated using (public.is_admin()) with check (public.is_admin());

-- announcements
drop policy if exists "announcements: signed-in read" on public.announcements;
create policy "announcements: signed-in read" on public.announcements
  for select to authenticated using (true);
drop policy if exists "announcements: admin insert" on public.announcements;
create policy "announcements: admin insert" on public.announcements
  for insert to authenticated with check (public.is_admin());
drop policy if exists "announcements: admin delete" on public.announcements;
create policy "announcements: admin delete" on public.announcements
  for delete to authenticated using (public.is_admin());

-- ---------- Admin-only helpers ----------
-- Make someone an admin (or a student again) by email. Admins only.
create or replace function public.set_role(target_email text, new_role text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then
    raise exception 'Only admins can change roles';
  end if;
  if new_role not in ('student', 'admin') then
    raise exception 'Role must be student or admin';
  end if;
  if lower(target_email) = lower((select email from public.profiles where id = auth.uid())) and new_role <> 'admin' then
    raise exception 'You cannot remove your own admin access';
  end if;
  update public.profiles set role = new_role where lower(email) = lower(target_email);
  if not found then
    raise exception 'No account with that email. Ask them to sign up first.';
  end if;
end $$;

revoke execute on function public.set_role(text, text) from public, anon;
grant execute on function public.set_role(text, text) to authenticated;
revoke execute on function public.is_admin() from public, anon;
grant execute on function public.is_admin() to authenticated;
revoke execute on function public.handle_new_user() from public, anon, authenticated;

-- =====================================================================
-- FIRST ADMIN: after you sign up on the website with your own email,
-- run this once (change the email):
--
--   update public.profiles set role = 'admin' where email = 'varunebix@gmail.com';
--
-- After that, add other admins from the Admin page.
-- =====================================================================
