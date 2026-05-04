--
-- PostgreSQL database dump
--

\restrict t33uFvqcegVaVyKSvZyee9kTi0PYqyAHfPQOh3MvbYxm32V5aHSzINpWFAoIgOz

-- Dumped from database version 18.1 (Debian 18.1-1.pgdg13+2)
-- Dumped by pg_dump version 18.3

-- Started on 2026-05-03 21:36:30

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
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
-- TOC entry 237 (class 1259 OID 16716)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO reklamacio_kezelo;

--
-- TOC entry 232 (class 1259 OID 16570)
-- Name: complaints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaints (
    id integer NOT NULL,
    complaint_date date DEFAULT CURRENT_DATE NOT NULL,
    complaint_number character varying(50) NOT NULL,
    product_identifier character varying(100) NOT NULL,
    quantity integer DEFAULT 1 NOT NULL,
    requires_return boolean DEFAULT false NOT NULL,
    description text,
    shipping_date date,
    total_cost integer DEFAULT 0,
    user_id integer NOT NULL,
    department_id integer NOT NULL,
    customer_id integer NOT NULL,
    product_id integer NOT NULL,
    defect_type_id integer NOT NULL,
    status_id integer NOT NULL
);


ALTER TABLE public.complaints OWNER TO reklamacio_kezelo;

--
-- TOC entry 231 (class 1259 OID 16569)
-- Name: complaints_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.complaints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.complaints_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3566 (class 0 OID 0)
-- Dependencies: 231
-- Name: complaints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.complaints_id_seq OWNED BY public.complaints.id;


--
-- TOC entry 224 (class 1259 OID 16526)
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    display_name character varying(100) NOT NULL
);


ALTER TABLE public.customers OWNER TO reklamacio_kezelo;

--
-- TOC entry 223 (class 1259 OID 16525)
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3567 (class 0 OID 0)
-- Dependencies: 223
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- TOC entry 228 (class 1259 OID 16548)
-- Name: defect_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.defect_types (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    display_name character varying(150) NOT NULL
);


ALTER TABLE public.defect_types OWNER TO reklamacio_kezelo;

--
-- TOC entry 227 (class 1259 OID 16547)
-- Name: defect_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.defect_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.defect_types_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3568 (class 0 OID 0)
-- Dependencies: 227
-- Name: defect_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.defect_types_id_seq OWNED BY public.defect_types.id;


--
-- TOC entry 222 (class 1259 OID 16515)
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    display_name character varying(100) NOT NULL
);


ALTER TABLE public.departments OWNER TO reklamacio_kezelo;

--
-- TOC entry 221 (class 1259 OID 16514)
-- Name: departments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.departments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.departments_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3569 (class 0 OID 0)
-- Dependencies: 221
-- Name: departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.departments_id_seq OWNED BY public.departments.id;


--
-- TOC entry 236 (class 1259 OID 16675)
-- Name: positions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.positions (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    display_name character varying(100) NOT NULL
);


ALTER TABLE public.positions OWNER TO reklamacio_kezelo;

--
-- TOC entry 235 (class 1259 OID 16674)
-- Name: positions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.positions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.positions_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3570 (class 0 OID 0)
-- Dependencies: 235
-- Name: positions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.positions_id_seq OWNED BY public.positions.id;


--
-- TOC entry 226 (class 1259 OID 16537)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    display_name character varying(150) NOT NULL
);


ALTER TABLE public.products OWNER TO reklamacio_kezelo;

--
-- TOC entry 225 (class 1259 OID 16536)
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3571 (class 0 OID 0)
-- Dependencies: 225
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- TOC entry 234 (class 1259 OID 16656)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    display_name character varying(100) NOT NULL
);


ALTER TABLE public.roles OWNER TO reklamacio_kezelo;

--
-- TOC entry 233 (class 1259 OID 16655)
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3572 (class 0 OID 0)
-- Dependencies: 233
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 230 (class 1259 OID 16559)
-- Name: statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.statuses (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    display_name character varying(100) NOT NULL
);


ALTER TABLE public.statuses OWNER TO reklamacio_kezelo;

--
-- TOC entry 229 (class 1259 OID 16558)
-- Name: statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.statuses_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3573 (class 0 OID 0)
-- Dependencies: 229
-- Name: statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.statuses_id_seq OWNED BY public.statuses.id;


--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    surname character varying(50) NOT NULL,
    forename character varying(50) NOT NULL,
    username character varying(20) NOT NULL,
    email character varying(120) NOT NULL,
    password character varying(60) NOT NULL,
    role_id integer NOT NULL,
    position_id integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.users OWNER TO reklamacio_kezelo;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO reklamacio_kezelo;

--
-- TOC entry 3574 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 3340 (class 2604 OID 16573)
-- Name: complaints id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints ALTER COLUMN id SET DEFAULT nextval('public.complaints_id_seq'::regclass);


--
-- TOC entry 3336 (class 2604 OID 16529)
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- TOC entry 3338 (class 2604 OID 16551)
-- Name: defect_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defect_types ALTER COLUMN id SET DEFAULT nextval('public.defect_types_id_seq'::regclass);


--
-- TOC entry 3335 (class 2604 OID 16518)
-- Name: departments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments ALTER COLUMN id SET DEFAULT nextval('public.departments_id_seq'::regclass);


--
-- TOC entry 3346 (class 2604 OID 16678)
-- Name: positions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.positions ALTER COLUMN id SET DEFAULT nextval('public.positions_id_seq'::regclass);


--
-- TOC entry 3337 (class 2604 OID 16540)
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- TOC entry 3345 (class 2604 OID 16659)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 3339 (class 2604 OID 16562)
-- Name: statuses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statuses ALTER COLUMN id SET DEFAULT nextval('public.statuses_id_seq'::regclass);


--
-- TOC entry 3333 (class 2604 OID 16393)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3560 (class 0 OID 16716)
-- Dependencies: 237
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version VALUES ('ba27b44f64df');


--
-- TOC entry 3555 (class 0 OID 16570)
-- Dependencies: 232
-- Data for Name: complaints; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.complaints VALUES (1, '2026-01-06', 'REK-202601115', '12556936', 3, false, 'A festési réteg vékony', '2025-09-11', 85000, 5, 4, 4, 3, 3, 2);
INSERT INTO public.complaints VALUES (2, '2026-02-05', 'REK-202601225', '12569445', 1, true, 'Hiányzó hegesztés', '2025-11-12', 75000, 5, 6, 3, 8, 12, 2);
INSERT INTO public.complaints VALUES (3, '2026-02-03', 'REK-20261258', '13526895', 2, true, 'A felületen nagy mennyiségű hegesztési fröcsek', '2025-10-29', 45000, 5, 5, 4, 12, 11, 1);
INSERT INTO public.complaints VALUES (4, '2026-02-10', 'REK-20251255', '23565840', 1, false, 'Oldallemez horpadt', '2025-08-06', 38000, 5, 2, 4, 1, 2, 3);
INSERT INTO public.complaints VALUES (5, '2025-12-12', 'REK-20251445', '12564558', 2, true, 'Ferde zártszelvény', '2025-11-13', 285000, 5, 2, 5, 2, 2, 2);
INSERT INTO public.complaints VALUES (6, '2025-12-23', 'REK-20254895', '13524589', 4, false, 'Szállítás közben sérült', '2025-09-17', 87000, 5, 9, 1, 5, 9, 3);
INSERT INTO public.complaints VALUES (7, '2025-11-12', 'REK-20252235', '12564556', 2, true, 'Hiányzó hegesztés', '2025-07-10', 45000, 5, 5, 4, 10, 12, 2);
INSERT INTO public.complaints VALUES (8, '2025-10-08', 'REK-20254332', '42268522', 1, false, 'Alkatrész rossz pozícióba', '2025-11-13', 37000, 5, 6, 6, 13, 8, 2);
INSERT INTO public.complaints VALUES (9, '2025-10-16', 'REK-20254225', '12569235', 2, false, 'Lemaradt fedőkupak', '2025-11-06', 35000, 5, 11, 4, 5, 10, 2);
INSERT INTO public.complaints VALUES (10, '2025-12-11', 'REK-20264456', '12544763', 2, true, 'Elmaradt hegesztés', '2026-02-11', 250000, 5, 6, 2, 8, 12, 2);
INSERT INTO public.complaints VALUES (11, '2026-02-09', 'REK-202600925', '23563320', 5, false, 'A termékeke hibás feéllel lettek felszerelve', '2025-09-16', 57800, 10, 11, 1, 3, 15, 2);
INSERT INTO public.complaints VALUES (13, '2026-02-16', 'REK-20252275', '13325558', 5, false, 'Rossz címkék kerültek a termékekre', '2026-01-27', 55000, 10, 1, 4, 5, 17, 2);
INSERT INTO public.complaints VALUES (14, '2025-08-12', 'REK-20250825', '13526795', 2, false, 'Termék fedél nélkül lett kiküldve', '2025-07-03', 45000, 5, 11, 4, 5, 10, 2);
INSERT INTO public.complaints VALUES (16, '2026-03-10', 'KEK-002', '12569665', 2, true, 'Vékony festégréteg', '2025-12-24', 85400, 12, 4, 5, 10, 3, 1);
INSERT INTO public.complaints VALUES (17, '2026-03-16', 'KEK-003', '12556447', 1, true, 'Alkatrész hibás pozícióban felhegsztve', '2026-01-08', 45000, 10, 5, 4, 14, 8, 1);
INSERT INTO public.complaints VALUES (18, '2026-04-10', 'REK-2515', '12563985', 2, true, 'Vékony festés réteg', '2025-12-05', 45000, 5, 4, 2, 2, 3, 2);
INSERT INTO public.complaints VALUES (12, '2026-02-17', 'REK-20253325', '13658879', 3, true, 'Hibás varrat miatt a tartály ereszt', '2025-12-16', 85000, 10, 7, 3, 4, 16, 2);


--
-- TOC entry 3547 (class 0 OID 16526)
-- Dependencies: 224
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers VALUES (1, 'hbm', 'HBM');
INSERT INTO public.customers VALUES (2, 'igm', 'IGM');
INSERT INTO public.customers VALUES (3, 'kone', 'KONE');
INSERT INTO public.customers VALUES (4, 'lbh', 'LBH');
INSERT INTO public.customers VALUES (5, 'lec', 'LEC');
INSERT INTO public.customers VALUES (6, 'prinoth', 'PRINOTH');
INSERT INTO public.customers VALUES (7, 'lfr', 'LFR');


--
-- TOC entry 3551 (class 0 OID 16548)
-- Dependencies: 228
-- Data for Name: defect_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.defect_types VALUES (1, 'beszállítóihiba', 'beszállítói hiba');
INSERT INTO public.defect_types VALUES (2, 'egyengetésihiba', 'egyengetési hiba');
INSERT INTO public.defect_types VALUES (3, 'festésihiba', 'festési hiba');
INSERT INTO public.defect_types VALUES (4, 'forgácsolásihiba', 'forgácsolási hiba');
INSERT INTO public.defect_types VALUES (5, 'menetelésihiba', 'menetelési hiba');
INSERT INTO public.defect_types VALUES (6, 'mérethiba', 'méret hiba');
INSERT INTO public.defect_types VALUES (7, 'mosásihiba', 'mosási hiba');
INSERT INTO public.defect_types VALUES (8, 'összeállításihiba', 'összeállítási hiba');
INSERT INTO public.defect_types VALUES (9, 'szállításisérülés', 'szállítási sérülés');
INSERT INTO public.defect_types VALUES (10, 'szerelésihiba', 'szerelési hiba');
INSERT INTO public.defect_types VALUES (11, 'tisztításihiba', 'tisztítási hiba');
INSERT INTO public.defect_types VALUES (12, 'hegesztésihiba', 'hegesztési hiba');
INSERT INTO public.defect_types VALUES (13, 'tömítetlenvarrat', 'tömítetlen varrat');
INSERT INTO public.defect_types VALUES (14, 'rozsdás', 'rozsdás');
INSERT INTO public.defect_types VALUES (15, 'hibasszereles', 'hibás szerelés');
INSERT INTO public.defect_types VALUES (16, 'lyukastartaly', 'lyukas tartály');
INSERT INTO public.defect_types VALUES (17, 'hibasgyartmanykisero', 'hibás gyártmánykísérő');


--
-- TOC entry 3545 (class 0 OID 16515)
-- Dependencies: 222
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.departments VALUES (1, 'adminisztráció', 'adminisztráció');
INSERT INTO public.departments VALUES (2, 'alkatrészgyártó', 'alkatrészgyártó');
INSERT INTO public.departments VALUES (3, 'beszállító', 'beszállító');
INSERT INTO public.departments VALUES (5, 'kisműhely', 'kisműhely');
INSERT INTO public.departments VALUES (6, 'nagyműhely', 'nagyműhely');
INSERT INTO public.departments VALUES (7, 'nyomáspróba', 'nyomáspróba');
INSERT INTO public.departments VALUES (8, 'raktár', 'raktár');
INSERT INTO public.departments VALUES (9, 'szállítás', 'szállítás');
INSERT INTO public.departments VALUES (10, 'szerelés', 'szerelés');
INSERT INTO public.departments VALUES (11, 'csomagoló', 'csomagoló');
INSERT INTO public.departments VALUES (12, 'mosó', 'mosó');
INSERT INTO public.departments VALUES (4, 'festőüzem', 'festőüzem');


--
-- TOC entry 3559 (class 0 OID 16675)
-- Dependencies: 236
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.positions VALUES (52, 'ugyvezetoigazgato', 'ügyvezető igazgató');
INSERT INTO public.positions VALUES (8, 'segedoperator', 'segéd operátor');
INSERT INTO public.positions VALUES (9, 'hegesztesivezeto', 'hegesztési vezető');
INSERT INTO public.positions VALUES (7, 'hegesztesitechnologus', 'hegesztési technológus');
INSERT INTO public.positions VALUES (1, 'operator', 'operátor');
INSERT INTO public.positions VALUES (2, 'minosegellenor', 'minőségellenőr');
INSERT INTO public.positions VALUES (3, 'technologus', 'technológus');
INSERT INTO public.positions VALUES (4, 'uzemvezeto', 'üzemvezető');
INSERT INTO public.positions VALUES (5, 'telephelyvezeto', 'telephelyvezető');
INSERT INTO public.positions VALUES (6, 'adminisztrator', 'adminisztrátor');
INSERT INTO public.positions VALUES (10, 'karbantarto', 'karbantartó');
INSERT INTO public.positions VALUES (11, 'villanyszerelo', 'villanyszerelő');
INSERT INTO public.positions VALUES (12, 'segedtechnologus', 'segéd technológus');


--
-- TOC entry 3549 (class 0 OID 16537)
-- Dependencies: 226
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products VALUES (1, 'bodenplatte', 'bodenplatte');
INSERT INTO public.products VALUES (2, 'console', 'console');
INSERT INTO public.products VALUES (3, 'dieseltank', 'dieseltank');
INSERT INTO public.products VALUES (4, 'oiltank', 'oiltank');
INSERT INTO public.products VALUES (5, 'hydrauliktank', 'hydrauliktank');
INSERT INTO public.products VALUES (6, 'kabinenbodenplatte', 'kabinenbodenplatte');
INSERT INTO public.products VALUES (7, 'kabinenpodest', 'kabinenpodest');
INSERT INTO public.products VALUES (8, 'kasten', 'kasten');
INSERT INTO public.products VALUES (9, 'kraftstofftank', 'kraftstofftank');
INSERT INTO public.products VALUES (10, 'kühlerkasten', 'kühlerkasten');
INSERT INTO public.products VALUES (11, 'wasserkühlerkasten', 'wasserkühlerkasten');
INSERT INTO public.products VALUES (12, 'kabinenkasten', 'kabinenkasten');
INSERT INTO public.products VALUES (13, 'gehause', 'gehause');
INSERT INTO public.products VALUES (14, 'bisoftank', 'bisoftank');


--
-- TOC entry 3557 (class 0 OID 16656)
-- Dependencies: 234
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roles VALUES (3, 'admin', 'Adminisztrátor');
INSERT INTO public.roles VALUES (1, 'user', 'Alap felhasználó');
INSERT INTO public.roles VALUES (2, 'super_user', 'Haladó felhasználó');


--
-- TOC entry 3553 (class 0 OID 16559)
-- Dependencies: 230
-- Data for Name: statuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.statuses VALUES (1, 'folyamatban', 'folyamatban');
INSERT INTO public.statuses VALUES (2, 'elfogadva', 'elfogadva');
INSERT INTO public.statuses VALUES (3, 'visszautasitva', 'visszautasítva');


--
-- TOC entry 3543 (class 0 OID 16390)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES (1, 'Varga', 'Norbert', 'vargan', 'varga.norbert@pelda.hu', '$2b$12$htgXOQUWRi/PMPR0SfKbduqgstt97wu2fXuAtacD4iTUy0ROt0zz6', 3, 6, true);
INSERT INTO public.users VALUES (11, 'Nagy', 'Endre', 'enagy', 'enagy@proba.hu', '$2b$12$tTpRnN/Psb6VIrhftl1QRu.3nYAEmVeUtQl2iw8xQ0TL6la85vfmC', 1, 10, true);
INSERT INTO public.users VALUES (12, 'Szabó', 'Lajos', 'lszabo', 'lszabo@proba.hu', '$2b$12$HtEMWL3mkcp/vvelbx5xAu7VK8zz40oXX1O.SB9/WLlG7h5no8DYe', 2, 2, true);
INSERT INTO public.users VALUES (13, 'Kiss', 'András', 'akiss', 'akiss@proba.hu', '$2b$12$dHrcJzGjg4dkdkp9HJ9P7O774CWtPYDtVPmyoLi4V88TAtkmToti6', 2, 52, true);
INSERT INTO public.users VALUES (9, 'Orsós', 'Kevin', 'korsos', 'korsos@proba.hu', '$2b$12$JZmp2V2rsP0wPkPvE0Z9E.NJHxu7HmOYtOFP4ZkzTtoxPGNXv3VVO', 1, 12, true);
INSERT INTO public.users VALUES (8, 'Szabó', 'Aladár', 'aszabo', 'aszabo@proba.hu', '$2b$12$UGvj73eYXz55YR8ug2iTHO.D58GfiRmQalcmJWPh8ORDlNkTfx5o.', 1, 6, false);
INSERT INTO public.users VALUES (10, 'Farkas', 'Csaba', 'csfarkas', 'norbi0187@gmail.com', '$2b$12$X2wVE715Ka7GwIv/LKZH/uuuC5Rl9hUjupt7kUSPnV05HEEG740GK', 2, 3, true);
INSERT INTO public.users VALUES (14, 'Aradi', 'Lajos', 'laradi', 'laradi@proba.hu', '$2b$12$RUflUEoXgHh8.VOVHwvXROgFc.Ea0UNUkhVIZAbLeBrG8OiTDod7G', 1, 10, true);
INSERT INTO public.users VALUES (5, 'Kovács', 'Mihály', 'kmihaly', 'kmihaly@proba.hu', '$2b$12$9c6Bn.eYhM99hOFRzQgia.UVZfWentIx0mmaAByVXD5vNhJX16vAG', 2, 9, true);
INSERT INTO public.users VALUES (6, 'Csonka', 'Ádám', 'csadam', 'csadam@proba.hu', '$2b$12$QePJ0nm.BE6fexokXpcRheBlxCy7WLkxui9uufyJ9PnVYdVHUoeg.', 1, 10, true);


--
-- TOC entry 3575 (class 0 OID 0)
-- Dependencies: 231
-- Name: complaints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.complaints_id_seq', 18, true);


--
-- TOC entry 3576 (class 0 OID 0)
-- Dependencies: 223
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_id_seq', 7, true);


--
-- TOC entry 3577 (class 0 OID 0)
-- Dependencies: 227
-- Name: defect_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.defect_types_id_seq', 17, true);


--
-- TOC entry 3578 (class 0 OID 0)
-- Dependencies: 221
-- Name: departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departments_id_seq', 12, true);


--
-- TOC entry 3579 (class 0 OID 0)
-- Dependencies: 235
-- Name: positions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.positions_id_seq', 52, true);


--
-- TOC entry 3580 (class 0 OID 0)
-- Dependencies: 225
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 14, true);


--
-- TOC entry 3581 (class 0 OID 0)
-- Dependencies: 233
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 44, true);


--
-- TOC entry 3582 (class 0 OID 0)
-- Dependencies: 229
-- Name: statuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.statuses_id_seq', 3, true);


--
-- TOC entry 3583 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 14, true);


--
-- TOC entry 3386 (class 2606 OID 16721)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3374 (class 2606 OID 16595)
-- Name: complaints complaints_complaint_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_complaint_number_key UNIQUE (complaint_number);


--
-- TOC entry 3376 (class 2606 OID 16593)
-- Name: complaints complaints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_pkey PRIMARY KEY (id);


--
-- TOC entry 3358 (class 2606 OID 16535)
-- Name: customers customers_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_name_key UNIQUE (name);


--
-- TOC entry 3360 (class 2606 OID 16533)
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- TOC entry 3366 (class 2606 OID 16557)
-- Name: defect_types defect_types_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defect_types
    ADD CONSTRAINT defect_types_name_key UNIQUE (name);


--
-- TOC entry 3368 (class 2606 OID 16555)
-- Name: defect_types defect_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defect_types
    ADD CONSTRAINT defect_types_pkey PRIMARY KEY (id);


--
-- TOC entry 3354 (class 2606 OID 16524)
-- Name: departments departments_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_name_key UNIQUE (name);


--
-- TOC entry 3356 (class 2606 OID 16522)
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- TOC entry 3382 (class 2606 OID 16685)
-- Name: positions positions_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_name_key UNIQUE (name);


--
-- TOC entry 3384 (class 2606 OID 16683)
-- Name: positions positions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (id);


--
-- TOC entry 3362 (class 2606 OID 16712)
-- Name: products products_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_name_key UNIQUE (name);


--
-- TOC entry 3364 (class 2606 OID 16544)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- TOC entry 3378 (class 2606 OID 16665)
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- TOC entry 3380 (class 2606 OID 16663)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3370 (class 2606 OID 16568)
-- Name: statuses statuses_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_name_key UNIQUE (name);


--
-- TOC entry 3372 (class 2606 OID 16566)
-- Name: statuses statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_pkey PRIMARY KEY (id);


--
-- TOC entry 3348 (class 2606 OID 16407)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3350 (class 2606 OID 16403)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3352 (class 2606 OID 16405)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 3389 (class 2606 OID 16606)
-- Name: complaints complaints_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- TOC entry 3390 (class 2606 OID 16616)
-- Name: complaints complaints_defect_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_defect_type_id_fkey FOREIGN KEY (defect_type_id) REFERENCES public.defect_types(id);


--
-- TOC entry 3391 (class 2606 OID 16601)
-- Name: complaints complaints_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- TOC entry 3392 (class 2606 OID 16611)
-- Name: complaints complaints_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- TOC entry 3393 (class 2606 OID 16621)
-- Name: complaints complaints_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.statuses(id);


--
-- TOC entry 3394 (class 2606 OID 16596)
-- Name: complaints complaints_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 3387 (class 2606 OID 16686)
-- Name: users fk_users_positions; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_positions FOREIGN KEY (position_id) REFERENCES public.positions(id);


--
-- TOC entry 3388 (class 2606 OID 16667)
-- Name: users fk_users_roles; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_roles FOREIGN KEY (role_id) REFERENCES public.roles(id);


-- Completed on 2026-05-03 21:36:30

--
-- PostgreSQL database dump complete
--

\unrestrict t33uFvqcegVaVyKSvZyee9kTi0PYqyAHfPQOh3MvbYxm32V5aHSzINpWFAoIgOz

