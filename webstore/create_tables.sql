DROP TABLE IF EXISTS public.http_basic_monitor;
DROP TABLE IF EXISTS public.http_regex_monitor;

CREATE TABLE public.http_basic_monitor
(
    host VARCHAR(255) NOT NULL,
    error_code INT,
    monitor_time TIMESTAMP,
    response_time_sec REAL
)
TABLESPACE pg_default;

CREATE TABLE public.http_regex_monitor
(
    host VARCHAR(255) NOT NULL,
    monitor_time TIMESTAMP,
    regex_match VARCHAR(255)
)
TABLESPACE pg_default;