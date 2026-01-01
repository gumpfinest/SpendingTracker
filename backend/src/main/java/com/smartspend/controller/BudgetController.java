package com.smartspend.controller;

import com.smartspend.dto.BudgetDTO;
import com.smartspend.entity.User;
import com.smartspend.service.BudgetService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/budgets")
@RequiredArgsConstructor
@Tag(name = "Budgets", description = "Budget management endpoints")
public class BudgetController {

    private final BudgetService budgetService;

    @PostMapping
    @Operation(summary = "Create a new budget")
    public ResponseEntity<BudgetDTO.Response> createBudget(
            @AuthenticationPrincipal User user,
            @Valid @RequestBody BudgetDTO.CreateRequest request) {
        return ResponseEntity.ok(budgetService.createBudget(user, request));
    }

    @GetMapping
    @Operation(summary = "Get budgets for a specific month and year")
    public ResponseEntity<List<BudgetDTO.Response>> getBudgets(
            @AuthenticationPrincipal User user,
            @RequestParam Integer month,
            @RequestParam Integer year) {
        return ResponseEntity.ok(budgetService.getUserBudgets(user, month, year));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get a specific budget")
    public ResponseEntity<BudgetDTO.Response> getBudget(
            @AuthenticationPrincipal User user,
            @PathVariable Long id) {
        return ResponseEntity.ok(budgetService.getBudget(user, id));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update a budget")
    public ResponseEntity<BudgetDTO.Response> updateBudget(
            @AuthenticationPrincipal User user,
            @PathVariable Long id,
            @Valid @RequestBody BudgetDTO.UpdateRequest request) {
        return ResponseEntity.ok(budgetService.updateBudget(user, id, request));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a budget")
    public ResponseEntity<Void> deleteBudget(
            @AuthenticationPrincipal User user,
            @PathVariable Long id) {
        budgetService.deleteBudget(user, id);
        return ResponseEntity.noContent().build();
    }
}
