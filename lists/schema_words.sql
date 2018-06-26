CREATE TABLE IF NOT EXISTS "word" (
  `w` TEXT,
  `pos` TEXT,
  `ts`  REAL,
  `cnt` INTEGER DEFAULT 1,
  `src` TEXT,
  CONSTRAINT wpos UNIQUE (w,pos)
);
CREATE TABLE IF NOT EXISTS "phrase" (
  `ph` TEXT,
  `tw` TEXT, /* json array of tagged words in phrase: [[word, postag], ...] */
  `ts`  REAL,
  `src` TEXT,
  CONSTRAINT phsrc UNIQUE (ph,src)
);
