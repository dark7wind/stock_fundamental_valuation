-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema securities_database
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `securities_database` ;

-- -----------------------------------------------------
-- Schema securities_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `securities_database` DEFAULT CHARACTER SET utf8 ;
USE `securities_database` ;

-- -----------------------------------------------------
-- Table `securities_database`.`stock_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`stock_info` ;

CREATE TABLE IF NOT EXISTS `securities_database`.`stock_info` (
  `stockId` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `createdDate` DATE NULL,
  `lastUpdatedDate` DATE NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `companyName` VARCHAR(255) NULL,
  `exchange` VARCHAR(255) NULL,
  `country` VARCHAR(255) NULL,
  `sp500` TINYINT NULL,
  `dow` TINYINT NULL,
  `industry` VARCHAR(255) NULL,
  `currency` VARCHAR(32) NULL,
  PRIMARY KEY (`stockId`),
  UNIQUE INDEX `stockId_UNIQUE` (`stockId` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securities_database`.`income_statement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`income_statement` ;

CREATE TABLE IF NOT EXISTS `securities_database`.`income_statement` (
  `stockId` INT UNSIGNED NOT NULL,
  `endDate` DATE NOT NULL,
  `createdDate` VARCHAR(45) NULL,
  `lastUpdatedDate` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `researchDevelopment` BIGINT NULL,
  `effectOfAccountingCharges` BIGINT NULL,
  `incomeBeforeTax` BIGINT NULL,
  `minorityInterest` BIGINT NULL,
  `netIncome` BIGINT NULL,
  `sellingGeneralAdministrative` BIGINT NULL,
  `grossProfit` BIGINT NULL,
  `ebit` BIGINT NULL,
  `operatingIncome` BIGINT NULL,
  `otherOperatingExpenses` BIGINT NULL,
  `interestExpense` BIGINT NULL,
  `extraordinaryItems` BIGINT NULL,
  `nonRecurring` BIGINT NULL,
  `otherItems` BIGINT NULL,
  `incomeTaxExpense` BIGINT NULL,
  `totalOperatingExpenses` BIGINT NULL,
  `totalRevenue` BIGINT NULL,
  `costOfRevenue` BIGINT NULL,
  `totalOtherIncomeExpenseNet` BIGINT NULL,
  `discontinuedOperations` BIGINT NULL,
  `netIncomeFromContinuingOps` BIGINT NULL,
  `netIncomeApplicableToCommonShares` BIGINT NULL,
  INDEX `fk_income_statement_stock_info1_idx` (`stockId` ASC) VISIBLE,
  PRIMARY KEY (`stockId`, `endDate`),
  CONSTRAINT `fk_income_statement_stock_info1`
    FOREIGN KEY (`stockId`)
    REFERENCES `securities_database`.`stock_info` (`stockId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securities_database`.`stock_statistics`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`stock_statistics` ;

CREATE TABLE IF NOT EXISTS `securities_database`.`stock_statistics` (
  `stockId` INT UNSIGNED NOT NULL,
  `createdDate` DATE NULL,
  `lastUpdatedDate` DATE NULL,
  `endDate` DATE NULL,
  `sharesBasic` INT NULL,
  `sharesDiluted` INT UNSIGNED NULL,
  PRIMARY KEY (`stockId`),
  CONSTRAINT `fk_stock_statistics_stock_info1`
    FOREIGN KEY (`stockId`)
    REFERENCES `securities_database`.`stock_info` (`stockId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securities_database`.`cash_flow`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`cash_flow` ;

CREATE TABLE IF NOT EXISTS `securities_database`.`cash_flow` (
  `stockId` INT UNSIGNED NOT NULL,
  `endDate` VARCHAR(45) NOT NULL,
  `createdDate` DATE NULL,
  `lastUpdatedDate` DATE NULL,
  `type` VARCHAR(45) NOT NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `investments` INT NULL,
  `changeToLiabilities` INT NULL,
  `totalCashflowsFromInvestingActivities` INT NULL,
  `netBorrowings` INT NULL,
  `totalCashFromFinancingActivities` INT NULL,
  `changeToOperatingActivities` INT NULL,
  `issuanceOfStock` INT NULL,
  `netIncome` INT NULL,
  `changeInCash` INT NULL,
  `repurchaseOfStock` INT NULL,
  `totalCashFromOperatingActivities` INT NULL,
  `depreciation` INT NULL,
  `otherCashflowsFromInvestingActivities` INT NULL,
  `dividendsPaid` INT NULL,
  `changeToInventory` INT NULL,
  `changeToAccountReceivables` INT NULL,
  `otherCashflowsFromFinancingActivities` INT NULL,
  `changeToNetincome` INT NULL,
  `capitalExpenditures` INT NULL,
  `effectOfExchangeRate` INT NULL,
  PRIMARY KEY (`stockId`, `endDate`),
  INDEX `fk_cash_flow_stock_info1_idx` (`stockId` ASC) VISIBLE,
  CONSTRAINT `fk_cash_flow_stock_info1`
    FOREIGN KEY (`stockId`)
    REFERENCES `securities_database`.`stock_info` (`stockId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securities_database`.`balance_sheet`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`balance_sheet` ;

CREATE TABLE IF NOT EXISTS `securities_database`.`balance_sheet` (
  `stockId` INT UNSIGNED NOT NULL,
  `endDate` DATE NOT NULL,
  `createdDate` DATE NOT NULL,
  `lastUpdatedDate` DATE NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `totalLiab` BIGINT NULL,
  `totalStockholderEquity` BIGINT NULL,
  `otherCurrentLiab` BIGINT NULL,
  `totalAssets` BIGINT NULL,
  `commonStock` BIGINT NULL,
  `otherCurrentAssets` BIGINT NULL,
  `retainedEarnings` BIGINT NULL,
  `otherLiab` BIGINT NULL,
  `treasuryStock` BIGINT NULL,
  `otherAssets` BIGINT NULL,
  `cash` BIGINT NULL,
  `totalCurrentLiabilities` BIGINT NULL,
  `shortLongTermDebt` BIGINT NULL,
  `otherStockholderEquity` BIGINT NULL,
  `propertyPlantEquipment` BIGINT NULL,
  `totalCurrentAssets` BIGINT NULL,
  `longTermInvestments` BIGINT NULL,
  `netTangibleAssets` BIGINT NULL,
  `shortTermInvestments` BIGINT NULL,
  `netReceivables` BIGINT NULL,
  `longTermDebt` BIGINT NULL,
  `inventory` BIGINT NULL,
  `accountsPayable` BIGINT NULL,
  `intangibleAssets` BIGINT NULL,
  `goodWill` BIGINT NULL,
  `capitalSurplus` BIGINT NULL,
  `deferredLongTermAssetCharges` BIGINT NULL,
  `minorityInterest` BIGINT NULL,
  `deferredLongTermLiab` BIGINT NULL,
  PRIMARY KEY (`stockId`, `endDate`),
  INDEX `fk_balance_sheet_stock_info1_idx` (`stockId` ASC) VISIBLE,
  CONSTRAINT `fk_balance_sheet_stock_info1`
    FOREIGN KEY (`stockId`)
    REFERENCES `securities_database`.`stock_info` (`stockId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
