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
  `createDate` VARCHAR(45) NULL,
  `lastUpdateDate` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `researchDevelopment` INT NULL,
  `effectOfAccountingCharges` INT NULL,
  `incomeBeforeTax` INT NULL,
  `minorityInterest` INT NULL,
  `netIncome` INT NULL,
  `sellingGeneralAdministrative` INT NULL,
  `grossProfit` INT NULL,
  `ebit` INT NULL,
  `operatingIncome` INT NULL,
  `otherOperatingExpenses` INT NULL,
  `interestExpense` INT NULL,
  `extraordinaryItems` INT NULL,
  `nonRecurring` INT NULL,
  `otherItems` INT NULL,
  `incomeTaxExpense` INT NULL,
  `totalOperatingExpenses` INT NULL,
  `totalRevenue` INT NULL,
  `costOfRevenue` INT NULL,
  `totalOtherIncomeExpenseNet` INT NULL,
  `discontinuedOperations` INT NULL,
  `netIncomeFromContinuingOps` INT NULL,
  `netIncomeApplicableToCommonShares` INT NULL,
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
  `createDate` DATE NULL,
  `lastUpdateDate` DATE NULL,
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
  `createDate` DATE NULL,
  `lastUpdateDate` DATE NULL,
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
  `createDate` DATE NOT NULL,
  `lastUpdateDate` DATE NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `totalLiab` INT NULL,
  `totalStockholderEquity` INT NULL,
  `otherCurrentLiab` INT NULL,
  `totalAssets` INT NULL,
  `commonStock` INT NULL,
  `otherCurrentAssets` INT NULL,
  `retainedEarnings` INT NULL,
  `otherLiab` INT NULL,
  `treasuryStock` INT NULL,
  `otherAssets` INT NULL,
  `cash` INT NULL,
  `totalCurrentLiabilities` INT NULL,
  `shortLongTermDebt` INT NULL,
  `otherStockholderEquity` INT NULL,
  `propertyPlantEquipment` INT NULL,
  `totalCurrentAssets` INT NULL,
  `longTermInvestments` INT NULL,
  `netTangibleAssets` INT NULL,
  `shortTermInvestments` INT NULL,
  `netReceivables` INT NULL,
  `longTermDebt` INT NULL,
  `inventory` INT NULL,
  `accountsPayable` INT NULL,
  `intangibleAssets` INT NULL,
  `goodWill` INT NULL,
  `capitalSurplus` INT NULL,
  `deferredLongTermAssetCharges` INT NULL,
  `minorityInterest` INT NULL,
  `deferredLongTermLiab` INT NULL,
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
