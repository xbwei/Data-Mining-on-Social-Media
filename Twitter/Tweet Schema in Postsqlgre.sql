
CREATE TABLE tweet (
    oid integer DEFAULT nextval('public.tweet_oid_seq1'::regclass) NOT NULL,
    tweetid character(256),
    tweetuser character(256),
    year character(50),
    month character(50),
    day character(50),
    "time" character(50),
    hashtags text,
    mention text,
    replyuser character(256),
    retweetuser character(256),
    text text,
    multireplyuser character(256),
    collectedtime timestamp without time zone DEFAULT now()
);


ALTER TABLE cpne.tweet OWNER TO postgres;

-- Completed on 2015-11-24 15:19:47

--
-- PostgreSQL database dump complete
--

