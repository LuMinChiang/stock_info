-- check company_history_data have duplicate data or not
SELECT d1.id,d1.company_code,d1.data_date
FROM company_history_data d1
INNER JOIN (
    SELECT company_code, data_date
    FROM company_history_data d2
    GROUP BY company_code, data_date
    HAVING COUNT(*) > 1
) AS duplicates
ON d1.company_code = duplicates.company_code AND d1.data_date = duplicates.data_date