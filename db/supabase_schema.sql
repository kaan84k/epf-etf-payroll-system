-- Schema for the Supabase database used by the payroll dashboard
-- Creates the employees table if it does not already exist

create table if not exists employees (
    id serial primary key,
    name text not null,
    email text not null unique,
    salary numeric not null
);
