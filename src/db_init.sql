CREATE DATABASE golang;

\c golang;

CREATE TABLE public.organizations (
    id bigint NOT NULL PRIMARY KEY,
    name character varying(200),
    main_color character varying(10)
);


