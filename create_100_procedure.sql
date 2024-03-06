DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateCompany100Data`()
BEGIN
    -- Drop the existing temporary table if it exists
    DROP TEMPORARY TABLE IF EXISTS tmp_company_100_data;

    -- Create a temporary table to hold the latest 100 records for each company_code
    CREATE TEMPORARY TABLE tmp_company_100_data AS
    SELECT
        chd.company_code,
        NOW(),
        "mysql_procedure",
        chd.closing_price,
        chd.volume,
        chd.data_date,
        chd.foreign_share_holding_ratio
    FROM (
        SELECT
            company_code,
            data_date,
            closing_price,
            volume,
            foreign_share_holding_ratio,
            ROW_NUMBER() OVER (PARTITION BY company_code ORDER BY data_date DESC) AS row_num
        FROM
            company_history_data
        WHERE
            company_code IS NOT NULL
    ) chd
    WHERE
        row_num <= 100;

    -- Truncate the existing company_100_data table
    TRUNCATE TABLE company_100_data;

    -- Insert the data from the temporary table into company_100_data
    INSERT INTO company_100_data 
    (company_code,update_time,update_name,closing_price,volume,data_date,foreign_share_holding_ratio)
    SELECT * FROM tmp_company_100_data;

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS tmp_company_100_data;
END //

DELIMITER ;