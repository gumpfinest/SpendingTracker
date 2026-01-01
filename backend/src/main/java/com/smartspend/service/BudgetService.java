package com.smartspend.service;

import com.smartspend.dto.BudgetDTO;
import com.smartspend.entity.Budget;
import com.smartspend.entity.User;
import com.smartspend.repository.BudgetRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class BudgetService {

    private final BudgetRepository budgetRepository;

    @Transactional
    public BudgetDTO.Response createBudget(User user, BudgetDTO.CreateRequest request) {
        // Check if budget already exists for this category/month/year
        if (budgetRepository.findByUserAndCategoryAndMonthAndYear(
                user, request.getCategory(), request.getMonth(), request.getYear()).isPresent()) {
            throw new RuntimeException("Budget already exists for this category and period");
        }

        Budget budget = Budget.builder()
                .user(user)
                .category(request.getCategory())
                .monthlyLimit(request.getMonthlyLimit())
                .currentSpent(BigDecimal.ZERO)
                .month(request.getMonth())
                .year(request.getYear())
                .build();

        budget = budgetRepository.save(budget);
        return BudgetDTO.Response.fromEntity(budget);
    }

    public List<BudgetDTO.Response> getUserBudgets(User user, Integer month, Integer year) {
        return budgetRepository.findByUserAndMonthAndYear(user, month, year)
                .stream()
                .map(BudgetDTO.Response::fromEntity)
                .collect(Collectors.toList());
    }

    public BudgetDTO.Response getBudget(User user, Long budgetId) {
        Budget budget = budgetRepository.findById(budgetId)
                .orElseThrow(() -> new RuntimeException("Budget not found"));

        if (!budget.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Access denied");
        }

        return BudgetDTO.Response.fromEntity(budget);
    }

    @Transactional
    public BudgetDTO.Response updateBudget(User user, Long budgetId, BudgetDTO.UpdateRequest request) {
        Budget budget = budgetRepository.findById(budgetId)
                .orElseThrow(() -> new RuntimeException("Budget not found"));

        if (!budget.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Access denied");
        }

        if (request.getMonthlyLimit() != null) {
            budget.setMonthlyLimit(request.getMonthlyLimit());
        }

        budget.setUpdatedAt(LocalDateTime.now());
        budget = budgetRepository.save(budget);

        return BudgetDTO.Response.fromEntity(budget);
    }

    @Transactional
    public void deleteBudget(User user, Long budgetId) {
        Budget budget = budgetRepository.findById(budgetId)
                .orElseThrow(() -> new RuntimeException("Budget not found"));

        if (!budget.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Access denied");
        }

        budgetRepository.delete(budget);
    }
}
