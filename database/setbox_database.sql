--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE setbox;
--
-- Name: setbox; Type: DATABASE; Schema: -; Owner: edvardsmazprecnieks
--

CREATE DATABASE setbox WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = icu LOCALE = 'en_US.UTF-8' ICU_LOCALE = 'en-US';


ALTER DATABASE setbox OWNER TO edvardsmazprecnieks;

\connect setbox

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: files; Type: TABLE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE TABLE public.files (
    lesson_id integer NOT NULL,
    info character varying(255) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.files OWNER TO edvardsmazprecnieks;

--
-- Name: files_id_seq; Type: SEQUENCE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE SEQUENCE public.files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.files_id_seq OWNER TO edvardsmazprecnieks;

--
-- Name: files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edvardsmazprecnieks
--

ALTER SEQUENCE public.files_id_seq OWNED BY public.files.id;


--
-- Name: lesson; Type: TABLE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE TABLE public.lesson (
    id integer NOT NULL,
    subject_id integer NOT NULL,
    date date NOT NULL,
    progress integer,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    name character varying(255)
);


ALTER TABLE public.lesson OWNER TO edvardsmazprecnieks;

--
-- Name: lesson_id_seq; Type: SEQUENCE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE SEQUENCE public.lesson_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lesson_id_seq OWNER TO edvardsmazprecnieks;

--
-- Name: lesson_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edvardsmazprecnieks
--

ALTER SEQUENCE public.lesson_id_seq OWNED BY public.lesson.id;


--
-- Name: subjects; Type: TABLE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE TABLE public.subjects (
    name character varying(255) NOT NULL,
    id integer NOT NULL,
    owner_user_id integer NOT NULL
);


ALTER TABLE public.subjects OWNER TO edvardsmazprecnieks;

--
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE SEQUENCE public.subjects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_id_seq OWNER TO edvardsmazprecnieks;

--
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edvardsmazprecnieks
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE TABLE public.users (
    email character varying(255),
    name character varying(255),
    id integer NOT NULL
);


ALTER TABLE public.users OWNER TO edvardsmazprecnieks;

--
-- Name: users_and_subject; Type: TABLE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE TABLE public.users_and_subject (
    user_id integer NOT NULL,
    subject_id integer NOT NULL,
    editor boolean NOT NULL
);


ALTER TABLE public.users_and_subject OWNER TO edvardsmazprecnieks;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: edvardsmazprecnieks
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO edvardsmazprecnieks;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edvardsmazprecnieks
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: files id; Type: DEFAULT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.files ALTER COLUMN id SET DEFAULT nextval('public.files_id_seq'::regclass);


--
-- Name: lesson id; Type: DEFAULT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.lesson ALTER COLUMN id SET DEFAULT nextval('public.lesson_id_seq'::regclass);


--
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: edvardsmazprecnieks
--



--
-- Data for Name: lesson; Type: TABLE DATA; Schema: public; Owner: edvardsmazprecnieks
--

INSERT INTO public.lesson VALUES (7, 3, '2023-03-10', 90, '17:00:00', '18:00:00', NULL);
INSERT INTO public.lesson VALUES (8, 3, '2022-11-23', NULL, '11:10:00', '12:50:00', 'Multiplicators');
INSERT INTO public.lesson VALUES (9, 4, '2022-12-01', NULL, '13:10:00', '16:35:00', 'Math words');
INSERT INTO public.lesson VALUES (10, 3, '2023-01-01', NULL, '00:01:00', '02:03:00', 'Celebrate New Year with Math');


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: edvardsmazprecnieks
--

INSERT INTO public.subjects VALUES ('Math', 3, 1);
INSERT INTO public.subjects VALUES ('English', 4, 1);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: edvardsmazprecnieks
--

INSERT INTO public.users VALUES ('Edvards', 'edvards@edvards.lv', 1);


--
-- Data for Name: users_and_subject; Type: TABLE DATA; Schema: public; Owner: edvardsmazprecnieks
--



--
-- Name: files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edvardsmazprecnieks
--

SELECT pg_catalog.setval('public.files_id_seq', 1, false);


--
-- Name: lesson_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edvardsmazprecnieks
--

SELECT pg_catalog.setval('public.lesson_id_seq', 6, true);


--
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edvardsmazprecnieks
--

SELECT pg_catalog.setval('public.subjects_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edvardsmazprecnieks
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: files files_id_key; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_id_key UNIQUE (id);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: lesson lesson_pkey; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.lesson
    ADD CONSTRAINT lesson_pkey PRIMARY KEY (id);


--
-- Name: subjects subjects_id_key; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_id_key UNIQUE (id);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- Name: users_and_subject users_and_subject_pkey; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users_and_subject
    ADD CONSTRAINT users_and_subject_pkey PRIMARY KEY (user_id, subject_id);


--
-- Name: users_and_subject users_and_subject_user_id_subject_id_key; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users_and_subject
    ADD CONSTRAINT users_and_subject_user_id_subject_id_key UNIQUE (user_id, subject_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_id_key; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_id_key UNIQUE (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: files files_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lesson(id);


--
-- Name: lesson lesson_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.lesson
    ADD CONSTRAINT lesson_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- Name: subjects subjects_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_user_id_fkey FOREIGN KEY (owner_user_id) REFERENCES public.users(id);


--
-- Name: users_and_subject users_and_subject_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users_and_subject
    ADD CONSTRAINT users_and_subject_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- Name: users_and_subject users_and_subject_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: edvardsmazprecnieks
--

ALTER TABLE ONLY public.users_and_subject
    ADD CONSTRAINT users_and_subject_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

