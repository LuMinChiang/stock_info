WITH RankedData AS (
    SELECT
        company_code,
        data_date,
        closing_price,
        volume,
        ROW_NUMBER() OVER (PARTITION BY company_code ORDER BY data_date DESC) AS row_num
    FROM
        company_100_data
    WHERE
        closing_price IS NOT NULL AND closing_price != 0
        AND volume IS NOT NULL AND volume != 0
)
SELECT
    company_code,
    data_date,
    closing_price,
    volume
FROM
    RankedData
WHERE
    row_num = 1;
