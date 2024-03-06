WITH RankedData AS (
    SELECT
        company_code,
        data_date,
        closing_price,
        ROW_NUMBER() OVER (PARTITION BY company_code ORDER BY ABS(DATEDIFF(data_date, '{}')) ASC, data_date DESC) AS row_num
    FROM
        company_history_data
    WHERE
		company_code = '{}' AND
        closing_price IS NOT NULL AND closing_price != 0
        AND data_date <= '{}'
)
SELECT
    company_code,
    data_date,
    closing_price
FROM
    RankedData
WHERE
    row_num = 1;