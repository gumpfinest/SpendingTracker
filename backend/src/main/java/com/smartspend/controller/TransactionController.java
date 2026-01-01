package com.smartspend.controller;

import com.smartspend.dto.TransactionDTO;
import com.smartspend.entity.User;
import com.smartspend.service.TransactionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/transactions")
@RequiredArgsConstructor
@Tag(name = "Transactions", description = "Transaction management endpoints")
public class TransactionController {

    private final TransactionService transactionService;

    @PostMapping
    @Operation(summary = "Create a new transaction")
    public ResponseEntity<TransactionDTO.Response> createTransaction(
            @AuthenticationPrincipal User user,
            @Valid @RequestBody TransactionDTO.CreateRequest request) {
        return ResponseEntity.ok(transactionService.createTransaction(user, request));
    }

    @GetMapping
    @Operation(summary = "Get all transactions for the authenticated user")
    public ResponseEntity<List<TransactionDTO.Response>> getTransactions(
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(transactionService.getUserTransactions(user));
    }

    @GetMapping("/range")
    @Operation(summary = "Get transactions within a date range")
    public ResponseEntity<List<TransactionDTO.Response>> getTransactionsByDateRange(
            @AuthenticationPrincipal User user,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endDate) {
        return ResponseEntity.ok(transactionService.getTransactionsByDateRange(user, startDate, endDate));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get a specific transaction")
    public ResponseEntity<TransactionDTO.Response> getTransaction(
            @AuthenticationPrincipal User user,
            @PathVariable Long id) {
        return ResponseEntity.ok(transactionService.getTransaction(user, id));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update a transaction")
    public ResponseEntity<TransactionDTO.Response> updateTransaction(
            @AuthenticationPrincipal User user,
            @PathVariable Long id,
            @Valid @RequestBody TransactionDTO.UpdateRequest request) {
        return ResponseEntity.ok(transactionService.updateTransaction(user, id, request));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a transaction")
    public ResponseEntity<Void> deleteTransaction(
            @AuthenticationPrincipal User user,
            @PathVariable Long id) {
        transactionService.deleteTransaction(user, id);
        return ResponseEntity.noContent().build();
    }
}
