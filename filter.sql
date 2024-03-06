WITH AvgData AS (
    SELECT 
        company_code,
        AVG(CASE WHEN data_date >= CURDATE() - INTERVAL 100 DAY THEN closing_price END) AS avg_closing_price,
        AVG(CASE WHEN data_date >= CURDATE() - INTERVAL 20 DAY THEN volume END) AS avg_volume
    FROM 
        company_history_data
    GROUP BY 
        company_code
),
LatestTwoDays AS (
    WITH LatestTwoDays AS (
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
        A.company_code,
        A.data_date AS latest_date,
        A.closing_price AS latest_closing_price,
        A.volume AS latest_volume,
        B.data_date AS previous_date,
        B.closing_price AS previous_closing_price,
        B.volume AS previous_volume,
        ((A.closing_price - B.closing_price) / B.closing_price) * 100 AS closing_price_percentage_diff,
        ((A.volume - B.volume) / B.volume) * 100 AS volume_percentage_diff
    FROM
        LatestTwoDays A
    JOIN
        LatestTwoDays B ON A.company_code = B.company_code AND A.row_num = 1 AND B.row_num = 2
)
SELECT 
    AvgData.company_code,
    AvgData.avg_closing_price,
    AvgData.avg_volume,
    LatestTwoDays.latest_date,
    LatestTwoDays.latest_closing_price,
    LatestTwoDays.previous_date,
    LatestTwoDays.previous_closing_price,
    LatestTwoDays.closing_price_percentage_diff,
    LatestTwoDays.latest_volume,
    LatestTwoDays.previous_volume,
    LatestTwoDays.volume_percentage_diff
FROM 
    AvgData
JOIN 
    LatestTwoDays ON AvgData.company_code = LatestTwoDays.company_code
WHERE
    LatestTwoDays.latest_closing_price > AvgData.avg_closing_price
    AND LatestTwoDays.latest_volume > 2 * AvgData.avg_volume
    AND LatestTwoDays.closing_price_percentage_diff > 3.5;
