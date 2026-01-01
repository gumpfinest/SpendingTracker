package com.smartspend.dto;

import com.smartspend.entity.Budget;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

public class BudgetDTO {

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateRequest {
        @NotBlank(message = "Category is required")
        private String category;

        @NotNull(message = "Monthly limit is required")
        @Positive(message = "Monthly limit must be positive")
        private BigDecimal monthlyLimit;

        @NotNull(message = "Month is required")
        private Integer month;

        @NotNull(message = "Year is required")
        private Integer year;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UpdateRequest {
        private BigDecimal monthlyLimit;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Response {
        private Long id;
        private String category;
        private BigDecimal monthlyLimit;
        private BigDecimal currentSpent;
        private BigDecimal remaining;
        private Double percentageUsed;
        private Integer month;
        private Integer year;

        public static Response fromEntity(Budget budget) {
            BigDecimal remaining = budget.getMonthlyLimit().subtract(budget.getCurrentSpent());
            double percentageUsed = budget.getMonthlyLimit().compareTo(BigDecimal.ZERO) > 0
                    ? budget.getCurrentSpent().divide(budget.getMonthlyLimit(), 4, java.math.RoundingMode.HALF_UP)
                            .multiply(BigDecimal.valueOf(100)).doubleValue()
                    : 0.0;

            return Response.builder()
                    .id(budget.getId())
                    .category(budget.getCategory())
                    .monthlyLimit(budget.getMonthlyLimit())
                    .currentSpent(budget.getCurrentSpent())
                    .remaining(remaining)
                    .percentageUsed(percentageUsed)
                    .month(budget.getMonth())
                    .year(budget.getYear())
                    .build();
        }
    }
}
