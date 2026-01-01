package com.smartspend.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

public class AnalyticsDTO {

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DashboardSummary {
        private BigDecimal totalBalance;
        private BigDecimal monthlyIncome;
        private BigDecimal monthlyExpenses;
        private BigDecimal monthlySavings;
        private Map<String, BigDecimal> spendingByCategory;
        private List<TransactionDTO.Response> recentTransactions;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SpendingForecast {
        private List<MonthlyForecast> forecasts;
        private BigDecimal projectedSavings;
        private String advice;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MonthlyForecast {
        private String month;
        private BigDecimal predictedSpending;
        private BigDecimal predictedSavings;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CategoryAnalysis {
        private String category;
        private BigDecimal totalSpent;
        private BigDecimal averageTransaction;
        private Integer transactionCount;
        private Double percentageOfTotal;
    }
}
