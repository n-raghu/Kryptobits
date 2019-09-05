INSERT INTO userroles(rid, rolename, tokentime)
SELECT 1, 'poweruser', -1
UNION ALL
SELECT 2, 'temporary', 3600
UNION ALL
SELECT 3,'ieluser',88000
UNION ALL
SELECT 101,'cg-events',60
UNION ALL
SELECT 103,'cg-als',60;

INSERT INTO users(uid,pwd,user_name,roleid)
SELECT 'raghu','raghupassword','raghunandan',1
UNION ALL
SELECT 'yogesh','yogeshpassword','yogeshgupta',1
UNION ALL
SELECT 'vishnu','vishnupassword','vishnu',3
UNION ALL
SELECT 'consumer-als-events','alsevents','consumer-als-events',101
UNION ALL
SELECT 'consumer-accountdata','accountdatapass','consumer-accountdata',103;