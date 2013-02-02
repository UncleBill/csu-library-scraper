--table books
create table books (
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
    recno        integer
);
--table bookInfos
create table bookInfos (
    id integer primary key,
    recno       integer,
    call_num    text,
    bar_code    text,
    login_num   text,
    store_loca  text,
    store_state text,
    lend_date   text,
    return_date text,
    tran_type   text,
    order_handle    text,
    volumn_info text,
    commit_time date,
    alt_time    date
);
--a trigger adding inserting time
create trigger add_time after
insert on bookInfos
begin
    insert into bookInfos ( commit_time ) values ( date('now') );
end;

--create trigger update_time after
--update on books
--begin
    --insert into bookInfos ( alt_time ) values ( datetime('now') );
--end;

