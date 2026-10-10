SELECT * FROM pg_database;

create database fastapi;


select * from information_schema.tables where table_schema='public';

select * from information_schema.columns where table_name='posts';
select * from information_schema.columns where table_name='users';
select * from information_schema.columns where table_name='votes';
select * from information_schema.columns where table_name in('posts','users','votes');

select * from posts;

select * from users;

select * from votes;


select 
p.id post_id,
count(v.user_id) vote_count
from posts p
left join votes v on p.id=v.post_id
where p.id=1
GROUP BY p.id
order by p.id;

select
u.id user_id,
count(p.id) post_count
from users u
left join posts p
on u.id=p.user_id
where user_id=3
group by u.id;

select * from information_schema.tables where table_schema='public';

select * from information_schema.columns where table_schema='public';

drop table alembic_version;

select * from users;

drop table votes cascade;