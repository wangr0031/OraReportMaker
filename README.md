# OraReportMaker
## 20180819开发日志
1. 新增程序的logger,后续日志输出统一使用自定义的logger
## 20180820开发日志
1. DBMS_WORKLOAD_REPOSITORY.awr_report_html生成awr报告
2. 增加oracle的异常报错展示`cx_Oracle.DatabaseError`


## 备注

```
获取ASH报告
 
select output
  from table(dbms_workload_repository.ash_report_text((select dbid from v$database), 
                                                      1, 
                                                      TO_DATE('20130712203500', 
                                                              'YYYYMMDDHH24MISS'), 
                                                      TO_DATE('20130712204600', 
                                                              'YYYYMMDDHH24MISS')));
 
 
获取ADDM报告
select * from dba_advisor_tasks  s  order by  s.created desc
 
set long 1000000 pagesize 0 longchunksize 1000 
 
select   dbms_advisor.get_task_report('ADDM:3620614489_1_25298') from dual;
 
 
获取AWR报告
 
SELECT SNAP_ID snapid FROM DBA_HIST_SNAPSHOT;
     select output from
                   table(dbms_workload_repository.awr_report_text(
                                       &dbid,
                                       &inst_num,
                                       &bid, &eid,
                                       8 ));

```