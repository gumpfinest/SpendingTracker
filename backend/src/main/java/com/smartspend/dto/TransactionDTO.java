package com.smartspend.dto;

import com.smartspend.entity.Transaction;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class TransactionDTO {

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateRequest {
        @NotBlank(message = "Description is required")
        private String description;

        @NotNull(message = "Amount is required")
        @Positive(message = "Amount must be positive")
        private BigDecimal amount;

        @NotNull(message = "Transaction type is required")
        private Transaction.TransactionType type;

        private LocalDateTime transactionDate;
        private String notes;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UpdateRequest {
        private String description;
        private BigDecimal amount;
        private Transaction.TransactionType type;
        private String category;
        private LocalDateTime transactionDate;
        private String notes;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Response {
        private Long id;
        private String description;
        private BigDecimal amount;
        private Transaction.TransactionType type;
        private String category;
        private Transaction.TransactionStatus status;
        private LocalDateTime transactionDate;
        private String notes;
        private LocalDateTime createdAt;

        public static Response fromEntity(Transaction transaction) {
            return Response.builder()
                    .id(transaction.getId())
                    .description(transaction.getDescription())
                    .amount(transaction.getAmount())
                    .type(transaction.getType())
                    .category(transaction.getCategory())
                    .status(transaction.getStatus())
                    .transactionDate(transaction.getTransactionDate())
                    .notes(transaction.getNotes())
                    .createdAt(transaction.getCreatedAt())
                    .build();
        }
    }
}
