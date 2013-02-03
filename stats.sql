.nullvalue 'NULL'
select 'how many books?';
select count(*) from books;

select 'bad books?';
select count(*) from books where bookname = 'No existing!';

select 'store stats?';
select count(*),store_state from bookInfos group by store_state;
