-- =====================================================================
-- SkillNavora LMS: student and admin logins (Supabase)
-- Run this once in Supabase: SQL Editor -> New query -> paste -> Run.
-- Safe to run again; it only creates what's missing and refreshes rules.
--
-- Security model
--   * Row level security (RLS) is on for every table.
--   * Students read and change only their own rows.
--   * Course materials are visible only to students enrolled in that course.
--   * Admins (profiles.role = 'admin') see everything, enrol students,
--     add materials and events, and review work.
--   * Nobody can make themselves admin: the role column can only change
--     through set_role(), which only admins can call.
-- =====================================================================

-- ---------- Profiles ----------
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
  values (new.id, new.email, coalesce(new.raw_user_meta_data ->> 'full_name', new.raw_user_meta_data ->> 'name', ''))
  on conflict (id) do nothing;
  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.profiles where id = auth.uid() and role = 'admin');
$$;

-- ---------- Enrolments: which student is in which program ----------
-- course_id matches the id of a program in assets/config.js (e.g. 'ai-pm').
create table if not exists public.enrollments (
  user_id     uuid not null references public.profiles (id) on delete cascade,
  course_id   text not null check (course_id ~ '^[a-z0-9-]{1,40}$'),
  status      text not null default 'active' check (status in ('active', 'completed')),
  created_at  timestamptz not null default now(),
  primary key (user_id, course_id)
);

create or replace function public.is_enrolled(c text)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.enrollments where user_id = auth.uid() and course_id = c);
$$;

-- ---------- Progress: modules a student has completed ----------
create table if not exists public.course_progress (
  user_id     uuid not null references public.profiles (id) on delete cascade,
  course_id   text not null,
  module      int  not null check (module between 0 and 99),
  done        boolean not null default false,
  updated_at  timestamptz not null default now(),
  primary key (user_id, course_id, module)
);

-- ---------- Course materials: recordings, slides, readings ----------
create table if not exists public.materials (
  id          bigint generated always as identity primary key,
  course_id   text not null check (course_id ~ '^[a-z0-9-]{1,40}$'),
  module      int  not null check (module between 0 and 99),
  title       text not null check (length(title) between 1 and 200),
  url         text not null check (url ~* '^https?://' and length(url) <= 1000),
  kind        text not null default 'link' check (kind in ('recording', 'slides', 'reading', 'assignment', 'link')),
  created_at  timestamptz not null default now()
);

-- ---------- Submissions: assignments and challenges ----------
create table if not exists public.submissions (
  id           bigint generated always as identity primary key,
  user_id      uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  course_id    text check (course_id ~ '^[a-z0-9-]{1,40}$'),
  kind         text not null default 'assignment' check (kind in ('assignment', 'challenge')),
  item         text check (length(item) <= 60),
  title        text not null check (length(title) between 1 and 200),
  link         text not null check (link ~* '^https?://' and length(link) <= 1000),
  notes        text check (length(notes) <= 4000),
  status       text not null default 'submitted' check (status in ('submitted', 'reviewed', 'needs_changes')),
  feedback     text check (length(feedback) <= 8000),
  reviewed_at  timestamptz,
  created_at   timestamptz not null default now()
);

-- ---------- Events: live sessions, workshops, demo days ----------
create table if not exists public.events (
  id           bigint generated always as identity primary key,
  title        text not null check (length(title) between 1 and 200),
  description  text check (length(description) <= 4000),
  starts_at    timestamptz not null,
  ends_at      timestamptz,
  join_url     text check (join_url is null or (join_url ~* '^https?://' and length(join_url) <= 1000)),
  created_at   timestamptz not null default now()
);

create table if not exists public.event_registrations (
  user_id     uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  event_id    bigint not null references public.events (id) on delete cascade,
  rating      int check (rating between 1 and 5),
  feedback    text check (length(feedback) <= 2000),
  created_at  timestamptz not null default now(),
  primary key (user_id, event_id)
);

-- ---------- Quiz attempts (Quiz zone) ----------
create table if not exists public.quiz_attempts (
  id          bigint generated always as identity primary key,
  user_id     uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  quiz_id     text not null check (quiz_id ~ '^[a-z0-9-]{1,40}$'),
  score       int  not null check (score >= 0),
  total       int  not null check (total between 1 and 100 and score <= total),
  created_at  timestamptz not null default now()
);

-- ---------- Help and session requests ----------
create table if not exists public.requests (
  id          bigint generated always as identity primary key,
  user_id     uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  topic       text not null check (length(topic) between 1 and 120),
  message     text not null check (length(message) between 1 and 4000),
  status      text not null default 'open' check (status in ('open', 'done')),
  created_at  timestamptz not null default now()
);

-- ---------- Announcements ----------
create table if not exists public.announcements (
  id          bigint generated always as identity primary key,
  title       text not null check (length(title) between 1 and 200),
  body        text not null check (length(body) between 1 and 8000),
  created_at  timestamptz not null default now()
);

-- ---------- Turn on row level security ----------
alter table public.profiles            enable row level security;
alter table public.enrollments         enable row level security;
alter table public.course_progress     enable row level security;
alter table public.materials           enable row level security;
alter table public.submissions         enable row level security;
alter table public.events              enable row level security;
alter table public.event_registrations enable row level security;
alter table public.quiz_attempts       enable row level security;
alter table public.requests            enable row level security;
alter table public.announcements       enable row level security;

-- ---------- Table permissions (which columns each signed-in user may touch) ----------
revoke all on public.profiles, public.enrollments, public.course_progress, public.materials, public.submissions,
  public.events, public.event_registrations, public.quiz_attempts, public.requests, public.announcements from anon, authenticated;

grant select on public.profiles to authenticated;
grant update (full_name, phone, linkedin, goal) on public.profiles to authenticated;
grant select, insert, update, delete on public.enrollments to authenticated;
grant select, insert, update, delete on public.course_progress to authenticated;
grant select, insert, update, delete on public.materials to authenticated;
grant select, delete on public.submissions to authenticated;
grant insert (course_id, kind, item, title, link, notes) on public.submissions to authenticated;
grant update (status, feedback, reviewed_at) on public.submissions to authenticated;
grant select, insert, update, delete on public.events to authenticated;
grant select, delete on public.event_registrations to authenticated;
grant insert (event_id) on public.event_registrations to authenticated;
grant update (rating, feedback) on public.event_registrations to authenticated;
grant select on public.quiz_attempts to authenticated;
grant insert (quiz_id, score, total) on public.quiz_attempts to authenticated;
grant select on public.requests to authenticated;
grant insert (topic, message) on public.requests to authenticated;
grant update (status) on public.requests to authenticated;
grant select, insert, delete on public.announcements to authenticated;

-- ---------- Policies (which rows) ----------
do $$ declare r record; begin
  for r in select policyname, tablename from pg_policies where schemaname = 'public' and tablename in
    ('profiles','enrollments','course_progress','materials','submissions','events','event_registrations','quiz_attempts','requests','announcements')
  loop execute format('drop policy %I on public.%I', r.policyname, r.tablename); end loop;
end $$;

-- profiles
create policy "read own or admin"  on public.profiles for select to authenticated using (id = auth.uid() or public.is_admin());
create policy "update own"         on public.profiles for update to authenticated using (id = auth.uid()) with check (id = auth.uid());

-- enrollments: students see theirs; admins manage all
create policy "read own or admin"  on public.enrollments for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy "admin insert"       on public.enrollments for insert to authenticated with check (public.is_admin());
create policy "admin update"       on public.enrollments for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "admin delete"       on public.enrollments for delete to authenticated using (public.is_admin());

-- course_progress: only for courses you're enrolled in
create policy "read own or admin"  on public.course_progress for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy "insert own enrolled" on public.course_progress for insert to authenticated with check (user_id = auth.uid() and public.is_enrolled(course_id));
create policy "update own enrolled" on public.course_progress for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid() and public.is_enrolled(course_id));
create policy "delete own"         on public.course_progress for delete to authenticated using (user_id = auth.uid());

-- materials: enrolled students and admins can read; admins manage
create policy "enrolled or admin read" on public.materials for select to authenticated using (public.is_admin() or public.is_enrolled(course_id));
create policy "admin insert"       on public.materials for insert to authenticated with check (public.is_admin());
create policy "admin update"       on public.materials for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "admin delete"       on public.materials for delete to authenticated using (public.is_admin());

-- submissions: students add theirs (course work only if enrolled); admins review
create policy "read own or admin"  on public.submissions for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy "insert own"         on public.submissions for insert to authenticated with check (
  user_id = auth.uid() and (kind = 'challenge' or course_id is null or public.is_enrolled(course_id)));
create policy "admin review"       on public.submissions for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "delete own unreviewed" on public.submissions for delete to authenticated using (user_id = auth.uid() and status = 'submitted');

-- events: every signed-in user can see them; admins manage
create policy "signed-in read"     on public.events for select to authenticated using (true);
create policy "admin insert"       on public.events for insert to authenticated with check (public.is_admin());
create policy "admin update"       on public.events for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "admin delete"       on public.events for delete to authenticated using (public.is_admin());

-- event registrations: register yourself, rate it after; admins see all
create policy "read own or admin"  on public.event_registrations for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy "register self"      on public.event_registrations for insert to authenticated with check (user_id = auth.uid());
create policy "feedback own"       on public.event_registrations for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy "cancel own"         on public.event_registrations for delete to authenticated using (user_id = auth.uid());

-- quiz attempts
create policy "read own or admin"  on public.quiz_attempts for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy "insert own"         on public.quiz_attempts for insert to authenticated with check (user_id = auth.uid());

-- requests
create policy "read own or admin"  on public.requests for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy "insert own"         on public.requests for insert to authenticated with check (user_id = auth.uid());
create policy "admin update"       on public.requests for update to authenticated using (public.is_admin()) with check (public.is_admin());

-- announcements
create policy "signed-in read"     on public.announcements for select to authenticated using (true);
create policy "admin insert"       on public.announcements for insert to authenticated with check (public.is_admin());
create policy "admin delete"       on public.announcements for delete to authenticated using (public.is_admin());

-- ---------- Admin-only helpers ----------
create or replace function public.set_role(target_email text, new_role text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'Only admins can change roles'; end if;
  if new_role not in ('student', 'admin') then raise exception 'Role must be student or admin'; end if;
  if lower(target_email) = lower((select email from public.profiles where id = auth.uid())) and new_role <> 'admin' then
    raise exception 'You cannot remove your own admin access';
  end if;
  update public.profiles set role = new_role where lower(email) = lower(target_email);
  if not found then raise exception 'No account with that email. Ask them to sign up first.'; end if;
end $$;

-- Enrol a student by email. Admins only.
create or replace function public.enroll(target_email text, course text)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid;
begin
  if not public.is_admin() then raise exception 'Only admins can enrol students'; end if;
  select id into uid from public.profiles where lower(email) = lower(target_email);
  if uid is null then raise exception 'No account with that email. Ask them to sign up first.'; end if;
  insert into public.enrollments (user_id, course_id) values (uid, course)
    on conflict (user_id, course_id) do update set status = 'active';
end $$;

revoke execute on function public.set_role(text, text), public.enroll(text, text), public.is_admin(), public.is_enrolled(text) from public, anon;
grant execute on function public.set_role(text, text), public.enroll(text, text), public.is_admin(), public.is_enrolled(text) to authenticated;
revoke execute on function public.handle_new_user() from public, anon, authenticated;

-- =====================================================================
-- FIRST ADMIN: after you sign up on the website with your own email,
-- run this once (change the email if needed):
--
--   update public.profiles set role = 'admin' where email = 'varunebix@gmail.com';
--
-- After that, add other admins and enrol students from the Admin page.
-- =====================================================================
