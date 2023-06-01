CREATE PROC [Common].[LoadDimWinningPortfolioSkuList] AS
MERGE Common.DimWinningPortfolioSkuList T
USING stage.DimWinningPortfolioSkuList S
ON S.Division = T.Division
   AND S.SKUGlobal = T.SKUGlobal
WHEN MATCHED AND NOT EXISTS
                     (
                         SELECT S.[IsActive],
                                S.[MarketingComment],
                                S.[PhaseOutQuarter],
                                S.[PhaseOutYear],
                                S.[SKUGroup],
                                S.[CreatedOn],
                                S.[UpdatedOn]
                         INTERSECT
                         SELECT T.[IsActive],
                                T.[MarketingComment],
                                T.[PhaseOutQuarter],
                                T.[PhaseOutYear],
                                T.[SKUGroup],
                                T.[CreatedOn],
                                T.[UpdatedOn]
                     ) THEN
    UPDATE SET [IsActive] = S.[IsActive],
               [MarketingComment] = S.[MarketingComment],
               [PhaseOutQuarter] = S.[PhaseOutQuarter],
               [PhaseOutYear] = S.[PhaseOutYear],
               [SKUGroup] = S.[SKUGroup],
               [UpdatedOn] = SYSDATETIMEOFFSET();

INSERT INTO Common.DimWinningPortfolioSkuList
(
    [Division],
    [IsActive],
    [MarketingComment],
    [PhaseOutQuarter],
    [PhaseOutYear],
    [SKUGlobal],
    [SKUGroup],
    [CreatedOn],
    [UpdatedOn]
)
SELECT si.[Division],
       si.[IsActive],
       si.[MarketingComment],
       si.[PhaseOutQuarter],
       si.[PhaseOutYear],
       si.[SkuGlobal],
       si.[SkuGroup],
       SYSDATETIMEOFFSET(),
       SYSDATETIMEOFFSET()
FROM stage.DimWinningPortfolioSkuList si
    LEFT OUTER JOIN Common.DimWinningPortfolioSkuList di
        ON si.Division = di.Division
           AND si.SkuGlobal = di.SkuGlobal
WHERE di.Division IS NULL
      AND di.SkuGlobal IS NULL;


UPDATE STATISTICS Common.DimWinningPortfolioSkuList;