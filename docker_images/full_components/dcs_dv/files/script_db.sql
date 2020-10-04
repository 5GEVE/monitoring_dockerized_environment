create database dashboards;
create database pipelines;
create user eve with encrypted password 'changeme';
grant all privileges on database dashboards to eve;
grant all privileges on database pipelines to eve;
