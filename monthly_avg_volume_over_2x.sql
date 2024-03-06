CREATE TABLE `STOCK_INFO`.`monthly_avg_volume_over_2x` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_code` VARCHAR(10) NULL,
  `update_time` DATETIME NULL,
  `update_name` VARCHAR(20) NULL DEFAULT NULL,
  `data_date` DATETIME NULL,
  `x_times` FLOAT NULL,
  PRIMARY KEY (`id`));