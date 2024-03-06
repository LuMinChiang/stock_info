WITH RankedData AS (
    SELECT
        company_code,
        data_date,
        closing_price,
        volume,
        ROW_NUMBER() OVER (PARTITION BY company_code ORDER BY data_date DESC) AS row_num
    FROM
        company_history_data
)
SELECT
    company_code,
    data_date,
    closing_price,
    volume
FROM
    RankedData
WHERE
    row_num <= {} and company_code = "{}"
order by
 data_date asc;
