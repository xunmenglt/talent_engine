```sql
SELECT * FROM T_HX_EMP_KPI 
WHERE KPI_YEAR = 2023 
  AND INSTITUTION_NAME = '北京总部' 
  AND KPI_GRADE = 'A';
````

| ID | KPI\_YEAR | EMP\_NO | EMP\_NAME | INSTITUTION\_NO | INSTITUTION\_NAME | JOB\_NO | JOB\_NAME | SCORE | JOB\_RANK | JOB\_TOTAL | REGION\_RANK | REGION\_TOTAL | REMARK | CREATE\_USER | UPDATE\_USER | KPI\_GRADE | CREATE\_TIME        | UPDATE\_TIME        |
| -- | --------- | ------- | --------- | --------------- | ----------------- | ------- | --------- | ----- | --------- | ---------- | ------------ | ------------- | ------ | ------------ | ------------ | ---------- | ------------------- | ------------------- |
| 1  | 2023      | EMP001  | 张伟        | BJ001           | 北京总部              | POS001  | 高级工程师     | 95.50 | 1         | 2          | 3            | 4             | None   | admin        | admin        | A          | 2025-05-12 19:21:56 | 2025-05-12 19:22:45 |

