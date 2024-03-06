CREATE VIEW filter_3 AS
WITH AvgData AS (
    SELECT 
        chd.company_code,
        AVG(CASE WHEN chd.data_date >= CURDATE() - INTERVAL 100 DAY THEN chd.closing_price END) AS avg_closing_price,
        AVG(CASE WHEN chd.data_date >= CURDATE() - INTERVAL 20 DAY THEN chd.volume END) AS avg_volume
    FROM 
        company_100_data chd
    GROUP BY 
        chd.company_code
),
LatestTwoDays AS (
    WITH LatestTwoDays AS (
        SELECT
            chd.company_code,
            chd.data_date,
            chd.closing_price,
            chd.volume,
            ROW_NUMBER() OVER (PARTITION BY chd.company_code ORDER BY chd.data_date DESC) AS row_num
        FROM
            company_100_data chd
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
	ROW_NUMBER() OVER () AS id,
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
    LatestTwoDays.volume_percentage_diff,
    ci.company_type,
    MAX(chd.closing_price) AS max_closing_price,
    MAX(chd.volume) AS max_volume
FROM 
    AvgData
JOIN 
    LatestTwoDays ON AvgData.company_code = LatestTwoDays.company_code
JOIN 
    company_id ci ON ci.company_code = AvgData.company_code
JOIN
    company_100_data chd ON chd.company_code = AvgData.company_code
WHERE
    LatestTwoDays.latest_closing_price > AvgData.avg_closing_price
    AND LatestTwoDays.latest_volume > 2 * AvgData.avg_volume
    AND LatestTwoDays.closing_price_percentage_diff > 3.5
    AND LatestTwoDays.latest_closing_price >= 10
GROUP BY
    AvgData.company_code, AvgData.avg_closing_price, AvgData.avg_volume,
    LatestTwoDays.latest_date, LatestTwoDays.latest_closing_price,
    LatestTwoDays.previous_date, LatestTwoDays.previous_closing_price,
    LatestTwoDays.closing_price_percentage_diff, LatestTwoDays.latest_volume,
    LatestTwoDays.previous_volume, LatestTwoDays.volume_percentage_diff,
    ci.company_type;
