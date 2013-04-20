--table books
create table if not exists books (
    id integer primary key,
    bookname    text,
    author      text,
    price       text,
    publisher   text,
    callnum     text,
    isbn        text,
    sortnum     text,
    pages       integer,
    pubdate     text,
    recno       integer,
    which_page  integer,
    commit_time text
);
