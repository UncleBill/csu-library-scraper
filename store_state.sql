select count(*) from bookInfos;
select count(*) from bookInfos where store_state = '入藏';
select count(*) from bookInfos where store_state = '借出';
select count(*) from bookInfos where (not store_state = '借出') and (not store_state = '入藏');
