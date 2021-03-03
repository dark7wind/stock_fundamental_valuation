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
  `createdDate` DATE NOT NULL,
  `lastUpdatedDate` DATE NOT NULL,
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
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `stockId` INT UNSIGNED NOT NULL,
  `endDate` DATE NOT NULL,
  `createdDate` VARCHAR(45) NOT NULL,
  `lastUpdatedDate` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
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
  PRIMARY KEY (`id`),
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
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `stockId` INT UNSIGNED NOT NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `createdDate` DATE NOT NULL,
  `lastUpdatedDate` DATE NOT NULL,
  `sharesOutstanding` VARCHAR(32) NULL,
  PRIMARY KEY (`id`),
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
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `stockId` INT UNSIGNED NOT NULL,
  `endDate` DATE NOT NULL,
  `createdDate` DATE NOT NULL,
  `lastUpdatedDate` DATE NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `investments` BIGINT NULL,
  `changeToLiabilities` BIGINT NULL,
  `totalCashflowsFromInvestingActivities` BIGINT NULL,
  `netBorrowings` BIGINT NULL,
  `totalCashFromFinancingActivities` BIGINT NULL,
  `changeToOperatingActivities` BIGINT NULL,
  `issuanceOfStock` BIGINT NULL,
  `netIncome` BIGINT NULL,
  `changeInCash` BIGINT NULL,
  `repurchaseOfStock` BIGINT NULL,
  `totalCashFromOperatingActivities` BIGINT NULL,
  `depreciation` BIGINT NULL,
  `otherCashflowsFromInvestingActivities` BIGINT NULL,
  `dividendsPaid` BIGINT NULL,
  `changeToInventory` BIGINT NULL,
  `changeToAccountReceivables` BIGINT NULL,
  `otherCashflowsFromFinancingActivities` BIGINT NULL,
  `changeToNetincome` BIGINT NULL,
  `capitalExpenditures` BIGINT NULL,
  `effectOfExchangeRate` BIGINT NULL,
  PRIMARY KEY (`id`),
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
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
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
  PRIMARY KEY (`id`),
  INDEX `fk_balance_sheet_stock_info1_idx` (`stockId` ASC) VISIBLE,
  CONSTRAINT `fk_balance_sheet_stock_info1`
    FOREIGN KEY (`stockId`)
    REFERENCES `securities_database`.`stock_info` (`stockId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securities_database`.`income_statement_TTM`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`income_statement_TTM` ;

CREATE TABLE IF NOT EXISTS `securities_database`.`income_statement_TTM` (
  `Id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `StockId` INT UNSIGNED NOT NULL,
  `Date` VARCHAR(45) NOT NULL,
  `CreatedDate` DATE NOT NULL,
  `LastUpdatedDate` DATE NOT NULL,
  `Type` VARCHAR(45) NOT NULL,
  `Ticker` VARCHAR(45) NOT NULL,
  `TotalRevenue` BIGINT NULL,
  `CostofRevenue` BIGINT NULL,
  `GrossProfit` BIGINT NULL,
  `OperatingExpense` BIGINT NULL,
  `OperatingIncome` BIGINT NULL,
  `NetNonOperatingInterestIncomeExpense` BIGINT NULL,
  `OtherIncomeExpense` BIGINT NULL,
  `PretaxIncome` BIGINT NULL,
  `TaxProvision` BIGINT NULL,
  `NetIncomeCommonStockholders` BIGINT NULL,
  `DilutedNIAvailabletoComStockholders` BIGINT NULL,
  `BasicEPS` BIGINT NULL,
  `DilutedEPS` BIGINT NULL,
  `BasicAverageShares` BIGINT NULL,
  `DilutedAverageShares` BIGINT NULL,
  `TotalOperatingIncomeasReported` BIGINT NULL,
  `TotalExpenses` BIGINT NULL,
  `NetIncomefromContinuingDiscontinuedOperation` BIGINT NULL,
  `NormalizedIncome` BIGINT NULL,
  `InterestExpense` BIGINT NULL,
  `NetInterestIncome` BIGINT NULL,
  `EBIT` BIGINT NULL,
  `ReconciledCostofRevenue` BIGINT NULL,
  `ReconciledDepreciation` BIGINT NULL,
  `NetIncomefromContinuingOperationNetMinorityInterest` BIGINT NULL,
  `TotalUnusualItemsExcludingGoodwill` BIGINT NULL,
  `TotalUnusualItems` BIGINT NULL,
  `NormalizedEBITDA` BIGINT NULL,
  `TaxRateforCalcs` BIGINT NULL,
  `TaxEffectofUnusualItems` BIGINT NULL,
  `InterestIncome` BIGINT NULL,
  `EBITDA` BIGINT NULL,
  `EarningsfromEquityInterestNetofTax` BIGINT NULL,
  `AverageDilutionEarnings` BIGINT NULL,
  `CreditLossesProvision` BIGINT NULL,
  `NonInterestExpense` BIGINT NULL,
  `INTEREST_INCOME_AFTER_PROVISION_FOR_LOAN_LOSS` BIGINT NULL,
  `TotalMoneyMarketInvestments` BIGINT NULL,
  `RentExpenseSupplemental` BIGINT NULL,
  `OtherNonOperatingIncomeExpenses` BIGINT NULL,
  `SpecialIncomeCharges` BIGINT NULL,
  `IncomefromAssociatesOtherParticipatingInterests` BIGINT NULL,
  PRIMARY KEY (`Id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securities_database`.`historical_price`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`historical_price`;

CREATE TABLE IF NOT EXISTS `securities_database`.`historical_price` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `stockId` INT UNSIGNED NOT NULL,
  `date` VARCHAR(45) NOT NULL,
  `createdDate` DATE NOT NULL,
  `lastUpdatedDate` DATE NOT NULL,
  `ticker` VARCHAR(45) NOT NULL,
  `open` FLOAT NULL,
  `high` FLOAT NULL,
  `low` FLOAT NULL,
  `close` FLOAT NULL,
  `adjclose` FLOAT NULL,
  `volume` FLOAT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `securities_database`.`analysis_info_revenue`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `securities_database`.`analysis_info_revenue`;

CREATE TABLE IF NOT EXISTS `securities_database`.`analysis_info_revenue` (
  `Id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `StockId` INT UNSIGNED NOT NULL,
  `Year` DATE NOT NULL,
  `CreatedDate` DATE NOT NULL,
  `LastUpdatedDate` DATE NOT NULL,
  `Ticker` VARCHAR(45) NOT NULL,
  `AvgEstimate` VARCHAR(45) NULL,
  `LowEstimate` VARCHAR(45) NULL,
  `HighEstimate` VARCHAR(45) NULL,
  `YearAgoSales` VARCHAR(45) NULL,
  `SalesGrowth` VARCHAR(45) NULL,
  `CurrentYearFlag` TINYINT NULL,
  `NoofAnalysts` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
