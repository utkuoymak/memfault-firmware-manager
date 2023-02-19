create table if not exists public.projects
(
    id         serial
        primary key,
    name       varchar,
    created_at timestamp,
    updated_at timestamp
);

alter table public.projects
    owner to firmware;

create unique index if not exists ix_projects_name
    on public.projects (name);

create table if not exists public.memberships
(
    id         serial
        primary key,
    email      varchar,
    project_id integer
        references public.projects,
    created_at timestamp,
    updated_at timestamp
);

alter table public.memberships
    owner to firmware;

create unique index if not exists ix_memberships_email
    on public.memberships (email);

create table if not exists public.devices
(
    id               serial
        primary key,
    project_id       integer
        references public.projects,
    current_firmware varchar,
    created_at       timestamp,
    updated_at       timestamp
);

alter table public.devices
    owner to firmware;

create index if not exists ix_devices_current_firmware
    on public.devices (current_firmware);

create table if not exists public.membership_api_keys
(
    id         serial
        primary key,
    secret_key varchar,
    member_id  integer
        references public.memberships,
    created_at timestamp,
    updated_at timestamp
);

alter table public.membership_api_keys
    owner to firmware;

create unique index if not exists ix_membership_api_keys_secret_key
    on public.membership_api_keys (secret_key);

create table if not exists public.device_api_keys
(
    id         serial
        primary key,
    secret_key varchar,
    device_id  integer
        references public.devices,
    created_at timestamp,
    updated_at timestamp
);

alter table public.device_api_keys
    owner to firmware;

create unique index if not exists ix_device_api_keys_secret_key
    on public.device_api_keys (secret_key);

create table if not exists public.firmware_events
(
    id         uuid not null
        primary key,
    device_id  integer
        references public.devices,
    firmware   varchar,
    status     varchar,
    project_id integer
        references public.projects,
    timestamp  timestamp,
    created_at timestamp,
    updated_at timestamp
);

alter table public.firmware_events
    owner to firmware;

create index if not exists ix_firmware_events_status
    on public.firmware_events (status);

create index if not exists ix_firmware_events_firmware
    on public.firmware_events (firmware);

create index if not exists ix_firmware_events_timestamp
    on public.firmware_events (timestamp);




insert into projects (id, name)
values (1, 'project_1');
insert into projects (id, name)
values (2, 'project_2');

insert into devices (id, project_id, current_firmware)
values (1, 1, '1.0.0');
insert into devices (id, project_id, current_firmware)
values (2, 1, '1.0.1');
insert into devices (id, project_id, current_firmware)
values (3, 2, '1.0.2');

insert into device_api_keys (secret_key, device_id)
values ('super_secret_key_1', 1);
insert into device_api_keys (secret_key, device_id)
values ('super_secret_key_2', 2);
insert into device_api_keys (secret_key, device_id)
values ('super_secret_key_3', 3);



insert into memberships (id, email, project_id)
values (1, 'member_1', 1);
insert into memberships (id, email, project_id)
values (2, 'member_2', 1);
insert into memberships (id, email, project_id)
values (3, 'member_3', 2);


insert into membership_api_keys (secret_key, member_id)
values ('super_secret_member_key_1', 1);
insert into membership_api_keys (secret_key, member_id)
values ('super_secret_member_key_2', 2);
insert into membership_api_keys (secret_key, member_id)
values ('super_secret_member_key_3', 3);



insert into firmware_events (id, device_id, firmware, status, project_id, timestamp)
values (gen_random_uuid(), 1, '1.0.0', 'installed', 1, '2023-01-01 00:00:00'::timestamp);
insert into firmware_events (id, device_id, firmware, status, project_id, timestamp)
values (gen_random_uuid(), 2, '1.0.0', 'installed', 1, '2023-01-01 00:00:00'::timestamp);
insert into firmware_events (id, device_id, firmware, status, project_id, timestamp)
values (gen_random_uuid(), 2, '1.0.1', 'updated', 1, '2023-01-01 00:00:00'::timestamp);

insert into firmware_events (id, device_id, firmware, status, project_id, timestamp)
values (gen_random_uuid(), 3, '1.0.0', 'installed', 1, '2023-01-01 00:00:00'::timestamp);
insert into firmware_events (id, device_id, firmware, status, project_id, timestamp)
values (gen_random_uuid(), 3, '1.0.1', 'updated', 2, '2023-01-01 00:00:00'::timestamp);
insert into firmware_events (id, device_id, firmware, status, project_id, timestamp)
values (gen_random_uuid(), 3, '1.0.2', 'updated', 2, '2023-01-01 00:00:00'::timestamp);

